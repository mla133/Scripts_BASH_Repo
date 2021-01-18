from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import struct
import extmod

def Connect(host, port, unit_id):
	c = extmod.ExtendedModbusClient(host=host, port=502, unit_id=unit_id, auto_open=True)
	# open or reconnect TCP to server
	if not c.is_open():
		if not c.open():
			print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

	return c

def EndBatch(conn):
	# 0x0400 EB variant, end batch...
	command = conn.write_multiple_registers(0, [4, 0x0400, 4])
	update = conn.write_single_coil(4096,1)
	EB_result = conn.read_input_registers(0, 4)
	return str(hex(EB_result[2]))

def TransactionStatus(conn):
	status = conn.read_discrete_inputs(4160, 17)
	return status