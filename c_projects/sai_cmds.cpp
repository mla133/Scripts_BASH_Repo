/*********************************************************************************
*                 Smart Additive Injector Protocols / Command Sets               *
*                               (sai_cmds.c)                                     *
*   -For the Accuload III.                                                       *
*   -Michael Becker                                                              *
*                                                                                *
*   This file contains the text strings as well as the specific fcns used to     *
*   implement the various Smart Additive Injector command sets (currently Titan  *
*   and Gate City).                                                              *
*                                                                                *
*   Functions Included In This File:                                             *
*           - SAI_type_find                                                      *
*           - II_SAI                                                             *
*           - Authorize_SAI                                                      *
*           - DeAuthorize_SAI                                                    *
*           - SetVol_SAI                                                         *
*           - ClearAlarms_SAI                                                    *
*           - SetVolPerCycle_SAI                                                 *
*                                                                                *
*   Initial Editing/Creation Date: 11/10/98                                      *
*********************************************************************************/

#include "options.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "database.h"
#include "comdrv.h"
#include "comm_inj.h"
#include "sai_cmds.h"
#include "add_inj.h"
#include <syslog.h>

//TODO: #pragma sep_on class pf_saved
extern unsigned char SmartInjTotalsStatus[MAX_SMART_INJECTORS];
//TODO: #pragma sep_off

// Enable injection pacing/volumes
#define DEBUG_INJ_VOL
#ifdef DEBUG_INJ_VOL
extern double CurBatchVol[MAX_INJECTORS];
#endif

// Enable All other injector commands
//#define DEBUG_CMDS

extern enum OTF_inj_states OTF_InjState[MAX_INJECTORS];

const char *SAI_command_table [NUMBER_SAI_COMMANDS][NUMBER_SAI_TYPES] = 
{                             
/* ---------------------   */ /* ----------- ----------- ---------- ----------- */
/* ---------------------   */ /* TITAN       BLEND-PAK   MINI-PAK	ADD-PACK    */
/* ---------------------   */ /* ----------- ----------- ---------- ----------  */
/*  II                     */{   "BI 001",   "EX 050",   "EX 050",	"IN"    	},
/*  AUTHORIZE              */{   "AL 001",   "EX 010",   "EX 010",	"EP"    	},
/*  POLL_TOTALS_AND_ALARMS */{   "ls 001",   NULL,       NULL,	    "TS"    	},
/*  POLL_TOTALS            */{   "at 001",   "RV 860",   "RV 850",	"TL"    	},
/*  POLL_ALARMS            */{   "ac 001",   "RV 802",   "RV 802",	"ST"    	},
/*  DEAUTHORIZE            */{   "UL 001",   "EX 001",   "EX 001",	"DP"    	},
/*  SET_VOL_PER_INJ        */{   "PS 001",   "WV 020",   "WV 020",	 NULL   	},
/*  SET_VOL_PER_CYCLE      */{   "AS 001",   "WV 010",   "WV 010",	"PW 30" 	},
/*  CLEAR_ALARMS           */{   "AC 001",   "EX 301",   "EX 301",	"CA"    	},
/*	SET_K_FACTOR	   	   */{	 NULL,		 NULL,		 NULL,		"PW 10" 	},
/*	SET_MTR_FACTOR		   */{	 NULL,		 NULL,		 NULL,		"PW 11"		},
/*	SET_HI_TOL			   */{	 NULL,		 NULL,		 NULL,		"PW 20"		},
/*	SET_LO_TOL			   */{	 NULL,		 NULL,		 NULL,		"PW 21"		},
/*	SET_MAX_ERRS		   */{	 NULL,		 NULL,		 NULL,		"PW 22"		},
/*	SET_CONV_FACTOR	       */{	 NULL,		 NULL,		 NULL,		"PW 23"		},
/*	SET_ALARM_PULSE_COUNT  */{	 NULL,		 NULL,		 NULL,		"PW 24"		},/*added for rev 10.15*/
/*	SET_ALARM_PULSE_TIME   */{	 NULL,		 NULL,		 NULL,		"PW 25"		},/*added for rev 10.15*/			
/*	SET_OUTPUT_STATE	   */{	 NULL,		 NULL,		 NULL,		"SO"		},
/*	RESET_PULSE_COUNT	   */{	 NULL,		 NULL,		 NULL,		"RC"		},
/*	READ_PULSE_COUNT	   */{	 NULL,		 NULL,		 NULL,		"PC"		},
/*	READ_OUTPUT_STATE	   */{	 NULL,		 NULL,		 NULL,		"OS"		},
/*	INITIALIZE			   */{	 NULL,		 NULL,		 NULL,		"IZ"		},
/*	SOFTWARE_VERSION	   */{	 NULL,		 NULL,		 NULL,		"SV"		},
/*	AUTHORIZE_IO	 	   */{	 NULL,		 NULL,		 NULL,		"AI"		},
/*	DEAUTHORIZE_IO	 	   */{	 NULL,		 NULL,		 NULL,		"DI"		},
/*	SET_OR_GET_IO	 	   */{	 NULL,		 NULL,		 NULL,		"IO"		},
/*  SET_CONTROL_METHOD	   */{	 NULL,		 NULL,		 NULL,		"PW 26"		},//added after rev 11.03 on the AIII.net
/*  SET_MTR_INJ_IO_PT      */{   NULL,		 NULL,		 NULL,		"PW 27"		},//added for ALIV, metered injectors
/* ----------------------- */

};

