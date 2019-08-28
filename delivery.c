/*  DELIVERY.C  delivery control and state definitions  */
/*  Copyright 1998 by FMC - Smith Meter */
/*  All Rights Reserved */
/*  Written by Doug Sutter, Oct 1998 */
 

#include "options.h"    /* PCEMUL */
#include "assert_x.h"   /* ASSERT macro */
ASSERTFILE(__FILE__)    /* filename used by ASSERT */
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "fcdi_key.h"
#include "menumgr.h"
#include "literals.h"
#include "stamgr.h"
#include "vlcalc.h"
#include "io_task.h"
#include "eventlog.h"
#include "datalog.h"
#include "add_inj.h"
#include "ei_di_in.h"
#include "datetime.h"
#include "alarms.h"
#include "report1.h"
#include "flowcntl.h"
#include "cvtdate.h"
#include "automate.h"
#include "file.h"

#pragma sep_on class pf_saved
byte Starting_batch[MAX_LOAD_ARMS]; 
byte Ending_transaction[MAX_LOAD_ARMS];
byte Starting_transaction[MAX_LOAD_ARMS];

extern unsigned char ArmFlowState[MAX_LOAD_ARMS]; 
#pragma sep_off


extern unsigned long sec_ticks;
extern unsigned long ten_ms_ticks;
extern unsigned long date_time_sec_ticks;

/*************************************************************************
*                START BATCH
**************************************************************************/
unsigned long tran_start_time_ticks;

void start_batch(byte arm)
{

	struct time_tm cur_time;
	struct event_log_data data;
	enum event_log_error event_error;
	enum data_log_error data_error;
	unsigned int trans_no;
	byte i,j;
	
	/* insure valid recipe has been selected */
	if (  (Preset_recipe[arm] == 0) || (Preset_recipe[arm] > MAX_RECIPES) ||
		  (pDB.recipe[Preset_recipe[arm]-1].recipe_used != (arm+1) ) )
		return;

	rDB.arm[arm].batch_done = FALSE;

	/* now we are committed to selected recipe */
	rDB.arm[arm].cur_recipe = Preset_recipe[arm] - 1;


	/* Setup for new transaction */
	rDB.arm[arm].transaction_done = FALSE;

	/* increment transaction # */
	trans_no = rDB.arm[arm].tran_hdr.trans_no + 1;
	if (trans_no > 9999)
		trans_no = 1;

	/* clear out transaction & batch report alarm log */
	clear_rpt_alarm_log(arm);

	/* save time transaction was started */
	DISABLE();
	cur_time.tm_isdst = STANDARD_TIME;
	systime2date(date_time_sec_ticks, &cur_time);
	tran_start_time_ticks = date_time_sec_ticks;
	ENABLE();

	rDB.arm[arm].start_year  = cur_time.tm_yr;
	rDB.arm[arm].start_month = cur_time.tm_mon;
	rDB.arm[arm].start_day   = cur_time.tm_day;
	rDB.arm[arm].start_wday  = cur_time.tm_wday;
	rDB.arm[arm].start_sec   = cur_time.tm_sec;
	rDB.arm[arm].start_min   = cur_time.tm_min;
	rDB.arm[arm].start_hour  = cur_time.tm_hr;

	date_time_string(rDB.arm[arm].tran_hdr.tran_start_time, tran_start_time_ticks);

	/* log transaction started event */
	sprintf(data.text,"%.21s\t%.21s\t%.21s%d", litptr[transaction_started_lit],
					  pDB.arm[arm].load_arm_id, 
					  litptr[trans_num_lit], trans_no);
	event_log_store(EVENT_TRANS_STARTED, &data, &event_error);

	/* reset batch # (do now for init_vlcalc) */
	rDB.arm[arm].batch_no = 0;
	rDB.arm[arm].tran_ftr.total_batches = 0;

	/* save prompt responses */
	for (i=0; i<MAX_PROMPTS; i++)
	{
		rDB.arm[arm].tran_hdr.prompt_response[i] = rDB.arm[arm].prompt_response[i];
		for (j=0; j<=ALPHA_PROMPT_SIZE; j++)
			rDB.arm[arm].tran_hdr.alpha_prompt[i][j] = Alpha_response[arm][i][j];
	}

	/* Initialize the original density and bsw and recalc flags to indicate this */
	/* batch has not been recalculated */
	rDB.arm[arm].tran_ftr.orig_bsw = 0;
	rDB.arm[arm].tran_ftr.orig_ref_den = 0;
	rDB.arm[arm].tran_ftr.den_recalc_flag = FALSE;
	rDB.arm[arm].tran_ftr.bsw_recalc_flag = FALSE;
	

	/* clear transaction and batch volumes and load averages, setup flow profile */
	init_vlcalc(arm, START_TRANSACTION);

	DISABLE_PWRDWN();
	rDB.arm[arm].tran_hdr.trans_no = trans_no;
	rDB.arm[arm].transaction_in_progress = TRUE;
	rDB.arm[arm].batch_status = BATCH_FLOW_IN_PROGRESS;
	Starting_transaction[arm] = TRUE;
	ENABLE_PWRDWN();

		
	rDB.arm[arm].batch[0].load_arm = arm+1;

	/* set additive mask to indicate which injectors are being used in this batch */
	DISABLE_PWRDWN();
	rDB.arm[arm].batch[rDB.arm[arm].batch_no].additive_mask = 0;
	for (i=0; i<MAX_INJECTORS; i++)
		if ((pDB.add_inj.inj[i].arm == arm) && (rDB.add_inj.inj[i].on_off == INJ_ON))
			rDB.arm[arm].batch[rDB.arm[arm].batch_no].additive_mask |= ((unsigned long)0x01 << i);
	ENABLE_PWRDWN();
							
	/* indicate flow valve is commanded to open */ 
	rDB.arm[arm].accuload_released = TRUE;

	Starting_batch[arm] = FALSE;
	Starting_transaction[arm] = FALSE;
}



			
/*************************************************************************
*    STOP BATCH - via stop key, remote stop input, permissive, alarm, host
**************************************************************************/
void stop_batch(byte arm)
{
	turn_pump_off_after_delay(arm);

	if (rDB.arm[arm].batch_status == BATCH_FLOW_IN_PROGRESS)
	{
		rDB.arm[arm].batch_status = BATCH_STOPPED;

		/* indicate flow valve has been commanded to close */
		rDB.arm[arm].accuload_released = FALSE;
					     
	}

}


