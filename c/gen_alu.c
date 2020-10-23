/*                                                                       
 *                                                                       
 * 4bitalu.c V1.0 (c) Dieter Mueller 08/2004                             
 *                                                                       
 * example: 4 Bit ALU inside the 27512 EPROM. Some Pins unused.          
 *                                                                       
 * WARNING: this code is intended for demonstration                      
 * only, and was never testet in a real/existing CPU.                    
 *                                                                       
 * Don't really expect it to work at all.                                
 *                                                                       
 */                                                                      
                                                                         
#include <stdio.h>                                                       
#include <stdlib.h>                                                      
                                                                         
//definition of ALU_commands                                             
                                                                         
#define ALU_PASS_A  0x00                                                 
#define ALU_PASS_B  0x01                                                 
                                                                         
#define ALU_ROL_A   0x02                                                 
#define ALU_ROR_A   0x03                                                 
#define ALU_LSL_A   0x04                                                 
#define ALU_LSR_A   0x05                                                 
                                                                         
#define ALU_ADD     0x06                                                 
#define ALU_SUB     0x07                                                 
#define ALU_ADC     0x08                                                 
#define ALU_SBC     0x09                                                 
                                                                         
#define ALU_AND     0x0a                                                 
#define ALU_OR      0x0b                                                 
#define ALU_XOR     0x0c                                                 
                                                                         
#define ALU_CONST_0 0x0d                                                 
#define ALU_CONST_1 0x0e                                                 
#define ALU_CONST_F 0x0f                                                 
                                                                         
                                                                         
int main(void);                                                          
char do_rom(long addr);                                                  
                                                                         
int main(void)                                                           
{                                                                        
  FILE *outstream;                                                       
                                                                         
  long i;                                                                
                                                                         
  outstream=fopen("4bitalu.bin","wb");                                   
  if(outstream==NULL)                                                    
  {                                                                      
    printf("\nFile open error.\n");                                      
    return(-1);                                                          
  }                                                                      
                                                                         
  for(i=0; i<0x10000; i++) //try all possible input_patterns, 64 kBytes   
  {                                                                      
    fputc(do_rom(i),outstream); //write one EPROM Byte                   
  }                                                                      
                                                                         
  fclose(outstream);                                                     
  return(0);                                                             
}                                                                        
                                                                         
char do_rom(long addr)                                                   
{                                                                        
  char out;                                                              
  char cmd,a,b;                                                          
  char cin;       //carry input                                          
  char cout,zout; //flags                                                
                                                                         
 //default: clear flags, clear result                                    
  out=0;                                                                 
  cin=0; cout=0; zout=0;                                                 
                                                                         
 //EPROM:                                                                
 //A0..3=A, A4..7=B,   A8..11=ALU_command, A12=Carry_in                  
 //Q0..3=Q, Q4=Z_Flag, Q7 =C_Flag                                        
  a  = addr     & 0x0f;                                                  
  b  =(addr>>4) & 0x0f;                                                  
  cmd=(addr>>8) & 0x0f;                                                  
                                                                         
  if((long)addr & 0x1000) cin=-1; //carry input                          
                                                                         
  switch(cmd)                                                            
  {                                                                      
    case ALU_PASS_A: out=a; break;                                       
    case ALU_PASS_B: out=b; break;                                       
                                                                         
    case ALU_ROL_A:  if(cin) out=0x01; //the rest like LSL               
    case ALU_LSL_A:  out|=(a<<1)&0x0e; if((char)a&0x08){cout=-1;} break; 
                                                                         
    case ALU_ROR_A:  if(cin) out=0x08; //the rest like LSR               
    case ALU_LSR_A:  out|=(a>>1)&0x07; if((char)a&0x01){cout=-1;} break; 
                                                                         
    case ALU_AND:    out=a&b; break;                                     
    case ALU_OR:     out=a|b; break;                                     
    case ALU_XOR:    out=a^b; break;                                     
                                                                         
    case ALU_ADC:    if(cin) out=1;                                      
    case ALU_ADD:    out+=(a&0xf)+(b&0xf);                               
                     if(out>0x0f){cout=-1;} break;                       
                                                                         
    case ALU_SBC:    if(cin==0) out=-1; //subtract 1, borrow active.     
    case ALU_SUB:    out+=(a&0xf)-(b&0xf);                               
                     if(out>=0){cout=-1;/*no borrow.*/} break;           
                                                                         
    case ALU_CONST_0: out=0x00; break;                                   
    case ALU_CONST_1: out=0x01; break;                                   
    case ALU_CONST_F: out=0x0f; break;                                   
  }                                                                      
                                                                         
  out&=0x0f; //limit result to 4 Bit, to keep the flags clean.           
  if(out==0) zout=-1; //check for Zero_Condition                                                   
                                                                         
 //now to pass the flags to the outputs.                                 
  if(zout) out|=0x10; //Zero                                             
  if(cout) out|=0x80; //Carry                                            
                                                                         
  return(out);                                                           
}