const char  *SAI_alarm_map [16][NUMBER_SAI_TYPES] =
{ 
/* -------- *//* ----------------------- ----------------------- ----------------------- 	--------------------- */
/* -------- *//* TITAN                   	BLEND-PAK               	MINI-PAK                	ADD-PACK              */
/* -------- *//* ----------------------- ----------------------- ----------------------- --------------------- */
/* bit0     */{  "additive_freq",          	"additive_freq",          	"low_additive",           	"low_additive"          },
/* bit1     */{  "low_additive",           	"additive_no_pulses",     	"additive_no_pulses",     	"additive_freq"		   	},
/* bit2     */{  "additive_no_pulses",     	"general_additive_alarm", 	"additive_pulse_excess",  	"additive_no_pulses"    },
/* bit3     */{  "additive_pulse_excess",  	"low_additive",           	"general_additive_alarm", 	"overrev_injector"      },
/* bit4     */{  "general_additive_alarm", 	"additive_pulse_excess",  	"general_additive_alarm", 	"additive_pulse_excess" },
/* bit5     */{  "general_additive_alarm", 	"general_additive_alarm", 	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit6     */{  "no_sai_alarm",           	"general_additive_alarm", 	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit7     */{  "no_sai_alarm",           	"general_additive_alarm", 	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit8     */{  "no_sai_alarm",           	"general_additive_alarm", 	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit9     */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit10    */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit11    */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit12    */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"addPak1_powerfail"     },
/* bit13    */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"addPak1_diagnostic"    },
/* bit14    */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm"         	},
/* bit15    */{  "no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm",           	"no_sai_alarm"         	}
};




enum SAI_type SAI_type_find (unsigned char programmed_inj_no, enum COMDRV_virtual_ports CurPort)
{
    /*********************************************************************/
	register 	struct SAI_port_data_struct 	*pSAIPort;
    /*********************************************************************/

	pSAIPort = &SAIPort[CurPort];
	pSAIPort->CurSAIOffset = programmed_inj_no;

    switch (rDB.add_inj.inj[programmed_inj_no].type)
        {
        case TITAN_INJ:
            pSAIPort->CurSAIType = SAI_TITAN;
			break;

        case GATE_CITY_BLEND_PAK_INJ: /* This will be a Blend-pak */
            pSAIPort->CurSAIType = SAI_BLEND_PAK;
			break;

        case GATE_CITY_MINIPAK_INJ:
            pSAIPort->CurSAIType = SAI_MINI_PAK;
			break;

        case SMITH_INJ:
            pSAIPort->CurSAIType = SAI_MINI_PAK;
			break;

        case ADD_PAK_INJ:
		case ADD_PAK_2_STROKE:
		case SHARE_INJ_1:
		case SHARE_INJ_2:
		case SHARE_INJ_3:
		case SHARE_INJ_4:
		case METER_INJ:
		    pSAIPort->CurSAIType = SAI_ADD_PACK;
			break;

        default:
            /* Not a smart additive injector, so return an error code ! */
            pSAIPort->CurSAIType = NO_ASSOCIATED_TYPE;
			break;
        }

	return (pSAIPort->CurSAIType);
}




void SAI_board_find (unsigned char boardNo, enum COMDRV_virtual_ports CurPort)
{
    /*********************************************************************/
	register 	struct SAI_port_data_struct 	*pSAIPort;
    /*********************************************************************/

	pSAIPort = &SAIPort[CurPort];
	pSAIPort->CurAICBBoard 	= boardNo;
    pSAIPort->CurSAIType 	= SAI_ADD_PACK;

	return;
}



unsigned char II_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	/******************************************************/
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
#ifdef DEBUG_INJ_VOL
	FILE * file;
#endif
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							// Grab the port we are on
	pSAIPort->CurSAICmd = II;							   // Flag the Command to be sent
	sai_inj_type = SAI_type_find (inj_no, CurPort);			// Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 			   // If we aren't config'ed right,
		return (0);										   // return an error
	FormatSAIPackettHeader (inj_no, CurPort);				// Set-up the header
	cmdSize = 6;										   // Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)					   // If we're an Add-Pak
		cmdSize = 2;									   // Shrink it
															// Put the command in the buffer
	memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[II][sai_inj_type], cmdSize);
	pSAIPort->TxBuf[cmdSize+pSAIPort->TxIndex] = 0;
    pSAIPort->TxIndex += cmdSize;						   // Move the pointer into the buffer
    FormatSAIPackettFooter (CurPort);						// Put together the Footer
    SmartAITransmit(CurPort);								// And Away she goes!
#ifdef DEBUG_INJ_VOL
	file = fopen("/home/root/inj_vol.txt", "a+");
	fprintf(file, "%s:\t\t\tInjector\t%d\tVol\t%9.3f\tBatchVol\t%8.2f\n", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);
	syslog(LOG_ALERT, "%s|%d|%7.3f|%6.2f", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);
	if(file != NULL)
		fclose(file);
	else
		file = NULL;
#endif
    return(1);											   // Flag that we xmitted the message
}

