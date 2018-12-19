/*-------------------------------------------------------------------------------------------+
 *                         Injection Engine for Additive Injectors                            |
 *                                     (inj_eng.c)                                            |
 *         -For the Accuload III.                                                             |
 *         -Michael Becker                                                                    |
 *                                                                                            |
 *         This file contains the actual Injection engine fcn.                                |
 *                                                                                            |
 *         Modifications for the AIIID (8/5/99) - The engine now calls its functionality      |
 *     from a table of functions, all of which are designed to be different to                |
 *     function with the different configurations of arms available on the AIIID.             |
 *     There are two tables with these fcns resident:                                         |
 *              - RunInjectors      - Controls actual pacing and on/off states                |
 *              - GetPulsesForInj   - Accumulates meter pulses for the injector               |
 *                                    Pacing.                                                 |
 *                                                                                            |
 *         Functions Included In This File:                                                   |
 *                 - GetVolForInj_StraightProduct                                             |
 *                 - GetVolForInj_SequentialBlender                                           |
 *                 - GetVolForInj_RatioBlender                                                |
 *                 - GetVolForInj_SideStream                                                  |
 *                 - RunInjectors_Standard                                                    |
 *                 - inj_engine                                                               |
 *                 - check_additive_feedback                                                  |
 *                                                                                            |
 *         Initial Editing/Creation Date: 11/10/98                                            |
 *-------------------------------------------------------------------------------------------*/
#include "options.h"
#include "add_inj.h"    
#include "database.h"
#include "io_task.h"
#include "aicb_io.h"
#include "add_inj.h"

#include "mtr_inj.h"
#include "alarms.h"
#include "inj_eng.h"
#include "stamgr.h"
#include "vlcalc.h"
#include "sai_cmds.h"
#include "share_lib.h"
#include "comm_inj.h"
#include "aicb_io.h"
#include <string.h>
#include <stdio.h>
#include <iostream>
#include <syslog.h>
#include "prv_inj.h"
#include "inj_tx.h"


//TODO: #pragma sep_on class pf_saved
unsigned char   injector_state  [MAX_INJECTORS];    /* The current state of the injection/injectors         */
double          CurBatchVol     [MAX_INJECTORS];    /* The current volume that the injector is pacing on.   */
unsigned char 	InjectDelayActive[MAX_LOAD_ARMS];
unsigned char InjRateRecalcDueToDelay[MAX_INJECTORS];

//TODO: extern struct MtrInjData MI[MAX_DUMB_INJECTORS];
//TODO: unsigned char ArmFlowState[MAX_LOAD_ARMS];
extern byte LatestRecipe[MAX_LOAD_ARMS];
extern enum OTF_arm_inj_state OTF_ArmInjState[MAX_LOAD_ARMS];
//TODO: #pragma sep_off

/*States of piston injectors for feedback*/
//TODO: #pragma sep_on class pf_saved
unsigned char PistonFeedBackInactive[MAX_INJECTORS];
//TODO: #pragma sep_off
unsigned char PistonFeedBackStatus[MAX_INJECTORS];

//TODO: #pragma sep_on
extern unsigned char SeqPrdFactorPrd[MAX_LOAD_ARMS];
extern enum OTF_inj_states OTF_InjState[MAX_INJECTORS];
extern unsigned long OTF_ArmDeauthTime[MAX_LOAD_ARMS];
//TODO: METER_DATA *ArmMeterData[MAX_LOAD_ARMS][MAX_METERS];
//TODO: #pragma sep_off

// Enable injection pacing/volumes
#define DEBUG_INJ_VOL
#ifdef DEBUG_INJ_VOL
extern double CurBatchVol[MAX_INJECTORS];
#endif

unsigned char InjInProgress		[MAX_INJECTORS];

extern float tempPrvVol;
extern float prove_pulses;
extern int InjCmdSent;
extern bool startPrvInject;
extern unsigned char InjPerRequest;
extern byte injInProgress;
unsigned char solenoid_response;
extern bool start_timer;
int proves;
extern void PulseFactorCalc_Seq(register unsigned char arm);
extern void SAI_SetState(unsigned char inj_no, unsigned char output, unsigned char state);
long timeout_AICB_IO = ten_ms_ticks;
long timeout_PROVING = ten_ms_ticks;
enum Inj_Diag_Entered injDiagEntered;

// FUNCTIONS
/*-------------------------------------------------------------------------------+
 *                      Additive Injector Function Tables                         |
 *                                                                                |
 *  These tables are arrays of pointers to functions.  One advantage of this      |
 *  approach may be seen in the inj_engine fcn itself. Use of these tables makes  |
 *  the code identical on that level no matter what the configuration of the      |
 *  arm (Straight, Seq, or Ratio).  It also allows for a modular approach to      |
 *  coding, debugging, and possible additions to the AccuLoad.                    |
 *-------------------------------------------------------------------------------*/
static void GetVolForInj_StraightProduct (register unsigned char arm)
{
	/******************************/
	register unsigned int   TempPrdPulses;
	register double         main_meter_pulses;
	register unsigned char  inj;
	double          		TempVol;
	double					pure_prod_pulses;
	/* 	Since this is a Straight product delvery, we know that the mtr = 0
		and prd = 0, so we will #define, and #undef these, since if they were 
		declared const, the compiler would still put them in RAM. 			*/
#define mtr_0	(unsigned char)0
#define prd_0	(unsigned char)0
	/******************************/

	/*  Let's get the current number of pulses for this batch. */
	/*	ArmMeterData[arm][mtr_0]->NewMtrPulses and MI[inj].ThisInjPulses were updated in io_task() so they
	    should be close in sync*/  
	if(ArmMeterData[arm][mtr_0] == NULL)
		return; //arm not active arm when virtual swing arm functionallity active

	TempPrdPulses = ArmMeterData[arm][mtr_0]->NewMtrPulses;

	if(are_there_upstream_flow_control_add(arm))
	{
		/*determine how much of tempPulses is  pure product*/
		pure_prod_pulses =
				subtract_fc_additive_pulses_from_product_pulses (arm,  TempPrdPulses, pDB.arm[arm].mtr[0].k_factor);
		if(pDB.pulse_in_type == VOL_PULSE)
			main_meter_pulses = pure_prod_pulses + ((rDB.arm[arm].prd[0].prd_without_fc_add[IV] -
					rDB.arm[arm].prd[0].total_downstream_injection_to_add) * pDB.arm[arm].mtr[0].k_factor ); /*total_downstream_injection_to_add is additive other than flow control*/
		else
			main_meter_pulses = pure_prod_pulses + ((rDB.arm[arm].prd[0].prd_raw_mass - 
					rDB.arm[arm].prd[0].total_downstream_injection_to_add) * pDB.arm[arm].mtr[0].k_factor);

		TempVol = (main_meter_pulses * (double)InjPulseFactor[arm][mtr_0]);
	}

	else
		TempVol     = ((double)TempPrdPulses + rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[0].total_pulses)
		* (double)InjPulseFactor[arm][mtr_0];

	for (inj=0; inj<MAX_INJECTORS; inj++)
	{
		if (rDB.add_inj.inj[inj].arm != arm) continue;
		CurBatchVol[inj] = TempVol;
	}

#undef mtr_0
#undef prd_0

	return;
}




