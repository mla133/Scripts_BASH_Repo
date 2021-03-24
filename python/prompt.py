import socket
from struct import *
import time
import binascii

mNET = '192.168.181.76'
mPort = 502
BUFF_SIZE = 1048
i = 0
timeout=0
data = ""
Pone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Pone.connect((mNET,mPort))
Pone.settimeout(2)

while True:
        print ("loop %i" % i)
        i+=1

        time.sleep(.2)

        # Send Wx prompt data 'PRODUCT:HSD-5000 LIT'
        Pone.send(bytes.fromhex('00000000001B4C109800000A1450524F445543543A4853442D35303030204C4954'))
        print ("Sending prompt data") 

        print ("receive")
        try:
                data = Pone.recv(BUFF_SIZE)
        
        except socket.timeout:
                timeout+=1
                print ("Timed out, count %i", timeout)
                continue
        print ("data: \t\t" , data)
        data1 = bytearray.fromhex('0000000000064c109800000a')

        if (data == data1):
                print ('Valid Return\n')
        else:
                break
        # Send Host command to post Wx prompt data
        Pone.send(bytes.fromhex('0000000000134c109e8500060c0001000a0000002c00000000'))
        print ("Sending host command")

        print ("receive")
        try:
                data = Pone.recv(BUFF_SIZE)
        
        except socket.timeout:
                timeout+=1
                print ("Timed out, count %i", timeout)
                continue
        print ("data: \t\t" , data)
        data1 = bytearray.fromhex('0000000000064c109e850006')

        if (data == data1):
                print ('Valid Return\n')
        else:
                break        
        # Send command to check host command status register (expecting a '254' or 'FE' at the end)
        Pone.send(bytes.fromhex('0000000000064C040E0A0001'))
        print ("Checking Host Register Status")

        print ("receive")
        try:
                data = Pone.recv(BUFF_SIZE)
        
        except socket.timeout:
                timeout+=1
                print ("Timed out, count %i", timeout)
                continue
        print ("data: \t\t" , data)
        data1 = bytearray.fromhex('0000000000054C040200FE')

        if (data == data1):
                print ('Valid Return\n')
        else:
                break
        
        # Read back prompt message registers to ensure they were written to...
        Pone.send(bytes.fromhex('0000000000064C039800000B'))
        print ("Checking Host Register Status")

        print ("receive")
        try:
                data = Pone.recv(BUFF_SIZE)
        
        except socket.timeout:
                timeout+=1
                print ("Timed out, count %i", timeout)
                continue
        print ("data: \t\t" , data)
        data1 = bytearray.fromhex('0000000000194C031650524F445543543A4853442D35303030204C49540000')

        if (data == data1):
                print ('Valid Return\n')
        else:
                break
        time.sleep(.2)
# Kick out an error response to err.txt for later viewing...        
fo = open("err.txt", "a+")
fo.write('***Invalid Response***\t\t')
fo.write("%s" % data)
fo.write('\n***Expected Respose***\t\t')
fo.write("%s" % data1)
fo.write("\nloop %i" % i)
fo.close()