unsigned char Poll_Totals_And_Alarms_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	/******************************************************/
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							// Grab the port we are on
	pSAIPort->CurSAICmd = POLL_TOTALS_AND_ALARMS;			// Flag the Command to be sent
    sai_inj_type = SAI_type_find (inj_no, CurPort);			// Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				// If we aren't config'ed right,
		return (0);											// return an error
															// If we're not a Titan or Add-Pack, 
    if ((sai_inj_type != SAI_TITAN) && (sai_inj_type != SAI_ADD_PACK)) 
    	return (0) ;										// return an error
    FormatSAIPackettHeader (inj_no, CurPort);				// Set-up the header
	cmdSize = 6;										   	// Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)					   	// If we're an Add-Pak
		cmdSize = 2;									   	// Shrink it
															// Put the command in the buffer
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[POLL_TOTALS_AND_ALARMS][sai_inj_type], cmdSize);
    pSAIPort->TxIndex += cmdSize;							// Move the pointer into the buffer
    pSAIPort->TxBuf[cmdSize+pSAIPort->TxIndex+1] = 0;
    FormatSAIPackettFooter (CurPort);						// Put together the Footer
    SmartAITransmit(CurPort);								// And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
    return(1);												// Flag that we xmitted the message
}


unsigned char Poll_Totals_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	/******************************************************/
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							// Grab the port we are on
	pSAIPort->CurSAICmd = POLL_TOTALS;                      // Flag the Command to be sent             
    sai_inj_type = SAI_type_find (inj_no, CurPort);			// Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				// If we aren't config'ed right,
		return (0);	        								// return an error
	FormatSAIPackettHeader (inj_no, CurPort);               // Set-up the header           
	cmdSize = 6;										   	// Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)					   	// If we're an Add-Pak
		cmdSize = 2;									   	// Shrink it
															// Put the command in the buffer
	memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[POLL_TOTALS][sai_inj_type], cmdSize);    
	pSAIPort->TxIndex += cmdSize;                           // Move the pointer into the buffer               
	FormatSAIPackettFooter (CurPort);                       // Put together the Footer
	SmartAITransmit(CurPort);                               // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return (1);                                             // Flag that we xmitted the message  
}


unsigned char Poll_Alarms_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	/******************************************************/
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							// Grab the port we are on
	pSAIPort->CurSAICmd = POLL_ALARMS;                      // Flag the Command to be sent              
    sai_inj_type = SAI_type_find (inj_no, CurPort);			// Find our type

	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				// If we aren't config'ed right,
		return (0);											// return an error
    FormatSAIPackettHeader (inj_no, CurPort);				// Set-up the header           
	cmdSize = 6;										   	// Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)					   	// If we're an Add-Pak
		cmdSize = 2;									   	// Shrink it
															// Put the command in the buffer
	memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[POLL_ALARMS][sai_inj_type], cmdSize);
    pSAIPort->TxIndex+=cmdSize;								// Move the pointer into the buffer  
    FormatSAIPackettFooter (CurPort);						// Put together the Footer
    SmartAITransmit(CurPort);								// And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
    return(1);												// Flag that we xmitted the message  
}




unsigned char Authorize_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	/******************************************************/
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
#ifdef DEBUG_INJ_VOL
	FILE * file;
#endif
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							// Grab the port we are on
	pSAIPort->CurSAICmd = AUTHORIZE;						// Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			// Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				// If we aren't config'ed right,
		return (0); 										// return an error
    if (sai_inj_type == SAI_TITAN)
        return (0);											// return an error
    FormatSAIPackettHeader (inj_no, CurPort);				// Set-up the header
	cmdSize = 6;										   	// Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)					   	// If we're an Add-Pak
		cmdSize = 2;									   	// Shrink it
															// Put the command in the buffer
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[AUTHORIZE][sai_inj_type], cmdSize);
    pSAIPort->TxIndex += cmdSize;							// Move the pointer into the buffer  
    FormatSAIPackettFooter (CurPort);						// Put together the Footer
    SmartAITransmit(CurPort);								// And Away she goes!
#ifdef DEBUG_INJ_VOL
	system("echo $(date) >> /home/root/inj_vol.txt");
	file = fopen("/home/root/inj_vol.txt", "a+");
	fprintf(file, "%s:\t\tInjector\t%d\tVol\t%9.3f\tBatchVol\t%8.2f\n", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);
	printf("%s: Injector %d Vol[%9.3f], BatchVol[%8.2f]\n", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);
	syslog(LOG_ALERT, "%s|%d|%7.3f|%6.2f", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);

	if(file != NULL)
		fclose(file);
	else
		file = NULL;
#endif
    return(1);												// Flag that we xmitted the message  
}


unsigned char DeAuthorize_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	/******************************************************/
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
#ifdef DEBUG_INJ_VOL
	FILE * file;