/*************************************************************************
*                END BATCH
**************************************************************************/
void end_batch(byte arm)
{

	/* indicate flow valve has been closed */
	rDB.arm[arm].accuload_released = FALSE;

	/* clear just in case we were waiting for valve to open */
	ArmState[arm].batch_presetting = FALSE;

	turn_pump_off_after_delay(arm);


	/* end_batch() could be called by EB command at start of 1st batch during valve delay */
	/*     so we want to cancel the pending batch, but the batch hasn't actually started */
	if (rDB.arm[arm].batch_status != BATCH_NOT_IN_PROGRESS)
	{
		/* force zoom to reset to split screen at end of batch */
		Zoom_ticks = 0;

	}

	DISABLE_PWRDWN();

	rDB.arm[arm].batch_status = BATCH_NOT_IN_PROGRESS;

	/* don't double increment total_batches */
	rDB.arm[arm].batch_done = TRUE;
	rDB.arm[arm].tran_ftr.total_batches++;

	
	/* clear in preparation for next batch */
	Entered_preset[arm] = 0;
	Preset_locked[arm] = FALSE;

	/* if in REMOTE_CONTROL, remove authorization after each batch */
	if ((rDB.host_control == HOST_CONTROL) && !rDB.arm[arm].trans_authorized)
	{
		rDB.arm[arm].accuload_authorized = FALSE;     
		rDB.arm[arm].auth_max_batch_vol = 0;
	}

	ENABLE_PWRDWN();

}



