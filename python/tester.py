#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyModbusTCP.client import ModbusClient
import time, struct, datetime, csv, random

import accuload
import inspect

inspect.getfile(ModbusClient)
print(accuload.__file__)


AL3_HOST = "192.168.76.1"
SERVER_PORT = 502

c = accuload.Connect(host=AL3_HOST, port=SERVER_PORT)

# Allocate Batch

# Set Batch

# Start Batch

# Poll Transaction Info
flags = accuload.TransactionStatus(c)
print(flags)

# Poll System Info

# End Batch
status = accuload.EndBatch(c)
print(status)

# End Transaction