#endif
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							// Grab the port we are on
	pSAIPort->CurSAICmd = DEAUTHORIZE;						// Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			// Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				// If we aren't config'ed right,
		return (0);        									// return an error
	pSAIPort->DeauthorizeInProgress = TRUE;    				// Flag that we are going to start a deauthorize
    //OTF_InjState added for wild stream blending with unlimited preset
    if(OTF_InjState[inj_no] == OTF_INJ_WAIT_DEAUTH)
    	OTF_InjState[inj_no] = OTF_INJ_DEAUTH_PASS;	  
    if (sai_inj_type == SAI_TITAN)							// If we're a Titan, this is don't do. 
        {       
		pSAIPort->DeauthorizeInProgress = FALSE;			// Flag that the deauthorize is done
        return(0);											// return an error
        }

    FormatSAIPackettHeader (inj_no, CurPort);				// Set-up the header
	cmdSize = 6;										   	// Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)					   	// If we're an Add-Pak
		cmdSize = 2;									   	// Shrink it
															// Put the command in the buffer
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[DEAUTHORIZE][sai_inj_type], cmdSize);
    pSAIPort->TxIndex += cmdSize;							 // Move the pointer into the buffer  
    FormatSAIPackettFooter (CurPort);						 // Put together the Footer
    SmartAITransmit(CurPort);								 // And Away she goes!
#ifdef DEBUG_INJ_VOL
	file = fopen("/home/root/inj_vol.txt", "a+");
	fprintf(file, "%s:\tInjector\t%d\tVol\t%9.3f\tBatchVol\t%8.2f\n", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);
	printf("%s: Injector %d Vol[%9.3f], BatchVol[%8.2f]\n", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);
	syslog(LOG_ALERT, "%s|%d|%7.3f|%6.2f", __FUNCTION__, inj_no+1, rDB.add_inj.inj[inj_no].additive_total, CurBatchVol[inj_no]);

 	if(file != NULL)
		fclose(file);
	else
		file = NULL;

#endif
    return(1);												 // Flag that we xmitted the message  
}

                                                                               
                                                                               
unsigned char SetVol_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)                                        
 {                                                                             
	/******************************************************/
    //char vol_array_4[4];                                                        
    //char vol_array_6[6];
    char vol_array[10];                                                        
    enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct 	*pSAIPort;
	char *comma_ptr;
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							   // Grab the port we are on
	pSAIPort->CurSAICmd = SET_VOL_PER_INJ;					   // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			   // Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				   // If we aren't config'ed right,
		return (0);    										   // return an error
    if (sai_inj_type == SAI_ADD_PACK)						   // If we're an Add-Pack, don't do this.  
		return (0);											   // (there is no corresponding command)
    FormatSAIPackettHeader (inj_no, CurPort);				   // Set-up the header
															   // Put the command in the buffer
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_VOL_PER_INJ][sai_inj_type], 6);
    pSAIPort->TxIndex += 6;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
	pSAIPort->TxIndex++;
    if (sai_inj_type == SAI_TITAN)
        {                                                                               
        sprintf(vol_array,"%04.0f",rDB.add_inj.inj[inj_no].vol_per_inj); 
		comma_ptr = strchr(vol_array, ',');
		if(comma_ptr != NULL)
			*comma_ptr = '.';//convert comma to decimal
        memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), vol_array/*vol_array_4*/, 4);                           
    	pSAIPort->TxIndex += 4;
        }
    else 
        {
        sprintf(vol_array,"%06.1f",rDB.add_inj.inj[inj_no].vol_per_inj);   
		comma_ptr = strchr(vol_array, ',');
		if(comma_ptr != NULL)
			*comma_ptr = '.';//convert comma to decimal
        memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), vol_array/*vol_array_6*/, 6);                           
	    pSAIPort->TxIndex += 6;
        }                                                                               
     FormatSAIPackettFooter (CurPort);                        // Put together the Footer
     SmartAITransmit(CurPort);								  // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
     return(1);												  // Flag that we xmitted the message  
 }                                                                             



unsigned char ClearAlarms_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)                               
 {                                                                             
	/******************************************************/
    const char clearSAIAlarmArray[5] 	= "0000";
    const char clearAddPakAlarmArray[5] = "FFFF";
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned char cmdSize;
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = CLEAR_ALARMS;						  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 				  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
	cmdSize = 6;											  // Set-up the command size
	if (sai_inj_type == SAI_ADD_PACK)						  // If we're an Add-Pak
		cmdSize = 2;										  // Shrink it
															  // Put the command in the buffer
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[CLEAR_ALARMS][sai_inj_type], cmdSize);
    pSAIPort->TxIndex += cmdSize;							  // Move the pointer into the buffer 
															  // Now, if we need to, tack on a ClearAlarm Mask
    if ((sai_inj_type == SAI_TITAN) || (sai_inj_type == SAI_ADD_PACK))
        {
        *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
	    pSAIPort->TxIndex ++;
		if (sai_inj_type == SAI_TITAN)
	        memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), clearSAIAlarmArray, 4);                           
		else // (sai_inj_type == SAI_ADD_PACK))
	        memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), clearAddPakAlarmArray, 4);                           
	    pSAIPort->TxIndex += 4;
        }
     FormatSAIPackettFooter (CurPort);                        // Put together the Footer
     SmartAITransmit(CurPort);                                // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif

     return(1);												  // Flag that we xmitted the message  
 }                                                                             

                                                                               