static void GetVolForInj_SequentialBlender (register unsigned char arm)
{
	/***************************************************************************/
	register unsigned char  inj;
	register unsigned char  prd;
	register unsigned int   tempPulses;
	register unsigned char 	CurPrd;
	register unsigned char 	WalkingBit = 0x01;
	register unsigned char 	*pInjArm;
	register unsigned char 	*pInjPrds;
	unsigned char			up_fc_add;
	register double 		*pPrdTotal;
	register double			*pPrdPulses;
	register float			temp_inj_pulse_factor;
	double          		TempVol;
	double					temp_pure_prod_pulses;
	float k_factor;
	struct s_load_arm_run_data *arm_ptr;
	/* 	Since this is a Sequential product delvery, we know that the mtr = 0,  */
	/*	so we will #define, and #undef it, since if it was 					   */
	/*	declared const, the compiler would still put it in RAM. 			   */
#define mtr_0		((unsigned char)0)
	/***************************************************************************/

	if(ArmMeterData[arm][mtr_0] == NULL)
		return;//arm not active arm when virtual swing arm functionallity active 
	/* Get the current product */
	CurPrd = rDB.arm[arm].arm.seq_prd;

	/*  Let's get the current number of pulses for this batch. */
	tempPulses = ArmMeterData[arm][mtr_0]->NewMtrPulses;
	arm_ptr = &rDB.arm[arm];
	k_factor = 	pDB.arm[arm].mtr[0].k_factor;
	up_fc_add = FALSE;
	if(are_there_upstream_flow_control_add(arm))
	{
		up_fc_add = TRUE;

		/*determine how much of tempPulses is  pure product*/
		temp_pure_prod_pulses =
				subtract_fc_additive_pulses_from_product_pulses (arm, tempPulses, k_factor);
		TempVol = temp_pure_prod_pulses *  (InjPulseFactor[arm][mtr_0]);
	}
	else
		TempVol = ((double)tempPulses) * (InjPulseFactor[arm][mtr_0]);

	pInjPrds 	= &rDB.add_inj.inj[0].prds_used;
	pInjArm 	= &rDB.add_inj.inj[0].arm;
	pPrdTotal 	= &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[MAX_PRODUCTS].cur_[pDB.add_inj.vol_used];
	pPrdPulses	= &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[MAX_PRODUCTS].total_pulses;
	for (inj=0; inj<MAX_INJECTORS; inj++)
	{
		// This injector is on this arm!!!
		if (*pInjArm == arm)
		{
			CurBatchVol[inj] = 0;
			pPrdTotal = 
					(double *)(		(unsigned long)pPrdTotal
							- 	(unsigned long)(MAX_PRODUCTS * sizeof(struct s_product_batch_data))		);

			/*with downstream injectors the injection is not metered with product volume like an upstream inj.
	 		  The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
			  the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
	 		  Regardless of injector type, injection rate is based of what was actually metered. If downstream inj paces it
	 		  its equivalent to being plumbed to it*/  
			pPrdPulses = 
					(double *)(		(unsigned long)pPrdPulses
							- 	(unsigned long)(MAX_PRODUCTS * sizeof(struct s_product_batch_data))		);


			for (prd=0; prd<MAX_PRODUCTS; prd++)
			{
				if (*pInjPrds & (WalkingBit<<prd))
				{
					if(prd != CurPrd)
					{
						/*with downstream injectors the injection is not metered with product volume like an upstream inj.
	 		  		The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
			  		the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
	 		  		Regardless of injector type, injection rate is based of what was actually metered. If downstream inj paces it
	 		  		its equivalent to being plumbed to it*/  

						temp_inj_pulse_factor= InjPulseFactor[arm][mtr_0];
						SeqPrdFactorPrd[arm] = prd;
						PulseFactorCalc_Seq(arm);
						if(!up_fc_add)
							CurBatchVol[inj] += *pPrdPulses * InjPulseFactor[arm][mtr_0];/*prior to flow control additives*/
						else
						{
							if(pDB.pulse_in_type == VOL_PULSE)									  /*additive other than flow control*/
								CurBatchVol[inj] += ((arm_ptr->prd[prd].prd_without_fc_add[IV] - arm_ptr->prd[prd].total_downstream_injection_to_add) *
										pDB.arm[arm].mtr[0].k_factor) * InjPulseFactor[arm][mtr_0];
							else													   /*additive other than flow control*/
								CurBatchVol[inj] += ((arm_ptr->prd[prd].prd_raw_mass - arm_ptr->prd[prd].total_downstream_injection_to_add)*
										pDB.arm[arm].mtr[0].k_factor) * InjPulseFactor[arm][mtr_0];
						}
						SeqPrdFactorPrd[arm] = MAX_PRODUCTS;
						InjPulseFactor[arm][mtr_0] = temp_inj_pulse_factor;

					}
					else
					{
						SeqPrdFactorPrd[arm] = MAX_PRODUCTS;
						if(!up_fc_add)
							CurBatchVol[inj] += *pPrdPulses * InjPulseFactor[arm][mtr_0];
						else
						{
							if(pDB.pulse_in_type == VOL_PULSE)									  /*additive other than flow control*/
								CurBatchVol[inj] += ((arm_ptr->prd[prd].prd_without_fc_add[IV] - arm_ptr->prd[prd].total_downstream_injection_to_add)*
										pDB.arm[arm].mtr[0].k_factor) * InjPulseFactor[arm][mtr_0];
							else													   /*additive other than flow control*/
								CurBatchVol[inj] += ((arm_ptr->prd[prd].prd_raw_mass - arm_ptr->prd[prd].total_downstream_injection_to_add)*
										pDB.arm[arm].mtr[0].k_factor) * InjPulseFactor[arm][mtr_0];
						}
					}
				}
				pPrdTotal = 
						(double *)(		(unsigned long)pPrdTotal
								+ 	(unsigned long)sizeof(struct s_product_batch_data)		);

				pPrdPulses = 
						(double *)(		(unsigned long)pPrdPulses
								+ 	(unsigned long)sizeof(struct s_product_batch_data)		);
			}

			/* If the injector is for this product, add in the real time vol */
			if (*pInjPrds & (WalkingBit<<CurPrd))
				CurBatchVol[inj] += TempVol;
		}

		pInjPrds 	+= sizeof(struct run_injector);
		pInjArm 	+= sizeof(struct run_injector);
	}

#undef mtr_0
	return;
}


