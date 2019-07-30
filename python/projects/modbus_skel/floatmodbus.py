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

    def read_double(self, address, number=1):
        reg_ll = self.read_holding_registers(address, number * 4)
        if reg_ll:
            return [float_utils.decode_ieee_d(d) for d in float_utils.word_list_to_longlong(reg_ll)]
        else:
            return None

    def write_double(self, address, doubles_list):
        b32_l = [float_utils.encode_ieee_d(d) for d in doubles_list]
        b16_l = float_utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)