unsigned char SetVolPerCycle_SAI (unsigned char inj_no, enum COMDRV_virtual_ports CurPort)                               
 {                                                                             
	/******************************************************/
    //char volArray6[6];                                                        
    //char volArray8[8];
    char volArray[10];                                                        
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	char *comma_ptr;
	/******************************************************/

	pSAIPort = &SAIPort[CurPort];
	pSAIPort->CurSAICmd = SET_VOL_PER_CYCLE;
    sai_inj_type = SAI_type_find (inj_no, CurPort);
	if (sai_inj_type == NO_ASSOCIATED_TYPE) 
		return (0);
    FormatSAIPackettHeader (inj_no, CurPort);
	if (sai_inj_type == SAI_ADD_PACK)						  // If we're an Add-Pak
		{
	    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_VOL_PER_CYCLE][sai_inj_type], 5);
	    pSAIPort->TxIndex += 5;
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
	    pSAIPort->TxIndex ++;
        //GetCharFromFloat replaced with sprintf in rev 11.11
	    //GetCharFromFloat(volArray8, rDB.add_inj.inj[inj_no].vol_per_cycle, 4, 3);
	    sprintf(volArray,"%08.3f",rDB.add_inj.inj[inj_no].vol_per_cycle); 
		comma_ptr = strchr(volArray, ',');
		if(comma_ptr != NULL)
			*comma_ptr = '.';//convert comma to decimal
	    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), /*volArray8*/volArray, 8);                           
	    pSAIPort->TxIndex += 8;
		}
	else
		{
	    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_VOL_PER_CYCLE][sai_inj_type], 6);
	    pSAIPort->TxIndex += 6;
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
	    pSAIPort->TxIndex ++;
        //GetCharFromFloat replaced with sprintf in rev 11.11
	    //GetCharFromFloat(volArray6, rDB.add_inj.inj[inj_no].vol_per_cycle, 4, 1);
		sprintf(volArray,"%06.1f",rDB.add_inj.inj[inj_no].vol_per_cycle); 
		comma_ptr = strchr(volArray, ',');
		if(comma_ptr != NULL)
			*comma_ptr = '.';//convert comma to decimal
	    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), volArray/*volArray6*/, 6);                           
	    pSAIPort->TxIndex += 6;
		}
    FormatSAIPackettFooter (CurPort);
    SmartAITransmit(CurPort);
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
    return (1);
 }                                                                             

unsigned char SetKFactor_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char factor_array[13];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_K_FACTOR;						  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_K_FACTOR][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	//PLEASE NOTE: IF YOU CHANGE FORMAT SPECIFIER BE SURE CORRECT LOCATION IS
	//CALLED THAT CONVERTS ',' TO '.' AS DONE AFTER THIS SPRINTF
	sprintf(factor_array,"%8.3f",pDB.add_inj.inj[inj_no].inj_k_factor);
	factor_array[8-3-1]='.'; //be sure a decimal point, not a comma (pDB.dec_comma_sel),where (8-3-1) is based off format specifier above
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), factor_array, 8);
    pSAIPort->TxIndex += 8;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}



unsigned char SetMtrFactor_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char factor_array[12];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_MTR_FACTOR;					  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_MTR_FACTOR][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	//PLEASE NOTE: IF YOU CHANGE FORMAT SPECIFIER BE SURE CORRECT LOCATION IS
	//CALLED THAT CONVERTS ',' TO '.' AS DONE AFTER THIS SPRINTF
	sprintf(factor_array,"%6.4f",pDB.add_inj.inj[inj_no].inj_meter_factor);
	factor_array[6-4-1]='.';//deciaml instead of comma 
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), factor_array, 6);
    pSAIPort->TxIndex += 6;
	FormatSAIPackettFooter (CurPort);                      	  // Put together the Footer
	SmartAITransmit(CurPort);                              	  // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}




unsigned char SetHiTol_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char tol_array[8];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_HI_TOL;						  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_HI_TOL][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	//PLEASE NOTE: IF YOU CHANGE FORMAT SPECIFIER BE SURE CORRECT LOCATION IS
	//CALLED THAT CONVERTS ',' TO '.' AS DONE AFTER THIS SPRINTF
	sprintf(tol_array,"%5.1f", pDB.add_inj.inj[inj_no].inj_high_tol);
	tol_array[5-1-1] = '.';//convert decimal to comma
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), tol_array, 5);
    pSAIPort->TxIndex += 5;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}



unsigned char SetLoTol_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char tol_array[8];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_LO_TOL;						  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_LO_TOL][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	//PLEASE NOTE: IF YOU CHANGE FORMAT SPECIFIER BE SURE CORRECT LOCATION IS
	//CALLED THAT CONVERTS ',' TO '.' AS DONE AFTER THIS SPRINTF
	sprintf(tol_array,"%5.1f", pDB.add_inj.inj[inj_no].inj_low_tol);
	tol_array[5-1-1] = '.';
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), tol_array, 5);
    pSAIPort->TxIndex += 5;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}




unsigned char SetMaxErrs_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char errs_address[3];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_MAX_ERRS;						  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_MAX_ERRS][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	GetCharAddress((char *)errs_address, pDB.add_inj.inj[inj_no].max_inj_tol_errors);
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), errs_address+1, 2);
    pSAIPort->TxIndex += 2;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}