/*************************************************************************
*          END TRANSACTION
**************************************************************************/
void end_transaction(byte arm)
{

	enum event_log_error event_error;
	enum data_log_error data_error;
	struct event_log_data data;
	struct time_tm cur_time;
	unsigned long seq_no;
	byte mtr;


	/* clear this flag always.  may have been presetting on arm and permissive was not met but */
	/*    transaction hadn't been started */
	rDB.arm[arm].permissive_not_met = FALSE;

	if (!rDB.arm[arm].transaction_in_progress)
		return;


	/* end_transaction() can be called without calling end_batch() as long as */
	/*   	 flow has stopped. if batch is still in progress, first end the batch. */
	end_batch(arm);

	DISABLE_PWRDWN();
	/* increment batch # to indicate # of batches run */
	rDB.arm[arm].batch_no++;

	/* set flag in case we loose power before we are finished */
	Ending_transaction[arm] = TRUE;
	ENABLE_PWRDWN();


	/* clear transaction variables/flags */
	rDB.arm[arm].transaction_done = TRUE;
	rDB.arm[arm].auth_max_trans_vol = 0;

	/* clear just in case we were waiting for valve to open */
	ArmState[arm].batch_presetting = FALSE;
	rDB.arm[arm].permissive_not_met = FALSE;

	/* restore allocated recipes (AB command) to recipes defined in program mode */
	rDB.arm[arm].recipe_mask_A = pDB.arm[arm].recipe_mask_A;
	rDB.arm[arm].recipe_mask_B = pDB.arm[arm].recipe_mask_B;

	rDB.arm[arm].accuload_authorized = FALSE;
	rDB.arm[arm].injectors_authorized = FALSE;
	rDB.arm[arm].trans_authorized = FALSE;

	/* clear batch variables/flags */
	rDB.arm[arm].batch_done = TRUE;
	rDB.arm[arm].auth_max_batch_vol = 0;
	Entered_preset[arm] = 0;
	Preset_locked[arm] = 0;


	/* save time transaction was ended - both formats are needed - convert date/time ticks into date/time string */
	DISABLE();
	cur_time.tm_isdst = STANDARD_TIME;
	systime2date(date_time_sec_ticks, &cur_time);
	rDB.arm[arm].tran_ftr.tran_end_time_ticks = date_time_sec_ticks;
	ENABLE();

    rDB.arm[arm].end_year  = cur_time.tm_yr;
    rDB.arm[arm].end_month = cur_time.tm_mon;
    rDB.arm[arm].end_day   = cur_time.tm_day;
	rDB.arm[arm].end_wday  = cur_time.tm_wday;
    rDB.arm[arm].end_sec   = cur_time.tm_sec;
    rDB.arm[arm].end_min   = cur_time.tm_min;
    rDB.arm[arm].end_hour  = cur_time.tm_hr;

	date_time_string(rDB.arm[arm].tran_ftr.tran_end_time, rDB.arm[arm].tran_ftr.tran_end_time_ticks);

	/* stop updating transaction volumes */
	end_vlcalc_transaction(arm);

	/*reset dual pulse counters if applicable*/
	for (mtr=0; mtr<MAX_METERS; mtr++)
		if((pDB.arm[arm].mtr[mtr].dp_error_reset == TRANSACTION_END) || (pDB.arm[arm].mtr[mtr].dp_error_reset == TRANSACTION_END_AND_POWERUP))
			DualPulseErrorCounts[arm][mtr] = 0;

	/* log transaction ended event */
	sprintf(data.text,"%.21s\t%.21s\t%.15s%d", litptr[transaction_ended_lit], 
				  		pDB.arm[arm].load_arm_id,
				  		litptr[trans_num_lit], rDB.arm[arm].tran_hdr.trans_no);
	event_log_store(EVENT_TRANS_ENDED, &data, &event_error);


	/* save transaction header in flash */
	archive_transaction_header(NULL, arm, &data_error);

	/* save batch in flash */
  	archive_batch_data(NULL, arm, rDB.arm[arm].batch_no-1, &data_error);

	/* save transaction in flash */
	archive_transaction_trailer(NULL, arm, &data_error);

	DISABLE_PWRDWN();
	rDB.arm[arm].transaction_in_progress = FALSE; /* Clear this flag when we are all done!! */
	Ending_transaction[arm] = FALSE;
	ENABLE_PWRDWN();


 /**********************************************************************************************
 CAUTION:
		Place stuff that should be completed on powerup in case we loose power before 
	finishing, above this point.  If power is lost before Ending_transaction is set
	false, end_transaction() will be called again on powerup                             
 ***********************************************************************************************/

	/* kick off transaction report, if printers are not busy */
	if (rDB.printer_1_in_use || rDB.printer_2_in_use || rDB.report_being_processed)
		rDB.arm[arm].trans_rpt_queued = TRUE;
	else
	{
		seq_no = 0;
		rDB.report_being_processed = TRUE;
		rDB.rpt_arm = arm;								/* current arm being printed */
		init_prn_task(arm,
				  	  TRANSACTION_REPORT,				/* rpt_id = transaction */
			      	  pDB.arm[arm].report_sel + 1, 		/* default = 1, user = 2 */
			      	  &seq_no, &seq_no);  				/* current transaction */
	}


}

