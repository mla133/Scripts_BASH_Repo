from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import struct

################################################################################################################
#    functions for decoding long/text/float/double
################################################################################################################

def decode_ieee(val_int):
   return struct.unpack("f", struct.pack("I", val_int))[0]

def decode_ieee_double(val_int):
   return struct.unpack("d", struct.pack("q", val_int))[0]

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
#   End of data decoding functions
#################################################################################################################################

class ExtendedModbusClient(ModbusClient):
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

    def read_text(self, reg_type, address, number=1):
        if reg_type == 4:
            reg_t = self.read_input_registers(address, number)
        else:
            reg_t = self.read_holding_registers(address, number)
        if reg_t:
            split_regs = list()

            # Run through reg list returned by read_holding registers, and split off
            # the 'XXXX' per register into 'XX' 'XX' by shifting and masking
            # then recombine them into a split_regs list
            for i, item in enumerate(reg_t):
                split_regs.append(reg_t[i] >> 8)
                split_regs.append(reg_t[i] & 0xff)

            # convert the split_regs list into its ASCII form
            ascii_list = [chr(c) for c in split_regs]

            # convert the split_regs list into a string
            s = ''.join(map(str,ascii_list))
            return(s)
        else:
            return None