static void GetVolForInj_RatioBlender (register unsigned char arm)
{
	/***************************************************************************************************/
	register unsigned int   TempPrdPulses;
	register unsigned char  inj;
	double          		TempVol[MAX_METERS];
	register unsigned char 	WalkingBit = 0x01;
	register unsigned char  prd_mtr;   	/* Since we are a ratio blender, we know that the Mtr */
	/* should equal the product. */
	struct s_product_batch_data	*batch_prd_ptr;

	/***************************************************************************************************/

	if(ArmMeterData[arm][0] == NULL)
		return;//arm not active arm when virtual swing arm functionallity active 
	/******** Product Loop ***********************************************/
	for (prd_mtr=0; prd_mtr<pDB.arm[arm].arm_product; prd_mtr++)
	{
		batch_prd_ptr = &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[prd_mtr];
		/*  Let's get the current number of pulses for this batch. */
		TempPrdPulses = ArmMeterData[arm][prd_mtr]->NewMtrPulses;/*get pulses not yet accounted for by vlcalc, insure most recent amount*/

		/*with downstream injectors the injection is not metered with product volume like an upstream inj.
	 	The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
		the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
	 	Regardless of injector type, injection rate is based of what was actually metered. If downstream inj paces it
	 	its equivalent to being plumbed to it*/  
		TempVol[prd_mtr] 	= ((double)TempPrdPulses + batch_prd_ptr->total_pulses) * InjPulseFactor[arm][prd_mtr];
	}


	/******** Injector Loop ***********************************************/
	for (inj=0; inj<pDB.num_inj_used; inj++)
	{
		/* If this inj is for the wrong arm, get out. */
		if (rDB.add_inj.inj[inj].arm != arm) continue;

		/* 	If we are here, this inj is on thsi arm, so its ok to wipe out it's pacing vol, since
			if its used, it will be put in below.  */
		CurBatchVol[inj] 	= 0;

		/******** Injector Product Summation Loop ***********************************************/
		for (prd_mtr=0; prd_mtr<pDB.arm[arm].arm_product; prd_mtr++)
		{
			/* If the injector isn't plumbed for this mtr, get out. */
			/* if ((  bmp 					  AND 			bit ) != TRUE )	*/
			if(pDB.add_inj.inj[inj].up_or_down == UPSTREAM_INJ)
			{
				if (!(pDB.add_inj.inj[inj].plumbing & (WalkingBit<<prd_mtr)))
					continue;
				CurBatchVol[inj] += TempVol[prd_mtr];
			}
			else/*this injector is downstream*/
			{
				/*see if the injector is paced by this product*/
				if(!(pDB.recipe[rDB.arm[arm].arm.cur_recipe].inj_prods[inj] & (0x01<<prd_mtr)))
					continue;
				CurBatchVol[inj] += TempVol[prd_mtr];
			}
		}
		/****************************************************************************************/
	}

}



static void GetVolForInj_SideStreamBlender (register unsigned char arm)
{
	/***************************************************************************************************/
	unsigned int   						tempPrdPulses[MAX_METERS];
	unsigned int   						tempPrdPulses_0;
	register unsigned char  			inj;
	double          					tempVol[MAX_METERS];
	register unsigned char 				walkingBit = 0x01;
	register int  						prd_mtr;   	/* Since we are a ratio blender, we know that the Mtr */
	/* should equal the product. */
	struct s_product_batch_data	*batch_prd_ptr;	 

	/***************************************************************************************************/
	/******** Product Loop ***********************************************/
	if(ArmMeterData[arm][0] == NULL)
		return;//arm not active arm when virtual swing arm functionallity active

	for (prd_mtr=0; prd_mtr<pDB.arm[arm].arm_product; prd_mtr++)
	{
		batch_prd_ptr = &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[prd_mtr];
		/*  Let's get the current number of pulses for these products */

		tempPrdPulses[prd_mtr] = ArmMeterData[arm][prd_mtr]->NewMtrPulses;

		/*with downstream injectors the injection is not metered with product volume like an upstream inj.
	 	The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
		the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
	 	Regardless of injector type, injection rate is based of what was actually metered, with downstream inj 
	 	if product paces it its equivalent to being plumbed to it*/  
		tempVol[prd_mtr]	= (((double)tempPrdPulses[prd_mtr]) + batch_prd_ptr->total_pulses) *
				InjPulseFactor[arm][prd_mtr];
	}

	//---------------------------------------------------------------------------------------------------------
	// Right here, do the special case
	tempPrdPulses_0 = tempPrdPulses[0];

	for (prd_mtr=1; prd_mtr<pDB.arm[arm].arm_product; prd_mtr++)
	{
		tempPrdPulses[0] -= (pDB.arm[arm].mtr[0].k_factor/pDB.arm[arm].mtr[prd_mtr].k_factor)*tempPrdPulses[prd_mtr];
		// If we wrapped, or went negative (If we didn't wrap, then  tempPrdPulses_0 >= tempPrdPulses[0].
		if (tempPrdPulses_0 < tempPrdPulses[0])
		{
			tempPrdPulses[0] = 0;
			break;
		}
	}

	/*with downstream injectors the injection is not metered with product volume like an upstream inj.
	The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
	the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
	Regardless of injector type, injection rate is based of what was actually metered. With downstream inj, 
	if product paces it, its equivalent to being plumbed to it*/ 
	tempVol[0] = (((double)tempPrdPulses[0]) + rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[0].total_pulses)*
			InjPulseFactor[arm][0];
	//---------------------------------------------------------------------------------------------------------



	/******** Injector Loop ***********************************************/
	for (inj=0; inj<pDB.num_inj_used; inj++)
	{
		/* If this inj is for the wrong arm, get out. */
		if (rDB.add_inj.inj[inj].arm != arm) continue;

		/* 	If we are here, this inj is on thsi arm, so its ok to wipe out it's pacing vol, since
			if its used, it will be put in below.  */
		CurBatchVol[inj] 	= 0;

		/******** Injector Product Summation Loop ***********************************************/
		for (prd_mtr=0; prd_mtr<pDB.arm[arm].arm_product; prd_mtr++)
		{
			/* If the injector isn't plumbed for this mtr, get out. */
			/* if ((  bmp 					  AND 			bit ) != TRUE )	*/
			if(pDB.add_inj.inj[inj].up_or_down == UPSTREAM_INJ)
			{
				if (!(pDB.add_inj.inj[inj].plumbing & (walkingBit<<prd_mtr)))	continue;
				CurBatchVol[inj] += tempVol[prd_mtr];
			}
			else/*this injector is downstream*/
			{
				/*see if the injector is paced by this product*/
				if(pDB.recipe[rDB.arm[arm].arm.cur_recipe].inj_prods[inj] & (0x01<<prd_mtr))
					CurBatchVol[inj] += tempVol[prd_mtr];
			}
		}
		/****************************************************************************************/
	}

	return;
}