/*************************************************************************
*                DELIVERY STATE
**************************************************************************/
#pragma sep_on
extern MENU_PAGE 			ConfigDispPage[];
#pragma sep_off



void update_delivery_status(char *dest, byte arm);


/*************************************************************************
*          DELIVERY CONTROL
*	
*	allows START and STOP to be used from dynamic displays
**************************************************************************/
enum delivery_status delivery_control(byte event, byte arm)
{
	enum preset_error error;

	switch (event)
	{
		case START:
		case HOST_START:

			/* don't momentarily start pump if digital remote stop is active */
			if (remote_stop_active(arm))
				break;

			/* don't allow local start if keypad and display is being used by */
			/*    automation system */ 
			if ((event == START) && (ArmState[arm].state_ptr == write_display_state))
				return(EVENT_NOT_USED);

			/* don't allow local start (key or digital input) if not programmed */
			if ((event == START) && !pDB.trans_term)
				return(EVENT_NOT_USED);

			/* Rev 0.02 don't allow starting until high flow rate is entered */
		   	if ((pDB.arm[arm].prd[0].hi_flow_rate == 0)  &&
		   	    (rDB.arm[arm].batch_status == BATCH_NOT_IN_PROGRESS))
				return(EVENT_NOT_USED);

			/* if batch hasn't been started yet, verify we have a valid preset */
			if (rDB.arm[arm].batch_status == BATCH_NOT_IN_PROGRESS) 
			{
				/* don't allow starting if we haven't made it all the way thru the preset */
				/*   sequence.  NOTE: could have selected recipe and entered a preset volume */
				/*   and then get an alarm during valve delay.  After alarm is cleared, we are */
				/*   at ready screen and without these checks the start key could be pressed */
				/*   from the ready screen and the batch would be started */
				if (!ArmState[arm].batch_presetting)
					return(EVENT_NOT_USED);
				else if (
						 (ArmState[arm].state_ptr != check_permissives_state) &&
						 (ArmState[arm].state_ptr != enter_hi_flow_rate) &&
						  !ArmState[arm].at_dyn_disp)
					return(EVENT_NOT_USED);


				/* has recipe been selected? It's possible to press START key while */
				/*     at recipe prompt before recipe has been selected */
				if (Preset_recipe[arm] == 0)
					return(EVENT_NOT_USED);

				setup_batch_preset(Entered_preset[arm], arm, &error);
				if (error != PRESET_OKAY)
					return(EVENT_NOT_USED);
			}		   



			return(DS_BATCH_STARTED);


		case STOP_KEY:
		case STOP_ARM:
		case STOP_ALL_ARMS:

			return(DS_BATCH_STOPPED);
				


		case BATCH_COMPLETE:
			/* final trip has been reached, end batch now */
			/*    NOTE: vlcalc could have queued up 2 BATCH_COMPLETEs before stamgr processed the 1st one */
			/*     so ignore the 2nd one (else if SB already received, could clear authorized flag)	*/
			if (rDB.arm[arm].batch_status != BATCH_NOT_IN_PROGRESS)
				end_batch(arm);

			return(DS_BATCH_STOPPED);

	}
	return(EVENT_NOT_USED);
}




/*************************************************************************
*       ALL PERMISSIVES OK? 
*			use when: 
*				Resetting batch
**************************************************************************/
byte all_permissives_ok(byte arm, char **perm_msg, byte *perm_start)
{
	static byte last_perm_start[MAX_LOAD_ARMS];
	byte i;


	// check arm-specific permissives
	for (i=0; i<MAX_PERMISSIVES; i++)
	{
		switch (pDB.arm[arm].permissive_type[i])
		{
			/* is permissive checked at batch reset only? */
			case PERM_BATCH_RESET:
				if (!permissive_met(arm, i))
				{
					*perm_msg = pDB.arm[arm].permissive_msg[i];
					return(FALSE);
				}
				break;

			case PERM_BATCH_RESET_FLOW:    /* is permissive checked all the time? */
				if (!permissive_met(arm, i))
				{
					*perm_msg = pDB.arm[arm].permissive_msg[i];
					return(FALSE);
				}
				break;

		}
	}

	*perm_start = last_perm_start[arm];
	return(TRUE);
}



byte permissive_met(byte arm, byte perm_index)
{
	byte io_pt;

	if (perm_index == 0)
		io_pt = pDB.permissive1_io_pt[arm];
	else
		io_pt = pDB.permissive2_io_pt[arm];

	if (io_pt != NOT_ASSIGNED)
		if (!rDB.dig[io_pt-1].state)
			return FALSE;

	return TRUE;
}





