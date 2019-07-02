#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Poll System Status registers 

from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.181.76"
SERVER_PORT = 502

c = ModbusClient()

# uncomment this line to see debug message
#c.debug(True)

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
    # read System Status(func 02, regs 4096-4106)
    regs = c.read_discrete_inputs(4096, 11)
    # if success display registers
    if regs:
        print("SYSTEM STATUS" + str(regs))