static void GetVolForInj_Hybrid (register unsigned char arm)
{
	/***************************************************************************************************/
	unsigned int 						pulses;
	double   							tempMtrPulses[MAX_METERS];
	double								tempSeqPrdPulses;
	register unsigned char  			inj;
	double          					tempVol[MAX_METERS];
	register unsigned char 				walkingBit = 0x01;
	register int  						mtr;
	byte								p;
	byte 								current_seq_prd;
	byte 								side_stream;
	byte								ratio_prd_use;   	
	byte								u;
	struct s_product_batch_data			*batch_prd_ptr;
	struct s_recipe_params 				*psRecipe;	
	struct ss_data						ss;
	struct s_batch_run_data  			*batch_ptr;
	struct s_load_arm					*pdb_arm_ptr;

	if(ArmMeterData[arm][0] == NULL)
		return;//arm not active arm when virtual swing arm functionallity active
	/***************************************************************************************************/
	batch_ptr   = &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no];
	pdb_arm_ptr = &pDB.arm[arm];
	psRecipe = &pDB.recipe[rDB.arm[arm].arm.cur_recipe];
	/******** Product Loop ***********************************************/
	/*ratio prds first*/
	for (mtr=0; mtr<pdb_arm_ptr->num_ratio_prds; mtr++)
	{
		batch_prd_ptr = &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[mtr];
		/*  Let's get the current number of pulses for these products */
		pulses = ArmMeterData[arm][mtr]->NewMtrPulses;
		tempMtrPulses[mtr] = (double)pulses;
		/*with downstream injectors the injection is not metered with product volume like an upstream inj.
	 	The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
		the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
	 	Regardless of injector type, injection rate is based of what was actually metered, with downstream inj 
	 	if product paces it its equivalent to being plumbed to it*/
		/*since meter = product with ratio prds, do the following*/
		tempVol[mtr]	= ((tempMtrPulses[mtr] + batch_prd_ptr->total_pulses) *
				InjPulseFactor[arm][mtr]);
	}
	/*now the sequential products*/
	mtr = pdb_arm_ptr->num_ratio_prds;
	current_seq_prd = rDB.arm[arm].arm.seq_prd;
	batch_prd_ptr = &rDB.arm[arm].arm.batch[rDB.arm[arm].arm.batch_no].prd[current_seq_prd];
	/*  get the sequential meter pulses */
	pulses = ArmMeterData[arm][mtr]->NewMtrPulses;
	tempMtrPulses[mtr] = (double)pulses; 
	side_stream = is_side_stream_in_use(arm, &ss);
	if(InjPulseFactor[arm][current_seq_prd] <= 0.0)
		InjPulseFactor[arm][current_seq_prd] = 1.0;	
	if(side_stream)
	{
		/*we need to seperate the main and side meter pulses form tempMtrPulses[mtr]*/
		tempSeqPrdPulses = tempMtrPulses[mtr] - ((pdb_arm_ptr->mtr[mtr].k_factor/pdb_arm_ptr->mtr[ss.side_mtr].k_factor)*
				tempMtrPulses[ss.side_mtr]);
		// If we wrapped, or went negative (If we didn't wrap, then  tempPrdPulses_0 >= tempPrdPulses[0].
		if (tempSeqPrdPulses < 0)
			tempSeqPrdPulses = 0;
		/*with downstream injectors the injection is not metered with product volume like an upstream inj.
		The downstream injection is eventually added to the product volume (see vlcalc...calc_batch_volumes), 
		the pulses from the meter are pure product pulses...no injection from an injector with it (like upstream).
		Regardless of injector type, injection rate is based of what was actually metered. With downstream inj, 
		if product paces it, its equivalent to being plumbed to it*/ 
		tempVol[mtr] = ((tempSeqPrdPulses + batch_prd_ptr->total_pulses) *InjPulseFactor[arm][current_seq_prd]);
	}
	else
		tempVol[mtr] = ((tempMtrPulses[mtr] + batch_prd_ptr->total_pulses) *InjPulseFactor[arm][current_seq_prd]);


	/******** Injector Loop ***********************************************/
	for (inj=0; inj<pDB.num_inj_used; inj++)
	{
		if(pDB.add_inj.inj[inj].type == NOT_CONFIG)
			continue;

		if (rDB.add_inj.inj[inj].on_off != INJ_ON)
			continue;

		/* If this inj is for the wrong arm, get out. */
		if (rDB.add_inj.inj[inj].arm != arm)
			continue;

		/* 	If we are here, this inj is on this arm, so its ok to wipe out it's pacing vol, since
			if its used, it will be put in below.  */
		CurBatchVol[inj] 	= 0;

		/******** Injector Product Summation Loop ***********************************************/
		for (mtr=0; mtr<=pdb_arm_ptr->num_ratio_prds; mtr++)
		{
			/* If the injector isn't plumbed for this mtr, get out. */
			/* if ((  bmp 					  AND 			bit ) != TRUE )	*/
			if(pDB.add_inj.inj[inj].up_or_down == UPSTREAM_INJ)
			{
				/*with an upstream inj, even if none of the products of this require additive as set up in the recipe,
				  the products are set up to "pace" the injector if the injector is plumb to this meter*/
				if (!(pDB.add_inj.inj[inj].plumbing & (walkingBit<<mtr)))
					continue;
				if(mtr == pdb_arm_ptr->num_ratio_prds)
				{
					/*this is the sequential meter, gather the sequential products which pace the injector*/
					/*this is last meter in this for loop*/
					/*if no products currently flowing use this injector, bail*/
					ratio_prd_use = FALSE;
					for(u=0; u<pdb_arm_ptr->num_ratio_prds; u++)
						if((psRecipe->blend_pct[u] > 0) &&
								(((1<<u) & psRecipe->inj_prods[inj]) > 0))
						{
							ratio_prd_use = TRUE;/*flowing ratio prds use this injector*/
							break;/*from for loop*/
						}
					for(p = pdb_arm_ptr->num_ratio_prds; p < pdb_arm_ptr->arm_product; p++)
					{
						if(!ratio_prd_use && (!((1<<p) & psRecipe->inj_prods[inj])))
							continue; /*ratio prds do not use injector, the seq prd (p) does not use this injector*/
						if((p==current_seq_prd) && (rDB.arm[arm].arm.batch_status == BATCH_FLOW_IN_PROGRESS))
							CurBatchVol[inj] += tempVol[mtr];/*the current sequential product*/ 
						else
							CurBatchVol[inj] += batch_ptr->prd[p].cur_[pDB.add_inj.vol_used];
					}
				}
				else
					CurBatchVol[inj] += tempVol[mtr]; /*ratio product, meter = product*/
			}/*end of "if(pDB.add_inj.inj[inj].up_or_down == UPSTREAM_INJ)"*/
			else/*this injector is downstream*/
			{
				/*see if the injector is paced by this product*/
				if(mtr < pdb_arm_ptr->num_ratio_prds)/*ratio prd, meter = product*/	
				{
					if(psRecipe->inj_prods[inj] & (0x01<<mtr))
						CurBatchVol[inj] += tempVol[mtr];/*ratio prd paces the injector, include it*/
				}
				else/*sequential meter, see which sequential prds pace this injector, this is last meter in this for loop*/
				{
					for(p = pdb_arm_ptr->num_ratio_prds; p < pdb_arm_ptr->arm_product; p++)
					{
						if(psRecipe->inj_prods[inj] & (0x01<<p))
						{
							if((p==current_seq_prd) && (rDB.arm[arm].arm.batch_status == BATCH_FLOW_IN_PROGRESS))
								CurBatchVol[inj] += tempVol[mtr];/*the current sequential product*/ 
							else
								CurBatchVol[inj] += batch_ptr->prd[p].cur_[pDB.add_inj.vol_used];
						}
					}
				}
			}/* end of "else this injector is downstream"*/
		}/*end of "for (mtr=0; mtr<=pdb_arm_ptr->num_ratio_prds; mtr++)"*/
	}
	/****************************************************************************************/
	return;
}