unsigned char SetConvFactor_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char conv_array[14];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	char *comma_ptr;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_CONV_FACTOR;					  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_CONV_FACTOR][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	sprintf(conv_array,"%+8.6e",pDB.add_inj.conversion_factor);
	comma_ptr = strchr(conv_array, ',');
	if(comma_ptr != NULL)
		*comma_ptr = '.';//convert comma to decimal
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), conv_array, 14);
    pSAIPort->TxIndex += 14;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d (%+8.6e)\n", __FUNCTION__, inj_no+1, pDB.add_inj.conversion_factor);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}

unsigned char SetAlrmPulseCount_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char count_array[4];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	char *comma_ptr;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_ALARM_PULSE_COUNT;			  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_ALARM_PULSE_COUNT][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	sprintf(count_array,"%03.0f",pDB.add_inj.alarm_pulse_count);
	comma_ptr = strchr(count_array, ',');
	if(comma_ptr != NULL)
		*comma_ptr = '.';//convert comma to decimal
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), count_array, 4);
    pSAIPort->TxIndex += 4;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}

unsigned char SetAlrmPulseTime_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char time_array[4];
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	char *comma_ptr;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_ALARM_PULSE_TIME;			  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_ALARM_PULSE_TIME][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	sprintf(time_array,"%03lu",pDB.add_inj.alarm_pulse_time);
	comma_ptr = strchr(time_array, ',');
	if(comma_ptr != NULL)
		*comma_ptr = '.';//convert comma to decimal
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), time_array, 4);
    pSAIPort->TxIndex += 4;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}


unsigned char SetControlMethod_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//----------------------------------------------------
	char control_array[3];
	char control;
	enum SAI_type sai_inj_type;
	register struct SAI_port_data_struct	*pSAIPort;
	//----------------------------------------------------
	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_CONTROL_METHOD;			  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_CONTROL_METHOD][sai_inj_type], 5);
    pSAIPort->TxIndex += 5;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;

    if(pDB.add_inj.inj[inj_no].type == METER_INJ)
    {
    	//Tell the A4M/A4B this Injector is Not Shared
    	control = 2;
    }
    else
    {
    	control = (pDB.add_inj.inj[inj_no].type == ADD_PAK_2_STROKE) ? 1 : 0;
    }

	sprintf(control_array,"%02u",control);
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), control_array, 3);
    pSAIPort->TxIndex += 3;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}

unsigned char SetMtrInjIoPt_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
	char io_pt_array[10];
	enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
 	unsigned char pulse_in;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];				  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_MTR_INJ_IO_PT;		  // Flag the Command to be sent
    	sai_inj_type = SAI_type_find (inj_no, CurPort);		  // Find our type
	if (sai_inj_type != SAI_ADD_PACK)			  // If we aren't config'ed right,
		return (0);					  // return an error

	if (inj_no>MAX_INJECTORS)
		return (0);					  // return an error

	//Make Sure We Are Either a Metered Inejctor or Shared Injector
	if((rDB.add_inj.inj[inj_no].type != METER_INJ) &&
			(rDB.add_inj.inj[inj_no].type < SHARE_INJ_1 && rDB.add_inj.inj[inj_no].type > SHARE_INJ_4))
	{
		return (0);
	}

	FormatSAIPackettHeader (inj_no, CurPort);		  // Set-up the header
    	memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_MTR_INJ_IO_PT][sai_inj_type], 5);
    	pSAIPort->TxIndex += 5;
    	*(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;
    	pSAIPort->TxIndex ++;

    	for(pulse_in=0;pulse_in<MAX_PULSE_IN;pulse_in++)
    	{
		if (pDB.pul_in[pulse_in].pulse_func == NO_PULSE_IN_FUNC)
			continue;
		if(rDB.add_inj.inj[inj_no].type == METER_INJ)
		{
			if (pDB.pul_in[pulse_in].pulse_func - MTR_INJ_1_FUNC == inj_no)
				break;  //found our metered injector here, let's use it below...
    	}
    	else
    	{
    		//Find the Shared Injector's Pulse Input
			if (pDB.pul_in[pulse_in].pulse_func - MTR_INJ_1_FUNC == (rDB.add_inj.inj[inj_no].type - SHARE_INJ_1))
				break;  //found our metered injector here, let's use it below...
			}
    	}

		if(rDB.add_inj.inj[inj_no].type == METER_INJ)
		{
			sprintf(io_pt_array,"%02u %02u %02u",pDB.meter_inj_io_pt[inj_no], pDB.add_pump_io_pt[inj_no], pulse_in);
		}
		else
		{
			sprintf(io_pt_array,"%02u %02u %02u",pDB.share_add_sol_io_pt[inj_no], pDB.add_pump_io_pt[inj_no], pulse_in);
		}
    	memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), io_pt_array, 8);

    	pSAIPort->TxIndex += 8;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!

#ifdef DEBUG_CMDS
    	syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message
}

unsigned char ResetPulseCount_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = RESET_PULSE_COUNT;				  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[RESET_PULSE_COUNT][sai_inj_type], 2);
    pSAIPort->TxIndex += 2;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}





