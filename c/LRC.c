#ifndef BYTE
  #define BYTE unsigned char
#endif
 
#define STX 0x02
#define ETX 0x03
#define PAD 0x7F
#define NULL 0x00
 
extern "C" BYTE GetLRC(BYTE* pbData,int iCount);
 
//GetLRC()---------------------------------------------------------------------
/*Calculates one byte Longitudinal Redundancy Checksum (LRC). The LRC is an 
  exclusive-or calculation on all data bytes. The LRC is calculated from the 
  begining of data buffer to the termination character, including termination 
  character itself. 
 
  Returns: Longitudinal Redundancy Checksum (LRC).
 
 
          +---+
          |STX|  Start of Text [1 Byte]
       /--+---+--
       |  | D |  Data [N bytes]
       L  | a |
       R  | t |
       C  | a |
          +---+
       s  |ETX|
       u  |ETB|  Termination Character [1 Byte]
       m  |EOT|
       \--+---+--
          |LRC|  Longitudinal Redundancy Checksum [1 Byte]
          +---+
                 iCount = N+1 [byte]
 
 */
BYTE GetLRC(BYTE* pbData, //[in] data buffer including 
                          //termination character (ETB/ETX/EOT)
            int iCount    //[in] size of data in bytes including
                          //termination character
            )
{
BYTE chLRC = 0;
while(iCount > 0)
  {
  chLRC ^= *pbData++;
  iCount--;
  }
 
return chLRC;
}

main ()
{
 
char buf[255];
char message[] = "This is a Test";
 
// prepare body
sprintf(buf,"%c%s%c",STX,message,ETX);
 
// append LRC
sprintf(buf,"%s%c",buf,GetLRC(buf,strlen(buf))); // call 'GetLRC()' from above

}