/*----------------------------------------------------------------------+
 *          Additive Injector Engine Core Functions                      |
 *----------------------------------------------------------------------*/
static void RunInjectors_Standard (register unsigned char arm)
{
	//-----------------------------------------
	register int i;
	register struct run_injector *prInj;
	register unsigned char mtr_inj;
	unsigned char new_on_off;
	unsigned char turn_off_inj;
	FILE * file;
	//-----------------------------------------

	for (i=0; i<pDB.num_inj_used; i++)
	{
		prInj = &rDB.add_inj.inj[i];
		/* If we aren't on or if the injector is for the other arm, keep going. */
		if ((prInj -> on_off != INJ_ON) || (rDB.add_inj.inj[i].arm != arm))
			continue;

		if(prInj->type == FLOW_RATE_CNTRL)
			continue;

		if(injector_state[i] == INJECTOR_DONE)
			fprintf(stderr,"INJECTOR_DONE [%d]\n",i);

		new_on_off = FALSE;
		turn_off_inj = FALSE;


		/****************** TURN INJECTOR OFF !!!! *****************************/
		/* Here the injector is ON, so we are looking to turn it off. */
		if ((injector_state[i] == INJECTOR_ON) || (injector_state[i] == INJECTOR_FINISH_INJECT))
		{
			//OTF_InjState[i] == OTF_INJ_SHUT_INJ_OFF for wild stream blending with unlimited preset
			//if feature not used OTF_InjState[] will always be OTF_INJ_READY
			//Added to accomodate recipe changes during a batch "ON The FLY"
			if ((CurBatchVol[i] >= prInj -> target_vol_off) || (OTF_InjState[i] == OTF_INJ_SHUT_INJ_OFF))
			{
				prInj -> target_vol_off += prInj -> vol_per_inj;
				turn_off_inj = TRUE;
			}
			/*lets see ifwe need to shut down a piston injector because of alarm, stop key, or permissive loss*/
			/*this is the AccuLoad II method. If the above is true then we would turn of the injector right away*/
			/*the injector would then turn on again when it was previously scheduled to go off and turn off at half*/
			/*the programed rate latter*/
			else if(pDB.add_inj.piston_stop_action == DE_ENERGIZE_PISTON)
			{
				/*the accu II method if we entered this 'else if'*/
				if((prInj->type == PISTON_INJ_CTRL) || (prInj->type == PISTON_INJ_CTRL_WITH_FEEDBACK))
					if(rDB.arm[arm].arm.batch_status == BATCH_STOPPED)
					{
						turn_off_inj = TRUE;
						new_on_off = TRUE;
					}
			}

			if(rDB.add_inj.inj[i].type == ADD_PAK_2_STROKE)
			{
				//when the solenoid turns off the piston
				//travels back home pumping additive into the flow stream
				//allow additive to deliver before the product valve shuts down
				//this will apply if there is no additive stop volume  
				if(rDB.arm[arm].arm.remain_vol < (prInj->vol_per_inj/4.0))
					turn_off_inj = TRUE;
			}

			if(turn_off_inj)
			{
				if((injector_state[i] == INJECTOR_FINISH_INJECT) && (rDB.add_inj.inj[i].type != ADD_PAK_2_STROKE))
					injector_state[i] = INJECTOR_LAST_COMPLETE;
				else
					injector_state [i] = INJECTOR_OFF; /* We have turned it off. */

				prInj -> no_injector_offs ++;
				switch (prInj -> type)
				{
				case PISTON_INJ_CTRL_WITH_FEEDBACK:
					DigOut(prInj -> control_io_pt,OFF);
					if(new_on_off)
					{
						prInj->target_vol_on = prInj->target_vol_off;
						prInj->target_vol_off = prInj->target_vol_on + (prInj -> vol_per_inj * (pDB.add_inj.inj_rate_pct/100));

					}
					break;
				case PISTON_INJ_CTRL:
					DigOut(prInj -> control_io_pt,OFF);
					if(new_on_off)
					{
						prInj->target_vol_on = prInj->target_vol_off;
						prInj->target_vol_off = prInj->target_vol_on + (prInj -> vol_per_inj * (pDB.add_inj.inj_rate_pct/100));
					}
					break;
				default:
					break;
				}
				if(OTF_InjState[i] == OTF_INJ_SHUT_INJ_OFF)
				{
					//used for wild stream blending with unlimited preset
					//where recipes can change in a middle of a batch
					//and injectors can change
					OTF_ArmDeauthTime[arm] = hun_ms_ticks;
				}
			}
		}

		/******************** INJECT !!!! **************************************/
		/* Here the injector is off, so we want to turn it on. */
		//OTF_ArmInjState[arm] for wild stream blending with unlimited preset
		//if feature not used OTF_Arm InjState[] will always be OTF_ARM_INJ_READY
		//Added to accomodate recipe changes during a batch "ON The FLY"
		else if ((injector_state[i] == INJECTOR_OFF)
				&& (CurBatchVol[i] >= prInj -> target_vol_on) &&
				(OTF_ArmInjState[arm] == OTF_ARM_INJ_READY)) //OTF_ARM_INJ_READY added for wild stream blending rev 11.04
		{
			prInj -> target_vol_on += prInj -> vol_per_inj;

			/***********************************************************************************************/
			/* NOTE: *If a trap is to be put in to catch if not flowing, etc, don't inject, it should be here. */


			/*keep following if statement above	"injector_state[i] = INJECTOR_ON, etc"*/
			if(InjectDelayActive[arm])
			{	
				InjRateRecalcDueToDelay[i] = TRUE;
				continue;/*pDB.arm[arm].add_start is indicating don't inject until latter in batch*/
			}
			/************************************************************************************************/

			/*the delay is not in affect, see if we need to recalcualte a rate before we inject*/
			if(InjRateRecalcDueToDelay[i])
				Inj_rate_recalc_from_delay(arm, i, prInj);

			injector_state[i] = INJECTOR_ON; /* We have turned it on. */
			prInj -> no_injector_ons ++;
			InjInProgress[i] = 1;
			switch (prInj -> type)
			{
			case PISTON_INJ_CTRL_WITH_FEEDBACK:
				if(PistonFeedBackStatus[i] != FEEDBACK_CYCLE_COMPLETE)
					rDB.add_inj.inj[i].feedback_error++;//never got the complete feedback pulse from previous injection
				PistonFeedBackStatus[i] = FEEDBACK_WAIT_LEAD_EDGE;//indicate waiting for first edge of feedback pulse
				DigOut(prInj -> control_io_pt,ON);
				break;
			case PISTON_INJ_CTRL:
				DigOut(prInj -> control_io_pt,ON);
	
#ifdef DEBUG_INJ_VOL
	file = fopen("/home/root/inj_vol.txt", "a+");
	fprintf(file, "%s:\tInjector\t%d\tVol\t%9.3f\tBatchVol\t%8.2f\n", __FUNCTION__, i+1, rDB.add_inj.inj[i].additive_total, CurBatchVol[i]);
	syslog(LOG_ALERT, "%s|%d|%7.3f|%6.2f", __FUNCTION__, i+1, rDB.add_inj.inj[i].additive_total, CurBatchVol[i]);
	if(file != NULL)
		fclose(file);
	else
		file = NULL;
#endif
				break;

			case TITAN_INJ:
			case GATE_CITY_BLEND_PAK_INJ:
			case GATE_CITY_MINIPAK_INJ:
			case SMITH_INJ:
			case ADD_PAK_INJ:
			case ADD_PAK_2_STROKE:
				SAI_II(i);
				break;

			case METER_INJ:
			case SHARE_INJ_1:
			case SHARE_INJ_2:
			case SHARE_INJ_3:
			case SHARE_INJ_4:
				/*determine which meter injector this additive belongs to or shares*/
				/*mtr_inj should be between 0-3 only*/
				mtr_inj = AI.MtrInjectPt[i];

				if(mtr_inj >= NO_MTR_INJECT_PT)
					break;

				if((prInj->type == METER_INJ) ||
						((prInj->type >= SHARE_INJ_1) && (prInj->type <= SHARE_INJ_4)))
					SAI_II(i);

				AI.MtrInjOn[mtr_inj] = MI_INJECT;
				break;

			default:
				break;
			}
		} /* End of Injector off section. */
		//with two stroke additive, injection occurs when solenoid is enegized as piston moves to far end of cylinder
		//it also injects when solenoid is de-energized until the piston reaches its home position
		else if((injector_state[i] == INJECTOR_TWO_STROKE_HOME) && (CurBatchVol[i] >= prInj -> target_vol_on))
			injector_state[i] = INJECTOR_LAST_COMPLETE; //complete two stroke injection is done,
	}/* End of for() loop. */
	return;
}


