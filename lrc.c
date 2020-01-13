#include <stdio.h>
#include <string.h>

#ifndef BYTE
  #define BYTE unsigned char
#endif
 
#define STX 0x02
#define ETX 0x03
#define PAD 0x7F
#define NUL 0x00
#define CR  0x0D
#define LF  0x0A
#define ENQ 0x05
 
BYTE GetLRC(BYTE* pbData, int iCount)
{
	BYTE chLRC = 0;
	while(iCount > 0)
  	{
  	  chLRC ^= *pbData++;
  	  iCount--;
  	}
 
	return chLRC;
}

main ( int argc, char *argv[])
{
	int i,j;
	char buf[255];

	if(argc!=3)
	{
	  printf("Usage:  ./LRC <address> <text>\n");
	  return(1);
	}

	sprintf(buf,"%02d%s%c", argv[1], argv[2], ETX);
	printf("02 ",buf);

	// Show hex dump of message
	for(j=0;j<strlen(buf);j++)
	{
	  printf("%02x ",buf[j]);
	}

	printf("%02x 7F\n",GetLRC(buf,strlen(buf)));

	return 0;
}