unsigned char ReadPulseCount_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = READ_PULSE_COUNT;					  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    SmartInjTotalsStatus[inj_no] = 0;						  //set to resync totals
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[READ_PULSE_COUNT][sai_inj_type], 2);
    pSAIPort->TxIndex += 2;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}




unsigned char SetInit_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = INITIALIZE;						  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
	FormatAddPakSystemPackettHeader ((unsigned int)inj_no, CurPort);		  // Set-up the system header for the Add-Pak
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[INITIALIZE][sai_inj_type], 2);
    pSAIPort->TxIndex += 2;
    FormatSAIPackettFooter (CurPort);                         // Put together the Footer
    SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(0);												  // no response required for initialize command 
}




unsigned char SWVersion_SAI(unsigned char inj_no, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SOFTWARE_VERSION;					  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SOFTWARE_VERSION][sai_inj_type], 2);
    pSAIPort->TxIndex += 2;
	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}



unsigned char SetOutputState_SAI(unsigned char inj_no, unsigned char output, unsigned char state, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = SET_OUTPUT_STATE;					  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_OUTPUT_STATE][sai_inj_type], 2);
    pSAIPort->TxIndex += 2;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;

	if (output == PUMP)
		{
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'P';                                    
	    pSAIPort->TxIndex ++;
		}
	else if (output == SOLENOID)
		{
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'S';                                    
	    pSAIPort->TxIndex ++;
		}
	else // Error condition
		{
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'X';                                    
	    pSAIPort->TxIndex ++;
		}

    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;

	if (state == SAI_OFF)
		{
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = '0';                                    
	    pSAIPort->TxIndex ++;
		}
	else if (state == SAI_ON)
		{
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = '1';                                    
	    pSAIPort->TxIndex ++;
		}
	else // Error condition
		{
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'X';                                    
	    pSAIPort->TxIndex ++;
		}

	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}



unsigned char ReadOutputState_SAI(unsigned char inj_no, unsigned char output, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
    enum SAI_type sai_inj_type;
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

	pSAIPort = &SAIPort[CurPort];							  // Grab the port we are on
	pSAIPort->CurSAICmd = READ_OUTPUT_STATE;				  // Flag the Command to be sent  
    sai_inj_type = SAI_type_find (inj_no, CurPort);			  // Find our type
	if (sai_inj_type != SAI_ADD_PACK) 						  // If we aren't config'ed right,
		return (0);											  // return an error
    FormatSAIPackettHeader (inj_no, CurPort);				  // Set-up the header
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[READ_OUTPUT_STATE][sai_inj_type], 2);
    pSAIPort->TxIndex += 2;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;

	if (output == PUMP)
		{
		pSAIPort->CurSAIOutput = PUMP;
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'P';                                    
	    pSAIPort->TxIndex ++;
		}
	else
		{
		pSAIPort->CurSAIOutput = SOLENOID;
	    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'S';                                    
	    pSAIPort->TxIndex ++;
		}

	FormatSAIPackettFooter (CurPort);                         // Put together the Footer
	SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s: Injector %d\n", __FUNCTION__, inj_no+1);
    syslog(LOG_ALERT, "Injector %d = %s", inj_no+1, __FUNCTION__);
#endif
	return(1);												  // Flag that we xmitted the message  
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//				AICB General IO Interface
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include "aicb_io.h"

unsigned char AuthorizeGeneralIO_SAI(unsigned char boardNo, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
 	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned int i;
	register unsigned int j;

	unsigned char tempString[8] = {0,0,0,0,0,0,0,0};
	unsigned char tempChar;
	//-----------------------------------------------------

 	if ((CurPort >= COMDRV_MTR_INJ_A4M) || (CurPort == COMDRV_null))	// Not valid for metered injectors on A4M
 		return(0);

	pSAIPort = &SAIPort[CurPort];							  	// Grab the port we are on
	pSAIPort->CurSAICmd = AUTHORIZE_IO;						  	// Flag the Command to be sent  
    SAI_board_find (boardNo, CurPort);		  					// Find our type
    FormatAddPakBoardPackettHeader ((unsigned int)boardNo, CurPort);    // Set-up the system header for the Add-Pak
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[AUTHORIZE_IO][SAI_ADD_PACK], 2);
    pSAIPort->TxIndex += 2;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;

	for (i=0; i<3; i++)
		{
		tempChar = 0;

		for (j=0; j<4; j++)
			{
			if ((i+j) >= NUM_AICB_INPUTS_PER_BOARD) 
				break;
			tempChar |= (gAICBInputsAuth[boardNo][(4*i)+j] << j);
			}

		if (tempChar < 10)
			tempString[2-i] = tempChar + (unsigned char)(0x30);
		else 
			tempString[2-i] = tempChar + (unsigned char)(0x37);
		}

	for (i=0; i<5; i++)
		{
		tempChar = 0;

		for (j=0; j<4; j++)
			{
			tempChar |= (gAICBOutputsAuth[boardNo][(4*i)+j] << j);
			}

		if (tempChar < 10)
			tempString[7-i] = tempChar + (unsigned char)(0x30);
		else 
			tempString[7-i] = tempChar + (unsigned char)(0x37);
		}

    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), &tempString[0], 8);
    pSAIPort->TxIndex += 8;
	pSAIPort->AICBBoardCommInProgress	= TRUE;
    FormatSAIPackettFooter (CurPort);                         // Put together the Footer
    SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s (%s)\n",__FUNCTION__, tempString);
    syslog(LOG_ALERT, "%s", __FUNCTION__);
