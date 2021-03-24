#include<stdio.h>  
#include <string.h>    
typedef struct meter_alarm{    
	long time_stamp; 
	int alarm;
	int length;
	char string[10];    
}cfx_meter_alarm;    

int main(){    
int i;    
cfx_meter_alarm alarm_log[10]; 
char substring[10];

       
	for(i=0;i<10;i++)
	{        
		alarm_log[i].time_stamp = i;
		alarm_log[i].alarm = 99;
		alarm_log[i].length = 10;
		sprintf(substring, "Test%d", i);
		strncpy(alarm_log[i].string, substring, sizeof(alarm_log[i].string));    
	}    
	printf("\nStudent Information List:");    
	for(i=0;i<10;i++)
	{
		//printf("\n%ld", alarm_log[i].time_stamp);
		//printf("\n%d", alarm_log[i].alarm);
		//printf("\n%d", alarm_log[i].length);
		//printf("\n%s", alarm_log[i].string);  
		printf("\n%ld %d %d %s", alarm_log[i].time_stamp, alarm_log[i].alarm, alarm_log[i].length, alarm_log[i].string);
	}    
   return 0;    
}    