/*************************************************************************
*		CHECK PERMISSIVE STATE	at start of transaction or batch
**************************************************************************/	
enum {PERM_MSG_1,
	  PERM_MSG_2};

void *check_permissives_state(byte key, byte arm, byte init)
{
	static char *perm_msg[MAX_LOAD_ARMS];
	byte perm_start;
	byte perms_ok;


	const static MENU_ITEM connect_permissive_list[]=
	{
		/*DYNAMIC|TEXT with VAR_LIT causes this state to be executed once per second */
		/*    needed to check if permissive has been met */
		{ROW(1),COL(1),SYSTEM_FONT,WHITE,"%s",TEXT|DYNAMIC,0,0,VAR_LIT,0,0,0,
			&p_null_string,0,0},

		/* NOTE: permissive message is word wrapped into var_lit[0] and [1] */
		{ROW(4),COL(1),SYSTEM_FONT,WHITE,ENDPT(ROW(4),COL(22)),DYNAMIC|TEXT,0,0,
			VAR_LIT|CENTER,0,SYSTEM,0,&var_litptr[PERM_MSG_1],0,0},

		{ROW(5),COL(1),SYSTEM_FONT,WHITE,ENDPT(ROW(5),COL(22)),DYNAMIC|TEXT,0,0,
			VAR_LIT|CENTER,0,SYSTEM,0,&var_litptr[PERM_MSG_2],0,0}

	};

	const static MENU_PAGE menu_pages[]=
		{MENU_LIST(connect_permissive_list)};

	const static MENU_INFO menu_info=
	{
		check_permissives_state,
		(MENU_PAGE *)menu_pages,
		NUM_PAGES(menu_pages)
	};


	if (init == TRUE)
	{
		var_lit[PERM_MSG_1][0] = var_lit[PERM_MSG_2][0] = 0;

		/* check if all permissives are ok */
		perms_ok = all_permissives_ok(arm, &perm_msg[arm], &perm_start);
		rDB.arm[arm].permissive_not_met = (perms_ok) ? (FALSE) : (TRUE);

		if (perms_ok)
		{
			ResetBatch(Preset_recipe[arm]);
			return(ready_state);
		}
		else
		{
			word_wrap(perm_msg[arm],LINE_LENGTH-1,var_lit[0],LINE_LENGTH+1);

			build_display(&menu_info,arm,NULL,NULL);

		}
	}
	else
	{
		switch(key)
		{

			case ENTER:
				rDB.arm[arm].permissive_not_met = FALSE; // START will have to be pressed again anyway
			    return(dynamic_display_select);


			case CLEAR:
			case STOP_KEY:
			case STOP_ARM:
			case STOP_ALL_ARMS:
				rDB.arm[arm].permissive_not_met = FALSE; // START will have to be pressed again anyway
				/* if presetting batch, return to preset volume prompt */
				return(ready_state);

				break;


/*			case PRINT:
				
				rDB.arm[arm].permissive_not_met = FALSE;
				if (rDB.arm[arm].cur_frate != 0)  
					return(wait_for_zero_flow);
				else
				{
					if (rDB.arm[arm].transaction_in_progress)
						end_transaction(arm);
				
					return(ready_state);
				}
				break;
*/

/*			case START:
			case HOST_START:

				
				if (all_permissives_ok(arm, &perm_msg[arm], &perm_start))
				{
					rDB.arm[arm].permissive_not_met = FALSE;

					return(ready_state);

				}
				break;

			case BATCH_COMPLETE:
				rDB.arm[arm].permissive_not_met = FALSE;
				return(ready_state);
*/
			case RE_INIT:

				var_lit[0][0] = var_lit[1][0] = 0;

				/* if this permissive is now ok, check if there are any more not met */
				if (all_permissives_ok(arm, &perm_msg[arm], &perm_start))
				{
					rDB.arm[arm].permissive_not_met = FALSE;

					ResetBatch(Preset_recipe[arm]);
					return(ready_state);
					
				}
				/* if another permissive is not met, display it's message */
				else
				{
					rDB.arm[arm].permissive_not_met = TRUE;
					word_wrap(perm_msg[arm],LINE_LENGTH-1,var_lit[0],LINE_LENGTH+1);
				}
				break;

		}
	}
	return(check_permissives_state);
}