/*-------------------------------------------------------------------------------+
 *                      Additive Injector Function Tables                         |
 *                                                                                |
 *  These tables are arrays of pointers to functions.  One advantage of this      |
 *  approach may be seen in the inj_engine fcn itself. Use of these tables makes  |
 *  the code identical on that level no matter what the configuration of the      |
 *  arm (Straight, Seq, or Ratio).  It also allows for a modular approach to      |
 *  coding, debugging, and possible additions to the AccuLoad.                    |
 *-------------------------------------------------------------------------------*/
/**********************************************************************/
/*             Injectors Pacing Table                                 */
/**********************************************************************/
void (* const RunInjectors[NUM_ARM_CONFIG_TYPES])(register unsigned char)=
{
		&RunInjectors_Standard,	    	/* STRAIGHT_PROD */
		&RunInjectors_Standard, 	 	/* SEQ_BLENDER   */
		&RunInjectors_Standard,       	/* RATIO_BLENDER */
		&RunInjectors_Standard,        	/* SIDE_STREAM   */ // This may dubplicate ratio blending
		&RunInjectors_Standard,			/* UNLOADING	 */ // unloading does not permit injectors, but we need something here
		&RunInjectors_Standard,			/* HYBRID	 */
		&RunInjectors_Standard,			/*STRAIGHT_WITH_VRS*/
};
/**********************************************************************/
/*            Pulse Accumulation Table for Injectors                  */
/**********************************************************************/
void (* const GetVolumeForInj[NUM_ARM_CONFIG_TYPES])(register unsigned char)=
{
		&GetVolForInj_StraightProduct,      /* STRAIGHT_PROD */
		&GetVolForInj_SequentialBlender,    /* SEQ_BLENDER   */
		&GetVolForInj_RatioBlender,         /* RATIO_BLENDER */
		&GetVolForInj_SideStreamBlender,     /* SIDE_STREAM   */	// This may NOT dup the ratio!
		&GetVolForInj_StraightProduct,		/*  UNLOADING	 */ // unloading does not permit injectors, but we need something here
		&GetVolForInj_Hybrid,				/*  HYBRID	 */ //
		&GetVolForInj_StraightProduct,      /* STRAIGHT_WITH_VRS, use that for straight arm */
};
/*------------------------------------------------------------------------------+
 *              End of Additive Injector Function Tables                         |
 *------------------------------------------------------------------------------*/


