#importing all needed libraries
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import struct
import datetime
import csv

################################################################################################################
#    functions to decode double and float values
################################################################################################################

#########################
# floating-point function
#########################
def decode_ieee(val_int):
   return struct.unpack("f", struct.pack("I", val_int))[0]

def decode_ieee_double(val_int):
   return struct.unpack("d", struct.pack("q", val_int))[0]

#################################################################
# decoding long long (64 bits)
#################################################################


def word_list_to_longlong(val_list, big_endian=True):
   # allocate list for long int
    longlong_list = [None] * int(len(val_list) / 4)
    # fill registers list with register items
    for i, item in enumerate(longlong_list):
        if big_endian:
           longlong_list [i] = (val_list[i * 4] << 48) + (val_list[(i * 4) + 1] << 32) + (val_list[(i * 4) + 2] << 16) + val_list[(i * 4) + 3]
        else:
            longlong_list [i] = (val_list[(i * 4) + 3] << 48) + (val_list[(i * 4) + 2] << 32) + (val_list[(i * 4) + 1] << 16) + val_list[i * 4]
    # return longlong_list list
    return longlong_list


def long_list_to_word(val_list, big_endian=True):
   # allocate list for long int
    word_list = list()
    # fill registers list with register items
    for i, item in enumerate(val_list):
        if big_endian:
            word_list.append(val_list[i] >> 16)
            word_list.append(val_list[i] & 0xffff)
        else:
            word_list.append(val_list[i] & 0xffff)
            word_list.append(val_list[i] >> 16)
    # return long list
    return word_list

#################################################################################################################################
#                End of data decoding functions
#################################################################################################################################

class FloatModbusClient(ModbusClient):
    def read_float(self, reg_type,  address, number=1):
        if reg_type == 4:
            reg_l = self.read_input_registers(address, number * 2)
        else:
            reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None

    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)

    def read_double(self, reg_type, address, number=1):
        if reg_type == 4:
            reg_ll = self.read_input_registers(address, number * 4)
        else:
            reg_ll = self.read_holding_registers(address, number * 4)
        if reg_ll:
            return [decode_ieee_double(d) for d in word_list_to_longlong(reg_ll)]
        else:
            return None
    def read_long(self, reg_type,  address, number=1):
        if reg_type == 4:
            reg_l = self.read_input_registers(address, number * 2)
        else:
            reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.word_list_to_long(reg_l)]
        else:
            return None
 
############################################################
# FROM HERE YOU CAN POLL/WRITE TO REGISTERS AS YOU SEE FIT #
############################################################

#prompting the user to enter the ip for each device
ip1 = input("Enter ip address : ")

#declaring currentDT to equal the datetime function
currentDT = datetime.datetime.now()

#initializing repeat to y to enter the while loop
repeat = 'y'

#repeating the program while unless the user does not want to repeat
while repeat == 'y':
    
    #connecting to MicroLoad
    c = FloatModbusClient(host= ip1, port=502, unit_id = 1, auto_open=True)
    
    #checks to see if MicroLoad connection is open
    if c.open():
        #letting the user know that the device is connected and data is being read
        print("Connected to device")
        #collecting date/time for MicroFlow
        #Microhour = c.read_input_registers(1670,1)
        #Microminute = c.read_input_registers(1669,1)
        #Microsecond = c.read_input_registers(1668,1)
        #Microday = c.read_input_registers(1666,1)
        #Micromonth = c.read_input_registers(1665,1)
        #Microyear = c.read_input_registers(1664,1)
        #assigning values as strings to MicroTime and MicroDate ([1:-1] removes bracket from data ouput)
        #MicroTime = str(Microhour)[1:-1] + str(":") + str(Microminute)[1:-1] + str(":") + str(Microsecond)[1:-1]
        #MicroDate = str(Microday)[1:-1] + str("/") + str(Micromonth)[1:-1] + str("/") + str(Microyear)[1:-1]
        # collecting float values from MicroFlow using modbus adresses
        #RomCRC = c.read_input_registers(3840,2);
        #RomMajor = c.read_input_registers(3584,1);
        #RomMinor = c.read_input_registers(3585,1);

        RomCRC = c.read_input_registers(4928,2);
        RomMajor = c.read_input_registers(4800,1);
        RomMinor = c.read_input_registers(4804,1);

        print(RomCRC);
        print(RomMajor);
        print(RomMinor);

        #closing the connection to the MicroFlow
        c.close()
    else:
        #letting the user know that the device isn't connected
        print("Device not connected")
        
        