/*************************************************************************
*          TURN PUMP ON/OFF
**************************************************************************/
void turn_pump_on(byte arm)
{
	byte mtr;

	for (mtr=0; mtr<MAX_METERS; mtr++)
	{
		if (pDB.pump_io_pt[arm][mtr] != NOT_ASSIGNED)
		{
			
			DigOut(pDB.pump_io_pt[arm][mtr],ON);
			rDB.arm[arm].pump_status = PUMP_ON;
		}
	}
}


void turn_pump_off(byte arm)
{
	byte mtr;
	
	for (mtr=0; mtr<MAX_METERS; mtr++)
	{
		if (pDB.pump_io_pt[arm][mtr] != NOT_ASSIGNED)
		{
			DigOut(pDB.pump_io_pt[arm][mtr],OFF);
			rDB.arm[arm].pump_status = PUMP_OFF;
		}
	}
}


/*************************************************************************
*          TURN PUMP OFF AFTER DELAY
**************************************************************************/
/* Routine is unused in the flow computer */

unsigned long Pump_delay_start_time[MAX_LOAD_ARMS];

/* check if pump delay timer has expired and it's time to turn pump off */
void check_pump_delay_off(byte arm)
{  
	byte elapsed_time;

	/* is pump delay off active */
	if (rDB.arm[arm].pump_status == PUMP_DELAY_OFF)
	{
		elapsed_time = (ten_ms_ticks - Pump_delay_start_time[arm])/100;
// TODO		if (elapsed_time >= pDB.arm[arm].pump_delay_off)
//			turn_pump_off(arm);
	}
	
}

/* set up pump delay to off timer */
void turn_pump_off_after_delay(byte arm)
{
	/* if no pump delay desired, turn off pump now */
// TODO	if (pDB.arm[arm].pump_delay_off == 0) 
//		turn_pump_off(arm);

	/* else setup pump delay timer */	   
/*	else */ if (rDB.arm[arm].pump_status == PUMP_ON)   
	{
		rDB.arm[arm].pump_status = PUMP_DELAY_OFF;
		Pump_delay_start_time[arm] = ten_ms_ticks;
	}		
}


/*************************************************************************
*                REMOTE STOP ACTIVE
**************************************************************************/
byte remote_stop_active(byte arm)
{

	byte remote_arm_stop = FALSE;
	byte remote_stop = FALSE;

	/* read remote stop (stops all arms) digital input */
	if (pDB.remote_stop_io_pt != DIG_NOT_ASSIGNED)
		remote_stop = rDB.dig[pDB.remote_stop_io_pt-1].state;

	/* read arm remote stop digital input */
	if (pDB.remote_stop_arm_io_pt[arm] != DIG_NOT_ASSIGNED)
		remote_arm_stop = rDB.dig[pDB.remote_stop_arm_io_pt[arm]-1].state;

	if ((remote_stop) || (remote_arm_stop))
		return(TRUE);

	return(FALSE);
}

/* This routine resets the batch. If the recipe passed is zero then the recipe for the new batch is the same as the */
/* one currently running. If the recipe passed is 1 through 4 then the next recipe will be set to zero through three */
/* respectively. */
void ResetBatch(int recipe)
{

	struct event_log_data event;
	enum event_log_error log_error;
		
	sprintf(event.text, "Batch Reset #%d", rDB.arm[0].batch[0].batch_no);  				// store one event 
	event_log_store(EVENT_POWER_DOWN, &event, &log_error);

	/* Reset the batch */
	end_transaction(0);
	/* If the recipe is non-zero, then set the requested recipe first */
	if ((recipe > 0) && ( recipe < 5 ))
	{
		rDB.arm[0].batch[0].recipe_no = recipe;
		rDB.arm[0].batch[0].batch_no = 1;
		Preset_recipe[0] = recipe;
	}
	add_inj_control();
	set_auto_inj(0);
	start_batch(0);
	ArmState[0].batch_presetting = FALSE;
}