extern void SetSAIOverspeedAlarms(void);
/*******************************************************************************
 *                                                                              *
 *                         Injection Engine                                     *
 *   This is THE function regarding additive injections.  This is the fcn which *
 *   actually drives the IO and comm commands.  It has been modified to call    *
 *   fcns from a table of fcns to account for multiple configurations in        *
 *   multiple load arms.                                                        *
 *******************************************************************************/
void inj_engine(int arm)
{
	/***********************************/
	//register unsigned char arm;
	register unsigned char arm_config;
	int inj = rDB.system.cur_injector;
	float pulses;
	static unsigned long start_sec_ticks = 0;
	/***********************************/

	SAI_tx_task();
	SAI_rx_task();

	if ((ten_ms_ticks-timeout_AICB_IO) >= 10)
	{
		AICB_IO_task();
		timeout_AICB_IO = ten_ms_ticks;
	}

	if ( (injDiagEntered == INJ_DIAG) && (rDB.add_inj.inj[inj].arm == arm) )
	{
		if(start_timer)
		{
			start_sec_ticks = sec_ticks;
			start_timer = false;
		}

		if((sec_ticks - start_sec_ticks) >= 1)
		{
			start_sec_ticks = sec_ticks;

			//Poll Roughly Every Second
			fprintf(stderr,"injDiagEntered=%d, inj=%d\n",injDiagEntered,inj);
			SAI_ReadCount_array[SAI_ReadCount_index++] = inj;

			SAI_GetState_array[SAI_GetState_index] = inj;
			SAI_GetState_output_array[SAI_GetState_index++] = PUMP;

			SAI_GetState_array[SAI_GetState_index] = inj;
			SAI_GetState_output_array[SAI_GetState_index++] = SOLENOID;
		}

		update_inj_prove_table();
	}

	if(((injPrvEntered == MTR_INJ_PROVING) || (injPrvEntered == AICB_PROVING)) && (rDB.add_inj.inj[inj].arm == arm) )
	{
		if((sec_ticks - start_sec_ticks) >= 1)
		{
			start_sec_ticks = sec_ticks;

			/* Get the pulses coming from the Metered Injectors */
			SAI_ReadCount_array[SAI_ReadCount_index++] = inj;
			prove_pulses = CalcVolForMtrInjProve(inj);

			SAI_GetState_array[SAI_GetState_index] = inj;
			SAI_GetState_output_array[SAI_GetState_index++] = PUMP;

			if(solenoid_response == INJ_SOL_RSP_RDY)
			{
				SAI_GetState_array[SAI_GetState_index] = inj;
				SAI_GetState_output_array[SAI_GetState_index++] = SOLENOID;

				solenoid_response = INJ_SOL_RSP_WAIT;
			}
		}

		if(((InjPerRequest > 0) || (injInProgress && solenoid_response == INJ_SOL_RSP_RCVD)) && (startPrvInject))
		{
			ProveInjector(inj, tempPrvVol, InjPerRequest);
		}

		update_inj_prove_table();
	}

	/* Do mtr Inj control */
	check_mtr_inj_remote_prove(inj);
	RecalcMtrInjOnTime();
	check_additive_feedback();

	if (AI.InjEngineSema[arm] == INJECTORS_ON)
	{
		arm_config = pDB.arm[arm].arm_config;
		GetVolumeForInj[arm_config](arm);
		RunInjectors[arm_config](arm);
		if(OTF_ArmInjState[arm] == OTF_ARM_WAIT_TOTALS_SYNC)
			OTF_ArmInjState[arm] = OTF_ARM_READY_TO_PROGRAM;
	}

	// We only need to run this routine once!
	if (AI.InjEngineSema[arm] == INJECTORS_ON)
		SetSAIOverspeedAlarms();

	return;
}




/***************************************************************************
 *                                                                          *
 *                   Check Additive Feedback                                *
 *   This fcn is called from io_task itself.  It will look for any Additive *
 *   Injectors which are PISTON_CTRL_WITH_FEEDBACK and                      *
 *   dependent on which it is, it will track them looking for a timeout.    *
 ***************************************************************************/
void check_additive_feedback (void)
{
	/********************************/
	register int i = 0;
	register unsigned char state;
	/********************************/


	for (i=0; i<MAX_FEEDBACK_INJECTORS; i++)
	{
		if ((rDB.add_inj.inj[i].type != PISTON_INJ_CTRL_WITH_FEEDBACK)
				|| (rDB.add_inj.inj[i].on_off != INJ_ON))
			continue;


		/* Get the "live, real time" input. */
		state  = rDB.system.dig_in_state[(rDB.add_inj.inj[i].feedback_io_pt-1)];

		if((state != PistonFeedBackInactive[i]) && (PistonFeedBackStatus[i] == FEEDBACK_WAIT_LEAD_EDGE))
		{
			//we are now getting the feedback pulse
			PistonFeedBackStatus[i] = FEEDBACK_WAIT_TRAIL_EDGE;
		}
		else if((state == PistonFeedBackInactive[i]) && (PistonFeedBackStatus[i] == FEEDBACK_WAIT_TRAIL_EDGE))
		{
			//the feedback pulse is now complete, got both edges of the pulse
			rDB.add_inj.inj[i].number_of_inj++;
			PistonFeedBackStatus[i] = FEEDBACK_CYCLE_COMPLETE;
		}
	}
	return;
}


/***************************************************************************
 *                                                                          *
 *                   Inj_rate_recalc_from_delay                             *
 *   The purpose of this function is to recalculate the injector rate	   *
 *   once the delay (pDB.arm[].add_start) expires		                   *
 *   The function is called once the delay expires to properly calcualate   *
 *   a new rate															   *
 ***************************************************************************/
