#!/usr/bin/env python
# -*- coding: utf-8 -*-

# how-to add float support to ModbusClient
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import float_utils

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


    # The next two functions aren't quite working yet -- MLA 073019
    # These two functions will utilize the float_utils.py module to extend
    # the utils module library for double precision in modbus

    def read_double(self, address, number=1):
        reg_ll = self.read_holding_registers(address, number * 4)
        if reg_ll:
            return [float_utils.decode_ieee_d(d) for d in float_utils.word_list_to_longlong(reg_ll)]
        else:
            return None

    def write_double(self, address, doubles_list):
        b32_l = [utils.encode_ieee_d(d) for d in doubles_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)

#Need to input proper ip adresses!!!
c = FloatModbusClient(host='192.168.181.76', port=502, auto_open=True)
#d = FloatModbusClient(host='192.168.181.206', port=502, auto_open=True)
#e = FloatModbusClient(host='192.168.181.206', port=502, auto_open=True)
#f = FloatModbusClient(host='192.168.181.206', port=502, auto_open=True)
#g = FloatModbusClient(host='192.168.181.206', port=502, auto_open=True)


############################################################
# FROM HERE YOU CAN POLL/WRITE TO REGISTERS AS YOU SEE FIT #
############################################################

#importing needed class for timestamp
import datetime
#importing needed class to output to csv file
import csv

# write 10.0 at @0
#c.write_float(0, [10.0])

# Debug ON
#c.debug(True)

# read bits (true/false)
# print("READ COILS")
# bits = c.read_coils(43,14)
# bitsd = d.read_coils(43,14)
# print(bits)
# print(bitsd)
# 
# # read registers (integers)
# print("READ REGISTERS")
# regs = c.read_holding_registers(0, 10)
# regsd = d.read_holding_registers(0, 10)
# print(regs)
# print(regsd)
# 
# # read PI (IEEE float version)
# print("READ FLOATS")
# float_l = c.read_float(2106, 1)
# float_ld = d.read_float(2106, 1)
# print(float_l)
# print(float_ld)

#pulling the current time to use for timestamp
current_time = datetime.datetime.now()

# read PI (IEEE double version)
print("READING DATA")

#collecting data from microflow(Need modbus addresses!!!!)
#double_MicroIV = c.read_double(4480, 1)
#double_MicroGV = c.read_double(4484, 1)
#double_MicroGST = c.read_double(4488, 1)
#double_MicroGSV = c.read_double(4492, 1)

#collecting data from Accuload
prog_mfac = c.read_float(3, 7698, 1)
float_avg_mfac= c.read_float(4, 4352, 1)
float_avg_temp= c.read_float(4, 4354, 1)
float_avg_dens= c.read_float(4, 4356, 1)
float_avg_press= c.read_float(4, 4358, 1)

#collecting data from LACT (still need modbus addresses!!!!)
#double_LACTIV = e.read_double(4480, 1)
#double_LACTGV = e.read_double(4484, 1)
#double_LACTGST = e.read_double(4488, 1)
#double_LACTGSV = e.read_double(4492, 1)

#collecting data from Omni  (still need modbus addresses!!!!)
#double_OmniIV = f.read_double(4480, 1)
#double_OmniGV = f.read_double(4484, 1)
#double_OmniGST = f.read_double(4488, 1)
#double_OmniGSV = f.read_double(4492, 1)

#collecting data from Spirit  (still need modbus addresses!!!!)
#double_SpiritIV = g.read_double(4480, 1)
#double_SpiritGV = g.read_double(4484, 1)
#double_SpiritGST = g.read_double(4488, 1)
#double_SpiritGSV = g.read_double(4492, 1)

#opening and naming the csv file so it can be written to
with open('LACT_data.csv','a') as LACT_data:
    LACT_data_writer = csv.writer(LACT_data)
    #giving each of the columns a heading
    LACT_data_writer.writerow(['AcculoadIV Load Averages', 'Meter Factor', 'Temperature', 'Density', 'Pressure'])
    LACT_data_writer.writerow([prog_mfac, float_avg_mfac, float_avg_temp, float_avg_dens, float_avg_press])

#    #assigning IV values to each column 
#    LACT_data_writer.writerow(['IV', double_MicroIV, double_AccuIV, double_LACTIV, double_OmniIV, double_SpiritIV, current_time])
#     #assigning GV values to each column
#    LACT_data_writer.writerow(['GV', double_MicroGV, double_AccuGV, double_LACTGV, double_OmniGV, double_SpiritGV, current_time])
#     #assigning GST values to each column
#    LACT_data_writer.writerow(['GST', double_MicroGST, double_AccuGST, double_LACTGST, double_OmniGST, double_SpiritGST, current_time])
#     #assigning GSV values to each column
#    LACT_data_writer.writerow(['GSV', double_MicroGSV, double_AccuGSV, double_LACTGSV, double_OmniGSV, double_SpiritGSV, current_time])


#closing the csv file     
LACT_data.close()
    
# Close the connection when done
c.close()
#d.close()
#e.close()
#f.close()
#g.close()