/*************************************************************************
*                REMOTE START STOP MONITOR
* Re-worked into batch reset input monitor for the flow computer
**************************************************************************/
static unsigned int LastResetState, ResetStateInit;
void remote_start_stop_monitor(byte arm)
{

	/* If there's a transaction reset input defined and it transitions */
	/* from low to high, then reset the batch */
	if (pDB.xaction_reset_io_pt[arm] != DIG_NOT_ASSIGNED) /* Is  a batch reset input defined? */
	{
		if (!ResetStateInit) /* The first time through then just record the current state */
		{
			ResetStateInit = TRUE;
		}
		else /* We've been through here at least once */
		{
			if ((rDB.dig[pDB.xaction_reset_io_pt[arm]-1].state == 1) &&
				(LastResetState == 0))  /* Transition detected? */
			{
				/* Reset the batch */
				ResetBatch(0);
			}
		}
		/* Record the current state of the input for compare next time */
		LastResetState = rDB.dig[pDB.xaction_reset_io_pt[arm]-1].state;
	}
	else /* No batch reset input defined, clear the initialized flag */
	{
		ResetStateInit = 0;
	}
}

					


/*************************************************************************
*	   MAX BATCHES ALLOWED PROMPT 
**************************************************************************/
// TODO: This can be deleted
void *max_batches_prompt(byte key, byte arm, byte init)
{
		

	const static MENU_ITEM max_batches_list[]=
	{
		/*DYNAMIC|TEXT with VAR_LIT causes this state to be executed once per second */
		/*    needed to check if permissive has been met */
		{ROW(1),COL(1),SYSTEM_FONT,WHITE,"%s",TEXT|DYNAMIC,0,0,VAR_LIT,0,0,0,
			&p_null_string,0,0},

		{ROW(1),COL(1),SYSTEM_FONT,WHITE,ENDPT(ROW(7),COL(22)),STRING,0,0,
			DISP_ONLY|CENTER,0,0,0,&litptr[max_batches_allowed_lit],0,0},

		{ROW(8),COL(1),SYSTEM_FONT,WHITE,ENDPT(ROW(8),COL(22)),STRING,0,0,
			DISP_ONLY|CENTER,0,SYSTEM,0,&var_litptr[0],0,0},

	};

	const static MENU_PAGE menu_pages[]=
		{MENU_LIST(max_batches_list)};

	const static MENU_INFO menu_info=
	{
		max_batches_prompt,
		(MENU_PAGE *)menu_pages,
		NUM_PAGES(menu_pages)
	};


	if (init == TRUE)
	{
		/* if bays, we may be at batch limit yet not have started any batches on this arm */
		if (!rDB.arm[arm].transaction_in_progress)
			strcpy(var_litptr[0],litptr[press_clear_lit]);
		else
			var_lit[0][0] = 0;

		build_display(&menu_info,arm,NULL,NULL);

	}
	else
	{
		switch(key)
		{

			case CLEAR:
				return(prev_display());

			case PRINT:
				/* this prompt may be displayed for an idle arm, if no more batches are allowed on bay */
				if (!rDB.arm[arm].transaction_in_progress)
					break;

				if ((rDB.arm[arm].cur_frate == 0))
				{
					/* is print key allowed to end transaction?	*/
					/*    1) allow if print key is enabled 		*/
					/*    2) allow once if power cycled during transaction 	*/
					/*    3) allow if there is a comm error 	*/
// TODO: Remove this routine
/*					if ((pDB.trans_term == PRINT_KEY) || (Allow_print_key_one_time[arm]) ||
				    	(rDB.sys_alarm[comms_error]))
					{
						Allow_print_key_one_time[arm] = FALSE;
						end_transaction(arm);  */
						return(ready_state);
//					}
				}
				else
					return(wait_for_zero_flow);

				break;

			default:
//				if (pDB.trans_term == TICKET_TRAY_IN) 
//				{  
					/* return to ready_state when ticket is removed */
					/* NOTE: transaction is ended by ticket_tray_monitor */
// TODO					if ((rDB.arm[arm].cur_frate == 0) && (!rDB.dig[pDB.ticket_tray_io_pt[arm] - 1].state))
  						return(ready_state);
//				}
				break;

		}
	}
	return(max_batches_prompt);
}