void Inj_rate_recalc_from_delay(byte arm, int inj, struct run_injector *prInj)
{
	double vol_pace_inj;
	double old_target_on_vol;
	float new_rate;
	float adj_rate;
	float total_meter_blend_pct[MAX_METERS];
	struct s_recipe_params *rcp_ptr;
	struct s_injector *inj_ptr;
	byte i;
	byte mtr_plumb;
	byte prd;

	mtr_plumb = pDB.add_inj.inj[inj].plumbing;
	rcp_ptr = &pDB.recipe[rDB.arm[arm].arm.cur_recipe];
	inj_ptr = &pDB.add_inj.inj[inj];
	/*determine the product amount pacing this injector*/
	vol_pace_inj = 0.0;
	switch(pDB.arm[arm].arm_config)
	{
	case RATIO_BLENDER:
	case SIDE_STREAM:

		if((rcp_ptr->ratio_seq_mode == SUCCESSIVE) && (pDB.arm[arm].arm_config == RATIO_BLENDER))
		{
			/*arm is plumbed in a ratio manner, but products deliver in a sequential manner*/
			for(i=0; i<MAX_SEQ_COMPS; i++)
			{
				if(rcp_ptr->blend_comp[i] == NO_COMP)
					continue;
				total_meter_blend_pct[rcp_ptr->blend_comp[i] - 1] += rcp_ptr->blend_pct[i];
			}
		}
		else
		{
			/*standard ratio blending where all products flow simultaneously*/
			for(i=0; i<MAX_METERS; i++)
				total_meter_blend_pct[i] = rcp_ptr->blend_pct[i];
		}

		for(i=0; i<pDB.arm[arm].arm_product; i++)
		{
			/*if the injector is plumbed and paced by this meter account for the volume to pass through this mtr*/
			if(mtr_plumb & (1 << i))
			{
				vol_pace_inj += total_meter_blend_pct[i] * rDB.arm[arm].arm.preset_vol * .01;
				if(ArmCleanPrd[arm] == i)
					vol_pace_inj += pDB.arm[arm].clean_volume;
				if(rcp_ptr->clean_deduct_prod == i)
					vol_pace_inj -= pDB.arm[arm].clean_volume;
			}

			/*if inj is downstream and paced by a product, its like being plumbed to the product*/
			else if((inj_ptr->up_or_down == DOWNSTREAM_INJ) && (rcp_ptr->inj_prods[inj] & (1<<i)))
			{
				vol_pace_inj += total_meter_blend_pct[i] * rDB.arm[arm].arm.preset_vol * .01;
				if(ArmCleanPrd[arm] == i)
					vol_pace_inj += pDB.arm[arm].clean_volume;
				if(rcp_ptr->clean_deduct_prod == i)
					vol_pace_inj -= pDB.arm[arm].clean_volume;
			}

		}
		break;

	case STRAIGHT_PROD:
	case STRAIGHT_WITH_VRS:
		vol_pace_inj = rDB.arm[arm].arm.preset_vol;
		break;

	case SEQ_BLENDER:
		/*all prds flow through one meter, so just see if product paces additive*/
		for(i=0; i<MAX_SEQ_COMPS; i++)
		{
			if((rcp_ptr->blend_comp[i] == NO_COMP) || (rcp_ptr->blend_pct[i] == 0.0))
				break;
			/*see if product paces additive*/
			prd = rcp_ptr->blend_comp[i]-1;
			if(rcp_ptr->inj_prods[inj] & (1<<prd))
				vol_pace_inj += rDB.arm[arm].arm.seq_preset[i];
			if(ArmCleanPrd[arm] == prd)
				vol_pace_inj += pDB.arm[arm].clean_volume;
			if(rcp_ptr->clean_deduct_prod == prd)
				vol_pace_inj -= pDB.arm[arm].clean_volume;
		}
		break;

	case HYBRID_BLENDER:
		for(i=0; i<pDB.arm[arm].num_ratio_prds; i++)
		{
			/*if the injector is plumbed and paced by this meter account for the volume to pass through this mtr*/
			if(mtr_plumb & (1 << i))
			{
				vol_pace_inj += rcp_ptr->blend_pct[i] * rDB.arm[arm].arm.preset_vol * .01;
				if(ArmCleanPrd[arm] == i)
					vol_pace_inj += pDB.arm[arm].clean_volume;
				if(rcp_ptr->clean_deduct_prod == i)
					vol_pace_inj -= pDB.arm[arm].clean_volume;
			}
			/*if inj is downstream and paced by a product, its like being plumbed to the product*/
			else if((inj_ptr->up_or_down == DOWNSTREAM_INJ) && (rcp_ptr->inj_prods[inj] & (1<<i)))
			{
				vol_pace_inj += rcp_ptr->blend_pct[i] * rDB.arm[arm].arm.preset_vol * .01;
				if(ArmCleanPrd[arm] == i)
					vol_pace_inj += pDB.arm[arm].clean_volume;
				if(rcp_ptr->clean_deduct_prod == i)
					vol_pace_inj -= pDB.arm[arm].clean_volume;
			}
		}
		for(i=pDB.arm[arm].num_ratio_prds; i<MAX_SEQ_COMPS; i++)
		{
			if((rcp_ptr->blend_comp[i] == NO_COMP) || (rcp_ptr->blend_pct[i] == 0.0))
				break;
			/*see if product paces additive*/
			prd = rcp_ptr->blend_comp[i]-1;
			if(rcp_ptr->inj_prods[inj] & (1<<prd))
				vol_pace_inj += rDB.arm[arm].arm.seq_preset[i];
			if(ArmCleanPrd[arm] == prd)
				vol_pace_inj += pDB.arm[arm].clean_volume;
			if(rcp_ptr->clean_deduct_prod == prd)
				vol_pace_inj -= pDB.arm[arm].clean_volume;
		}
		break;

	default: break;
	}

	/*note: In the future, if this feature is needed for low flow start always, after every stop/start sequence
	 in batch you could look at prInj->on_off to determin how many injections did occur and
	 base a new vol_per_inj factor from that*/
	/*old_target_on_vol represents value which caused this injection sequence to trigger*/  
	old_target_on_vol = prInj->target_vol_on - prInj->vol_per_inj;
	if(vol_pace_inj > old_target_on_vol)
	{
		/*calculate new injection rate*/ 
		new_rate = ((vol_pace_inj - old_target_on_vol)/vol_pace_inj) * prInj->vol_per_inj;
		//adj_rate = new_rate * (pDB.add_inj.inj_rate_pct/100);
		adj_rate = new_rate/2;
		prInj->vol_per_inj = new_rate;
		/*set when the next injection (after this current one) should occur*/
		prInj->target_vol_on = old_target_on_vol + new_rate;
		/*set when the this current injection sequence will end*/
		prInj->target_vol_off = old_target_on_vol + adj_rate;
		/*indicate that a recalc value was calculated*/
		InjRateRecalcDueToDelay[inj] = FALSE;

	}
}

