#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Read PI (3.14157....)

from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time

import extmod

SERVER_HOST = "192.168.76.76"
SERVER_PORT = 502

#c = ModbusClient()
c = extmod.ExtendedModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True)

# uncomment this line to see debug message
c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

# open or reconnect TCP to server
if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

# open or reconnect TCP to server
if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

# if open() is ok, read coils (modbus function 0x01)
if c.is_open():
    # read PI variable (func 03, reg 2106) 
    result = c.read_float(2106, 1)
    result2 = c.read_double(2108, 2)
    # if success display registers
    if result:
        print("PI (float): " + str(result))
    if result2:
        print("PI (double): " + str(result2))