/*************************************************************************
*           WAIT FOR ZERO FLOW
**************************************************************************/
void *wait_for_zero_flow(byte key, byte arm, byte init)
{
	static unsigned long message_ticks[MAX_LOAD_ARMS];
	static byte message_flash[MAX_LOAD_ARMS];

	const static MENU_ITEM wait_for_zero_flow_list[]=
	{

		{ROW(4),COL(1),SYSTEM_FONT,WHITE,ENDPT(ROW(4),COL(22)),STRING,
			0,0,DISP_ONLY|CENTER,0,0,0,&litptr[waiting_zero_flow_lit],0,0},

		/*DYNAMIC|TEXT with VAR_LIT causes this state to be executed once per second */
		/*    needed to check flow rate */
		{ROW(1),COL(1),SYSTEM_FONT,BLACK,"%s",DYNAMIC|TEXT,0,0,VAR_LIT,0,0,0,&litptr[mtr_lit],0,0},

	};

	const static MENU_PAGE wait_for_zero_flow_pages[]=
		{MENU_LIST(wait_for_zero_flow_list)};

	const static MENU_INFO wait_for_zero_flow_info=
	{
		wait_for_zero_flow,
		(MENU_PAGE *)wait_for_zero_flow_pages,
		NUM_PAGES(wait_for_zero_flow_pages)
	};


	(void)key;

	if ((rDB.arm[arm].cur_frate == 0))
	{	
		/* if transaction is in progress, end the transaction */
		/*     	this fcn verifies no other arms on the bay are in valve opening delay */
		/* 		NOTE: OK_to_end_trans  returns false if transaction is already ended */
		if (OK_to_end_transaction(arm))
			end_transaction(arm);

		/* in case transaction is ended remotely */
		if (!rDB.arm[arm].transaction_in_progress)
			return(ready_state);

	}
	else if (init == TRUE)
	{
		build_display(&wait_for_zero_flow_info,arm,NULL,NULL);

		message_flash[arm] = WHITE;
		message_ticks[arm] = ten_ms_ticks;
	}
	else if ((ten_ms_ticks - message_ticks[arm]) >= 100)
	{
		message_flash[arm] = (message_flash[arm] == BLACK) ? WHITE:BLACK;
		message_ticks[arm] = ten_ms_ticks;

		change_attrib(NULL,&litptr[waiting_zero_flow_lit],message_flash[arm],1);
	}

	return(wait_for_zero_flow);
}


/**************************************************************************
*  		VALVE FAULT MONITOR
**************************************************************************/
enum vf_alarm_state {
	VF_ALARM_OK,
	VF_ALARM_DELAY
};


void valve_fault_monitor(byte arm, byte mtr)
{

	static enum vf_alarm_state vf_alarm_state[MAX_LOAD_ARMS][MAX_METERS];
    static unsigned long vf_alarm_time[MAX_LOAD_ARMS][MAX_METERS];
	float flow_rate;
	byte valve_closed;

	/* if valve fault alarm is not enabled, exit now */
	if (pDB.arm[arm].valve_fault_timeout == 0)
		return;

	 if (mtr != 0)
		return;			/* meter doesn't exist */

	/* get current flow rate */
	flow_rate = rDB.arm[arm].cur_frate;	

	valve_closed = (rDB.arm[arm].accuload_released) ? FALSE:TRUE;

	/* check for valve fault alarm (valve is commanded closed, but there is flow present */
	/*		for longer than programmed valve fault timeout (in secs) */
	switch (vf_alarm_state[arm][mtr])
	{
		case VF_ALARM_OK:
			/* is valve closed with flow? */
			if (valve_closed && (flow_rate > 0))
			{
				/* if so, save current time and wait vf delay time before alarming */
				vf_alarm_state[arm][mtr] = VF_ALARM_DELAY;
				vf_alarm_time[arm][mtr] = sec_ticks;
			}
			break;

		case VF_ALARM_DELAY:
			/* first check if valve position and flow rate are correct */
			if (!valve_closed || (flow_rate == 0))
			{
				/* if so, go back to checking for illegal conditions */
				vf_alarm_state[arm][mtr] = VF_ALARM_OK;
			}
			
			/* check if vf time delay has expired */
			if ((sec_ticks - vf_alarm_time[arm][mtr]) >= pDB.arm[arm].valve_fault_timeout)
			{
				/* if so, set vf alarm */
				set_meter_alarm(valve_fault,arm,mtr);

				/* wait for vf time delay before setting alarm again */
				vf_alarm_state[arm][mtr] = VF_ALARM_OK;
			}

			break;
	}
}				



/*************************************************************************
*	OK to end transaction?
* 		requires valve to be closed but not zero flow 
**************************************************************************/
byte OK_to_end_transaction(byte arm)
{

	/* if arm is independent, check if valve closed on this arm only */
		/* if transaction in progress and valve is closed, then end transaction */
	if (rDB.arm[arm].transaction_in_progress && !rDB.arm[arm].accuload_released)
		return(TRUE);
	else
		return(FALSE);
}


