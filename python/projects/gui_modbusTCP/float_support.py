#!/usr/bin/env python
# -*- coding: utf-8 -*-

# how-to add float support to ModbusClient

import inspect
from pyModbusTCP.client import ModbusClient
#from pyModbusTCP import utils
import utils

# print inspect.getmodule(utils)

 
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

    def read_double(self, address, number=1):
        reg_ll = self.read_holding_registers(address, number * 4)
        if reg_ll:
            return [utils.decode_ieee_d(d) for d in utils.word_list_to_longlong(reg_ll)]
        else:
            return None

    def write_double(self, address, doubles_list):
        b32_l = [utils.encode_ieee(d) for d in doubles_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)

c = FloatModbusClient(host='192.168.1.24', port=502, auto_open=True)

# write 10.0 at @0
#c.write_float(0, [10.0])

# Debug ON
c.debug(True)

# read PI (float & double versions)
float_l = c.read_float(2106, 1)
print(float_l)

double_l = c.read_double(2108, 1)
print(double_l)

c.close()
