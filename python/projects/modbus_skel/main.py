#!/usr/bin/env python
# -*- coding: utf-8 -*-

# how-to add float support to ModbusClient
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import float_utils

class FloatModbusClient(ModbusClient):
    def read_float(self, address, number=1):
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

c = FloatModbusClient(host='192.168.181.76', port=502, auto_open=True)
d = FloatModbusClient(host='192.168.181.206', port=502, auto_open=True)


############################################################
# FROM HERE YOU CAN POLL/WRITE TO REGISTERS AS YOU SEE FIT #
############################################################

# write 10.0 at @0
#c.write_float(0, [10.0])

# Debug ON
#c.debug(True)

# read bits (true/false)
print("READ COILS")
bits = c.read_coils(43,14)
bitsd = d.read_coils(43,14)
print(bits)
print(bitsd)

# read registers (integers)
print("READ REGISTERS")
regs = c.read_holding_registers(0, 10)
regsd = d.read_holding_registers(0, 10)
print(regs)
print(regsd)

# read PI (IEEE float version)
print("READ FLOATS")
float_l = c.read_float(2106, 1)
float_ld = d.read_float(2106, 1)
print(float_l)
print(float_ld)

# read PI (IEEE double version)
print("READ DOUBLES")
double_l = c.read_double(2108, 1)
print(str(double_l) + "  <--Double IEEE precision isn't working yet...")

# Close the connection when done
c.close()
