#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
import extmod  # updated modbus library that handles floats/doubles/text
import struct

# Define connection parameters
SERVER_HOST = "192.168.76.77"
SERVER_PORT = 502
c = extmod.ExtendedModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True)

# uncomment this line to see debug message
#c.debug(True)

# open or reconnect TCP to server
if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

# if open() is ok
if c.is_open():
    # Send Reset_Batch command to microFlow (40578)
    recipe = int(input("Enter recipe (0 for current): "))

    update = c.write_single_register(40578,recipe)
    if update:
        result = c.read_input_registers(3590,1)

    # Read Transaction Log (one that just got archived)
    update = c.write_single_register(40587,1)
    if update:
        result = c.read_input_registers(3590,1)
        
        end_time_text   = c.read_text(4, 2384, 16)
        start_time_text = c.read_text(4, 2400, 16)
        avg_mfac        = c.read_float(4, 2816)
        k_factor        = c.read_double(3, 23552)
        avg_ctl         = c.read_float(4, 4874)
        avg_cpl         = c.read_float(4, 4876)
        avg_ctpl        = c.read_float(4, 4888)
        avg_ccf         = c.read_float(4, 4878)
        total_pulses    = c.read_double(4, 5120)
        cur_raw         = c.read_double(4, 5124)
        cur_grs         = c.read_double(4, 5128)
        cur_gsv         = c.read_double(4, 5136)

        print(str(start_time_text))
        print(str(end_time_text))
        print(str(avg_mfac))
        print(str(k_factor))
        print(str(avg_ctl))
        print(str(avg_cpl))
        print(str(avg_ctpl))
        print(str(avg_ccf))
        print(str(total_pulses))
        print(str(cur_raw))
        print(str(cur_grs))
        print(str(cur_gsv))

    















    