#    #opening and naming the csv file so it can be written to
#    with open('device_data.csv','a') as device_data:
#        device_data_writer = csv.writer(device_data)
#        #giving each of the columns a heading
#        device_data_writer.writerow(['   ', 'MicroFlow', 'AccuLoad', 'UCOS Windows', 'UCOS Linux','Omni', 'Spirit'])
#        #adding the date from each device to each column
#        device_data_writer.writerow(['Date', MicroDate, ALDate, windDate, linDate, OMNIDate, SpiritDate])
#        #adding the time from each device to each column
#        device_data_writer.writerow(['Time', MicroTime, ALTime, windTime, linTime, OMNITime, SpiritTime])
#        #assigning IV values to each column 
#        device_data_writer.writerow(['IV', MicroIV, AccuIV, windIV, linIV, OmniIV, SpiritIV])
#        #assigning GV values to each column
#        device_data_writer.writerow(['GV', MicroGV, AccuGV, windGV, linGV, OmniGV, SpiritGV])
#        #assigning GST values to each column
#        device_data_writer.writerow(['GST', MicroGST, AccuGST, windGST, linGST, OmniGST, SpiritGST])
#        #assigning GSV values to each column
#        device_data_writer.writerow(['GSV', MicroGSV, AccuGSV, windGSV, linGSV, OmniGSV, SpiritGSV])
#        #assigning NSV values to each column
#        device_data_writer.writerow(['NSV', MicroNSV, AccuNSV, windNSV, linNSV, OmniNSV, SpiritNSV])
#        #assigning CTL values to each column
#        device_data_writer.writerow(['CTL', MicroCTL, AccuCTL, windCTL, linCTL, OMNICTL, SpiritCTL])
#        #assigning CPL values to each column
#        device_data_writer.writerow(['CPL', MicroCPL, AccuCPL, windCPL, linCPL, OMNICPL, SpiritCPL])
#        #assigning CTPL values to each column
#        device_data_writer.writerow(['CTPL', MicroCTPL, AccuCTPL, windCTPL, linCTPL, OMNICTPL, SpiritCTPL])
#        #assigning ref temp to each column
#        device_data_writer.writerow(['Ref. Temp.', MicroRefTemp, AccuRefTemp, windRefTemp, linRefTemp, OMNIRefTemp, SpiritRefTemp])
#        #assigning maintainence temp to each column
#        device_data_writer.writerow(['Main. Temp.', MicroMainTemp, AccuMainTemp, windMainTemp, linMainTemp, OMNIMainTemp, SpiritMainTemp])
#        #assigning Live temp to each column
#        device_data_writer.writerow(['Live Temp.', MicroLiveTemp, AccuLiveTemp, windLiveTemp, linLiveTemp, OMNILiveTemp, SpiritLiveTemp])
#        #assigning average temp to each column
#        device_data_writer.writerow(['Avg. Temp.', MicroAvgTemp, AccuAvgTemp, windAvgTemp, linAvgTemp, OMNIAvgTemp, SpiritAvgTemp])
#        #assigning maintainence pressure to each column
#        device_data_writer.writerow(['Main. Pressure', MicroMainPres, AccuMainPres, windMainPres, linMainPres, OMNIMainPres, SpiritMainPres])
#        #assigning average pressure to each column
#        device_data_writer.writerow(['Avg. Pressure', MicroAvgPres, AccuAvgPres, windAvgPres, linAvgPres, OMNIAvgPres, SpiritAvgPres])
#        #assigning live pressure to each column
#        device_data_writer.writerow(['Live Pressure', MicroLivePres, AccuLivePres, windLivePres, linLivePres, OMNILivePres, SpiritLivePres])
#        #assigning reference density to each column
#        device_data_writer.writerow(['Ref. Density', MicroRefDens, AccuRefDens, windRefDens, linRefDens, OMNIRefDens, SpiritRefDens])
#        #assigning average density to each column
#        device_data_writer.writerow(['Avg. Density', MicroAvgDens, AccuAvgDens, windAvgDens, linAvgDens, OMNIAvgDens, SpiritAvgDens])
#        #assigning live density to each column
#        device_data_writer.writerow(['Live Density', MicroLiveDens, AccuLiveDens, windLiveDens, linLiveDens, OMNILiveDens, SpiritLiveDens])
#        #assigning k factor to each column
#        device_data_writer.writerow(['K Factor', MicroKfactor, AccuKfactor, windkfactor, linkfactor, OMNIKfactor, SpiritKfactor])
#        #assigning meter factor to each column
#        device_data_writer.writerow(['Meter Factor', Micrometerfactor, Accumeterfactor, windmeterfactor, linmeterfactor, OMNImeterfactor, Spiritmeterfactor])
#        #assigning bs&w
#        device_data_writer.writerow(['BS&W', MicroBSW, AccuBSW, windBSW, linBSW, OMNIBSW, SpiritBSW])
#        #assigning mass to each column
#        device_data_writer.writerow(['Mass', Micromass, Accumass, windmass, linmass, OMNImass, Spiritmass])
#        #assigning pulse total to each column
#        device_data_writer.writerow(['Pulse Total', Micropulse, Accupulse, windpulse, linpulse, OMNIpulse, Spiritpulse])
#   #closing the csv file     
#    device_data.close()
#    
    #asking the user if they would like to run the program again
    repeat = input("Would you like to collect data again? (y/n): ")
    
    #will enter this if statement if the user would like to repeat this program
    if repeat == 'y':
        #asking the user if they would like to use the same ips
        ip_repeat = input("Would you like to use the same ip adresse? (y/n): ")
        #will enter this if statement if the user would like to enter new ips
        if ip_repeat == 'n':
            #prompting the user to enter the ip for each device
            ip1 = input("Enter MicroFlow ip address (Press enter if MicroFlow is unused): ")