#endif
	return(1);												  // response required
}


unsigned char DeAuthorizeGeneralIO_SAI(unsigned char boardNo, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

 	if ((CurPort >= COMDRV_MTR_INJ_A4M) || (CurPort == COMDRV_null))	// Not valid for metered injectors on A4M
 		return(0);

	pSAIPort = &SAIPort[CurPort];							  	// Grab the port we are on
	pSAIPort->CurSAICmd = DEAUTHORIZE_IO;						  	// Flag the Command to be sent  
    SAI_board_find (boardNo, CurPort);		  					// Find our type
    FormatAddPakBoardPackettHeader ((unsigned int)boardNo, CurPort);    // Set-up the system header for the Add-Pak
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[DEAUTHORIZE_IO][SAI_ADD_PACK], 2);
    pSAIPort->TxIndex += 2;
	pSAIPort->AICBBoardCommInProgress	= TRUE;
    FormatSAIPackettFooter (CurPort);                         // Put together the Footer
    SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s\n", __FUNCTION__);
    syslog(LOG_ALERT, "%s", __FUNCTION__);
#endif
	return(1);												  // response required
}




unsigned char SetGeneralIO_SAI(unsigned char boardNo, enum COMDRV_virtual_ports CurPort)
{
	//-----------------------------------------------------
 	register struct SAI_port_data_struct 	*pSAIPort;
	register unsigned int i;
	register unsigned long tempLong;
	register unsigned long tempOut;

	unsigned char tempString[8] = {0,0,0,0,0,0,0,0};
	#define LOW_NIBBLE_MASK	((unsigned long)0x0000000F)
	//-----------------------------------------------------

 	if ((CurPort >= COMDRV_MTR_INJ_A4M) || (CurPort == COMDRV_null))	// Not valid for metered injectors on A4M
		return(0);

	pSAIPort = &SAIPort[CurPort];							  	// Grab the port we are on
	pSAIPort->CurSAICmd = SET_OR_GET_IO;						  	// Flag the Command to be sent  
    SAI_board_find (boardNo, CurPort);		  					// Find our type
    FormatAddPakBoardPackettHeader ((unsigned int)boardNo, CurPort);    // Set-up the system header for the Add-Pak
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_OR_GET_IO][SAI_ADD_PACK], 2);
    pSAIPort->TxIndex += 2;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'O';
    pSAIPort->TxIndex ++;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
	tempOut = GetAICBOutMap(boardNo);
	
	for (i=0; i<8; i++)
		{
		tempLong = tempOut >> (4*(7-i));
		tempLong = tempLong & LOW_NIBBLE_MASK;

		if (tempLong < 10)
			tempString[i] = (unsigned char)tempLong + (unsigned char)(0x30);
		else 
			tempString[i] = (unsigned char)tempLong + (unsigned char)(0x37);
		}

    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), &tempString[0], 8);
    pSAIPort->TxIndex += 8;
	pSAIPort->CurIODirection = 'O';
	pSAIPort->AICBBoardCommInProgress	= TRUE;
    FormatSAIPackettFooter (CurPort);                         // Put together the Footer
    SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s (%s)\n", __FUNCTION__, tempString);
    syslog(LOG_ALERT, "%s", __FUNCTION__);
#endif
	return(1);												  // response required
}


unsigned char GetGeneralIO_SAI(unsigned char boardNo, enum COMDRV_virtual_ports CurPort)
{

	//-----------------------------------------------------
 	register struct SAI_port_data_struct 	*pSAIPort;
	//-----------------------------------------------------

 	if ((CurPort >= COMDRV_MTR_INJ_A4M) || (CurPort == COMDRV_null))	// Not valid for metered injectors on A4M
 		return(0);

	pSAIPort = &SAIPort[CurPort];							  	// Grab the port we are on
	pSAIPort->CurSAICmd = SET_OR_GET_IO;						  	// Flag the Command to be sent  
    SAI_board_find (boardNo, CurPort);		  					// Find our type
    FormatAddPakBoardPackettHeader ((unsigned int)boardNo, CurPort);    // Set-up the system header for the Add-Pak
    memcpy((pSAIPort->TxBuf + pSAIPort->TxIndex), SAI_command_table[SET_OR_GET_IO][SAI_ADD_PACK], 2);
    pSAIPort->TxIndex += 2;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = SPACE_SAI;                                    
    pSAIPort->TxIndex ++;
    *(pSAIPort->TxBuf + pSAIPort->TxIndex) = 'I';                                    
    pSAIPort->TxIndex ++;
	pSAIPort->CurIODirection = 'I';
	pSAIPort->AICBBoardCommInProgress	= TRUE;
    FormatSAIPackettFooter (CurPort);                         // Put together the Footer
    SmartAITransmit(CurPort);                                 // And Away she goes!
#ifdef DEBUG_CMDS
    printf("%s\n", __FUNCTION__);
    syslog(LOG_ALERT, "%s", __FUNCTION__);
#endif
	return(1);												  // response required

}
