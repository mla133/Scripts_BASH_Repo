import socket
import struct
import time
import array
import binascii
import sys
import argparse
import sqlite3
import os
import random


#################################################################################################################
# Define arguments
#################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-f","--infile",type=str, 
	help="Name of an input file")
parser.add_argument("-o","--outfile",type=str, 
	help="Name of an output file")
parser.add_argument("-i","--ipaddr",type=str,
	help="IP address")
parser.add_argument("-a","--arm",type=str,
	help="Arm number")
parser.add_argument("-t","--threeip",type=str,
	help="AL3 IP address")
parser.add_argument("-d","--debug",
	help="Debug output level",type=int)
parser.add_argument("-m","--mode",type=str,
	help="Mode: F1=Function 1, n=native (functions 2&4), F3=Function 3, r=remote read, b=backwards compatability, c=console, set=set config, EX=Extended services, EXf=Extended services (file mode)")
args = parser.parse_args()


#################################################################################################################
# Handle arguments
#################################################################################################################

print "**********************************************************************************\n\t\t\t\tModTCP started!\n"
if not args.mode == 'c':
	if not args.infile:
		print "Input file must be specified!\nClosing..."
		sys.exit(1)
	else:
		print "Input from:\t",args.infile
		infile = args.infile

	if not args.outfile:
		print "Output to:\tModTCPout.txt"
		outfile = "ModTCPout.txt"
	else:
		print args.outfile
		outfile = args.outfile

	try:
		inputfile = open(infile, 'r')
		outputfile = open(outfile, 'w')
	except:
		print "Could not open file, closing..."
		sys.exit(1)

	if not args.arm:
		print "An arm must be specified!\nClosing..."
		sys.exit(1)
	elif len(args.arm)>2:
		print "Invalid arm value!\nClosing..."
		sys.exit(1)
	else:
		arm = args.arm.zfill(2)

if not args.ipaddr:
	ALIVIP = 'localhost'
else:
	ALIVIP = args.ipaddr
print "ALIV IP:\t",ALIVIP

if args.mode == 'b':
	AL3IP = args.threeip
	print "AL3 IP:\t\t",AL3IP

if args.debug:
	debug=args.debug
else:
	debug=0


#################################################################################################################
# Open socket connections and databases
#################################################################################################################

MPort = 502
BUFF_SIZE = 2048
ALIV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
AL3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	ALIV.connect((ALIVIP,MPort))
	ALIV.settimeout(2)
	if args.mode == 'b':
		AL3.connect((AL3IP,MPort))
		AL3.settimeout(2)
except:
	print "Could not open port!"
	sys.exit(1)

try:
	pdb = sqlite3.connect('/dev/shm/pdb_edit_buf.sqlite')
	rdb = sqlite3.connect('/dev/shm/accu4_db_ram.sqlite')
	ldb = sqlite3.connect('/media/data/database/accu4_datalog.sqlite')
except:
	print "Database connection error!"
	sys.exit(1)

timeout=0
data = ""
out = ""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#################################################################################################################
# Error dict for extended services
#################################################################################################################
errors = {
0x0000	:	"ROUTE_NO_ERROR",
0x0001	:	"ROUTE_DOWNLOAD_SUCCESSFUL",
0x8000	:	"ROUTE_EMPTY_CONFIG",
0x8001	:	"ROUTE_BLOCK_NOT_FOUND",
0x8002	:	"ROUTE_BAD_MESSAGE_FORMAT",
0x8003	:	"ROUTE_BLOCK_OUT_OF_SEQUENCE",
0x8004	:	"ROUTE_INVALID_FLASH_DATA",
0x8005	:	"ROUTE_TARGET_BUFFER_TOO_SMALL",
0x8006	:	"ROUTE_BAD_CRC",
0x8007	:	"ROUTE_NO_CONFIG_AVAIL",
0x8008	:	"ROUTE_DOWNLOAD_ALREADY_IN_PROGRESS",
0x8009	:	"ROUTE_BAD_DATABASE_SPEC",
0x800a	:	"ROUTE_IN_PROG_MODE",
0x800b	:	"ROUTE_RELEASED",
0x800c	:	"ROUTE_BAD_VALUE",
0x800d	:	"ROUTE_FLOW_ACTIVE",
0x800e	:	"ROUTE_NO_TRANSACTIONS_EVER_DONE",
0x800f	:	"ROUTE_OPERATION_NOT_ALLOWED",
0x8010	:	"ROUTE_WRONG_CONTROL_MODE",
0x8011	:	"ROUTE_TRANSACTION_IN_PROGRESS",
0x8012	:	"ROUTE_ALARM_ACTIVE",
0x8013	:	"ROUTE_STORAGE_FULL",
0x8014	:	"ROUTE_OPERATION_OUT_OF_SEQUENCE",
0x8015	:	"ROUTE_POWER_FAIL_DURING_TRANS",
0x8016	:	"ROUTE_AUTHORIZED",
0x8017	:	"ROUTE_PROGRAM_CODE_NOT_USED",
0x8018	:	"ROUTE_DISP_KEY_IN_REMOTE_CONTROL",
0x8019	:	"ROUTE_TICKET_NOT_IN_PRINTER",
0x801a	:	"ROUTE_NO_KEY_DATA_PENDING",
0x801b	:	"ROUTE_NO_TRANS_IN_PROGRESS",
0x801c	:	"ROUTE_OPTION_NOT_INSTALLED",
0x801d	:	"ROUTE_START_AFTER_STOP_DELAY",
0x801e	:	"ROUTE_PERMISSIVE_DELAY_ACTIVE",
0x801f	:	"ROUTE_PRINT_REQUEST_PENDING",
0x8020	:	"ROUTE_NO_METER_ENABLED",
0x8021	:	"ROUTE_MUST_BE_IN_PROG_MODE",
0x8022	:	"ROUTE_TICKET_ALARM_DURING_TRANS",
0x8023	:	"ROUTE_VOLUME_TYPE_NOT_SELECTED",
0x8024	:	"ROUTE_EXACTLY_ONE_REC_MUST_BE_ENABLED",
0x8025	:	"ROUTE_BATCH_LIMIT_REACHED",
0x8026	:	"ROUTE_CHECKING_ENTRIES",
0x8027	:	"ROUTE_PROD_REC_ADD_NOT_ASSIGNED",
0x8028	:	"ROUTE_MUST_USE_MINI_PROTOCOL",
0x8029	:	"ROUTE_BUFFER_ERROR",
0x802a	:	"ROUTE_KEYPAD_LOCKED",
0x802b	:	"ROUTE_DATA_RECALL_ERROR",
0x802c	:	"ROUTE_INTERNAL_ERROR",
0x802d	:	"ROUTE_TRANSMIT_REPLY",
0x802e	:	"ROUTE_UNKNOWN_ERROR",
0x802f	:	"ROUTE_UNUSED_BATCH",
0x8030	:	"ROUTE_PACKING_FLASH",
0x8031	:	"ROUTE_DATA_NOT_AVAILABLE",
0x8032	:	"ROUTE_CARD_IN_REQUIRED",
0x8033	:	"ROUTE_TOO_MANY_SHARED_ADDITIVES",
0x8034	:	"ROUTE_MAX_ACTIVE_ARMS_IN_USE",
0x8035	:	"ROUTE_TRANSACTION_NOT_STANDBY",
0x8036	:	"ROUTE_SWING_ARM_OUT_OF_POSITION",
0x8037	:	"ROUTE_NO_CURRENT_BATCH_ON_THIS_ARM",
0x8038	:	"ROUTE_DATA_REQUEST_QUEUED_ASK_LATER",
0x8039	:	"ROUTE_COMFLASH_ARCHIVING",
0x803a	:	"ROUTE_CONFLICTS_WITH_ARM_CONFIG",
0x803b	:	"ROUTE_NO_PENDING_REPORTS",
0x803c	:	"ROUTE_NO_KEY_EVER_PRESSED",
0x803d	:	"ROUTE_DATABASE_ACCESS_ERROR",
0x803e	:	"ROUTE_ABORT",
0x803f	:	"ROUTE_SECURITY_ACCESS_NOT_AVAILABLE",
0x8040	:	"ROUTE_NOT_IN_PROGRAM_MODE",
0x8041	:	"ROUTE_VALVE_OPENING_DELAY",
0x8042	:	"ROUTE_INVALID_ON_VIRTUAL_ARM",
0xc000	:	"ROUTE_INTERNAL_FLASH_ERROR",
0xc001	:	"ROUTE_FLASH_HAS_OVERRUN",
0xc002	:	"ROUTE_INTERNAL_BUFFER_ERROR",
0xc003	:	"ROUTE_BUFFER_ALLOCATION_ERROR",
0xc004	:	"ROUTE_BUFFER_OVERRUN",
0xc005	:	"ROUTE_FLASH_ERASE_ERROR",
0xc006	:	"ROUTE_FLASH_WRITE_ERROR"
}


print "**********************************************************************************\n\n"


#################################################################################################################
# Define functions
#################################################################################################################



##############################################################################################

########							Function send_command					##################

##############################################################################################
def send_command ( incoming ):

	# check modbus query OK
	try:
		incoming = arm + incoming
		int(incoming,16)
		if len(incoming)%2:
			raise ValueError("derp")
	except:
		print bcolors.WARNING+"Input is invalid! "+bcolors.ENDC,incoming
		outputfile.write("Input is invalid")
		return "-1"

	# Format modbus query
	incoming = "00000000"+str("{0:0>4}".format(format(len(incoming),'x')))+incoming
	out = incoming.decode("hex")

	# Send modbus query, get response
	try:
		ALIV.send(out)
		data = ALIV.recv(BUFF_SIZE)

	except socket.timeout:
		print bcolors.WARNING+"Timed out",
		print bcolors.ENDC
		outputfile.write("Timed out\n")
		return "-1"

	# Parse response, convert to something useful
	data = data[6:]
	string = data.encode("hex")

	if len(string)<6:
		print bcolors.WARNING+"Response too short..."+bcolors.ENDC,string,", out: ",incoming
		outputfile.write("Response too short...\n")
		return "-1"

	# Error response recognition
	if (int(string[2],16)&0x8) == 8:
		print bcolors.FAIL+"ERROR RESPONSE:\t",
		outputfile.write("ERROR RESPONSE: ")
		if string[5] == '1':
			print "ILLEGAL FUNCTION",
			outputfile.write("ILLEGAL FUNCTION\n")
		elif string[5] == '2':
			print "ILLEGAL DATA ADDRESS",
			outputfile.write("ILLEGAL DATA ADDRESS\n")
		elif string[5] == '3':
			print "ILLEGAL DATA VALUE",
			outputfile.write("ILLEGAL DATA VALUE\n")
		elif string[5] == '4':
			print "SERVER DEVICE FAILURE",
			outputfile.write("SERVER DEVICE FAILURE\n")
		elif string[5] == '6':
			print "SERVER DEVICE BUSY",
			outputfile.write("SERVER DEVICE BUSY\n")
		print bcolors.ENDC
		return "-1"
	return string


##############################################################################################

########							Function send_both						##################

##############################################################################################
def send_both ( incoming ):

	# check modbus query OK
	try:
		incoming = arm + incoming
		int(incoming,16)
		if len(incoming)%2:
			raise ValueError("derp")
	except:
		print bcolors.WARNING+"Input is invalid!"+bcolors.ENDC
		outputfile.write("Input is invalid")
		return "-1"

	# Format modbus query
	incoming = "00000000"+str("{0:0>4}".format(format(len(incoming),'x')))+incoming
	out = incoming.decode("hex")

	# Send modbus query, get response
	try:
		ALIV.send(out)
		data = ALIV.recv(BUFF_SIZE)
		AL3.send(out)
		data3 = AL3.recv(BUFF_SIZE)

	except socket.timeout:
		print bcolors.WARNING+"Timed out",
		print bcolors.ENDC
		return "-1"

	# Parse response, convert to something useful
	data = data[6:]
	data3 = data3[6:]
	string = data.encode("hex")
	string3 = data3.encode("hex")

	if len(string)<6 or len(string3)<6:
		print bcolors.WARNING+"Response too short..."+bcolors.ENDC
		outputfile.write("Response too short...\n")
		return "-1"

	# Error response recognition
	if (int(string[2],16)&0x8) == 8:
		print bcolors.FAIL+"ERROR RESPONSE:\t",
		outputfile.write("ERROR RESPONSE: ")
		if string[5] == '1':
			print "ILLEGAL FUNCTION",
			outputfile.write("ILLEGAL FUNCTION\n")
		elif string[5] == '2':
			print "ILLEGAL DATA ADDRESS",
			outputfile.write("ILLEGAL DATA ADDRESS\n")
		elif string[5] == '3':
			print "ILLEGAL DATA VALUE",
			outputfile.write("ILLEGAL DATA VALUE\n")
		elif string[5] == '4':
			print "SERVER DEVICE FAILURE",
			outputfile.write("SERVER DEVICE FAILURE\n")
		elif string[5] == '6':
			print "SERVER DEVICE BUSY",
			outputfile.write("SERVER DEVICE BUSY\n")
		print bcolors.ENDC
		return "-1"

	if (int(string3[2],16)&0x8) == 8:
		print bcolors.FAIL+"ERROR RESPONSE:\t",
		outputfile.write("ERROR RESPONSE: ")
		if string3[5] == '1':
			print "ILLEGAL FUNCTION",
			outputfile.write("ILLEGAL FUNCTION\n")
		elif string3[5] == '2':
			print "ILLEGAL DATA ADDRESS",
			outputfile.write("ILLEGAL DATA ADDRESS\n")
		elif string3[5] == '3':
			print "ILLEGAL DATA VALUE",
			outputfile.write("ILLEGAL DATA VALUE\n")
		elif string3[5] == '4':
			print "SERVER DEVICE FAILURE",
			outputfile.write("SERVER DEVICE FAILURE\n")
		elif string3[5] == '6':
			print "SERVER DEVICE BUSY",
			outputfile.write("SERVER DEVICE BUSY\n")
		print bcolors.ENDC
		return "-1"

	return string,string3


##############################################################################################

########							Function check_string					##################

##############################################################################################
def check_string(data, dbName, dbTable, dbColumn, Number, incoming):

	# Range check input
	passed = True
	for i in range(0,len(data), 2):
		if data[i:i+2]=="00":
			data = data[0:i]
	nice_data = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))
	
	# Check the database against what modbus told us, save the old value and put in garbage
	try:
		if dbName == "rdb":
			rand = str(random.randint(0,65535))
			query = "SELECT "+dbColumn+" FROM "+dbTable+" WHERE "+identifier+" = "+Number
			if debug > 2:
				print query
				outputfile.write(query)
			rdb_c.execute(query)
			fetched = rdb_c.fetchone()
			if fetched is not None:
				old_data = fetched[0]
			else:
				old_data = ""

			if debug>0:
				print "nice_data: ",nice_data,", old_data: ",old_data
				outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

			if not nice_data == old_data:
				passed = False
				outputfile.write("\t****ERROR**** ")
				outputfile.write("- Value in database does not match what Modbus reported")
				outputfile.write("nice_data: ",nice_data,", old_data: ",old_data)
			query = "UPDATE "+dbTable+" SET "+dbColumn+" = \""+str(rand)+"\" WHERE "+identifier+" = "+Number
			if debug > 2:
				print query
				outputfile.write("\n\t"+query)
			rdb_c.execute(query)
			rdb.commit()
		
		# Same thing but for the parameter database
		elif dbName == "pdb":
			rand = str(random.randint(0,65535))
			query = "SELECT "+dbColumn+" FROM "+dbTable+" WHERE "+identifier+" = "+Number
			if debug > 2:
				print query
				outputfile.write("\n\t"+query)
			pdb_c.execute(query)
			fetched = pdb_c.fetchone()
			if fetched is not None:
				old_data = fetched[0]
			else:
				old_data = ""

			if debug>0:
				print "nice_data: ",nice_data,", old_data: ",old_data
				outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

			if not nice_data == old_data:
				passed = False
				outputfile.write("\t****ERROR**** ")
				outputfile.write("- Value in database does not match what Modbus reported")
				outputfile.write("nice_data: ",nice_data,", old_data: ",old_data)
			query = "UPDATE "+dbTable+" SET "+dbColumn+" = \""+str(rand)+"\" WHERE "+identifier+" = "+Number
			if debug > 2:
				print query
				outputfile.write("\n\t"+query)
			pdb_c.execute(query)
			pdb.commit()
		
		# Same thing but for the log database
		elif dbName == "ldb":
			rand = str(random.randint(0,65535))
			query = "SELECT "+dbColumn+" FROM "+dbTable+" WHERE "+identifier+" = "+Number
			if debug > 2:
				print query
				outputfile.write("\n\t"+query)
			ldb_c.execute(query)
			fetched = ldb_c.fetchone()
			if fetched is not None:
				old_data = fetched[0]
			else:
				old_data = ""

			if debug>0:
				print "nice_data: ",nice_data,", old_data: ",old_data
				outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

			if not nice_data == old_data:
				passed = False
				outputfile.write("\t****ERROR**** ")
				outputfile.write("- Value in database does not match what Modbus reported")
				outputfile.write("nice_data: ",nice_data,", old_data: ",old_data)
			query = "UPDATE "+dbTable+" SET "+dbColumn+" = \""+str(rand)+"\" WHERE "+identifier+" = "+Number
			if debug > 2:
				print query
				outputfile.write("\n\t"+query)
			ldb_c.execute(query)
			ldb.commit()
	except TypeError as e:
		outputfile.write("- Database error!"+str(e)+"\n")
		print e," - TypeError - check string"
		return
	except Exception as e:
		outputfile.write("- Database error!"+str(e)+"\n")
		print e," - check string"
		return
	except:
		outputfile.write("General exception caught.\n")
		print "General exception caught."
		return


	string = send_command(incoming)
	if string == "-1":
		return

	data = string[6:]
	for i in range(0,len(data), 2):
		if data[i:i+2]=="00":
			data = data[0:i]
	nice_data = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

	if debug>0:
		print "nice_data: ",nice_data,", rand: ",rand
		outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

	if not nice_data == rand:
		print "n= ",nice_data,", r= ",rand
		passed = False
		outputfile.write("\t****ERROR**** ")
		outputfile.write("- Reported value did not change with the database")
		outputfile.write("\n\tnice_data: "+str(nice_data)+", rand: "+str(rand))

	try:
		query = "UPDATE "+dbTable+" SET "+dbColumn+" = \""+str(old_data)+"\" WHERE "+identifier+" = "+Number
		if debug > 2:
			print query
			outputfile.write("\n\t"+query)

		if dbName == "rdb":
			rdb_c.execute(query)
			rdb.commit()
		if dbName == "pdb":
			pdb_c.execute(query)
			pdb.commit()
		if dbName == "ldb":
			ldb_c.execute(query)
			ldb.commit()
	except TypeError as e:
		outputfile.write("- Database error!"+str(e)+"\n")
		print e
		return
	except Exception as e:
		outputfile.write("- Database error!"+str(e)+"\n")
		print e
		return
	except:
		outputfile.write("General exception caught.\n")
		print "General exception caught."
		return

	if passed:
		outputfile.write("\nOK")
		print bcolors.OKGREEN+"OK"+bcolors.ENDC
	else:
		outputfile.write("\t****ERROR****\n")
		print bcolors.FAIL+"fxn {} reg {}".format(incoming[:2],int(incoming[2:6],16))+bcolors.ENDC


##############################################################################################

########							Function send_ext_packet				##################

##############################################################################################
def send_ext_packet ( packet_out ):
	
	# Do some length checks
	if (len(packet_out) % 2):
		print "Odd number of bytes, try again"
		return "-1"
	pkt_bytes = "%x" % (len(packet_out)/2)
	if ((len(packet_out)/2)>1024):
		return "-1"

	# print "We have",pkt_bytes,"valid bytes"

	# Put packet length in register 0
	response = send_command("060000"+pkt_bytes.zfill(4))
	if response == "-1":
		print "Cannot write length!"
		return "-1"

	## Write packet into modbus registers
	# Break it into the largest chunks we can send
	addr = 1
	while len(packet_out) > 492:
		HexAddr = "%x" % addr
		response = send_command("10"+HexAddr.zfill(4)+"007bf6"+packet_out[:492])
		if response == "-1":
			return "-1"
		packet_out = packet_out[492:]
		addr += 123
		# print response

	# Send the remainder
	rem_bytes = "%x" % (len(packet_out)/2)
	rem_regs = "%x" % (len(packet_out)/4)
	HexAddr = "%x" % addr
	response = send_command("10"+HexAddr.zfill(4)+rem_regs.zfill(4)+rem_bytes.zfill(2)+packet_out)
	if response == "-1":
		return "-1"
	# print response

	## Hit the coil!
	send_command("051000FF00")
	if response == "-1":
		return "-1"

	## Assemble the response packet
	# Read register 0 to see how many valid bytes we have
	response = send_command("0400000001")
	if response == "-1":
		return "-1"
	response_bytes = int(response[6:],16)
	if debug > 0:
		print "we got ",response_bytes,"valid bytes"
	if response_bytes == 0:
		print "0 response bytes!"
		return "-1"
	elif response_bytes == 1:
		response_bytes = 2
	response_packet = ""
	addr = 1

	# Grab them in the biggest chunks we can!
	while response_bytes > 246:
		HexAddr = "%x" % addr
		response = send_command("04"+HexAddr.zfill(4)+"007b")
		if response == "-1":
			return "-1"
		response_packet += response[6:]
		response_bytes -= 246
		addr += 123

	# Grab the rest
	HexAddr = "%x" % addr
	num_bytes = "%x" % (response_bytes/2)
	response = send_command("04"+HexAddr.zfill(4)+num_bytes.zfill(4))
	if response == "-1":
		return "-1"
	response_packet += response[6:]

	# Check for error response
	try:
		router_bits = int(response_packet[:1],16) & 3
		# print "router: ",router_bits,", bitmask: ", router_bits
		if router_bits == 1:
			raise ValueError("\nError! - Service does not exist")
		elif router_bits == 2:
			raise ValueError("\nError! - Router error")
		elif router_bits == 3:
			raise ValueError("\nRouter ANGRY")

		# print int(response_packet[4:8],16),", ",response_packet[4:8]
		error_code = errors[int(response_packet[4:8],16)]

		if error_code == "ROUTE_NO_ERROR":
			print "\n"+bcolors.OKGREEN+error_code+bcolors.ENDC+"\n"
		else:
			print "\n"+bcolors.FAIL+error_code+bcolors.ENDC+"\n"
		# return errors[response_packet[5:]]

	except ValueError as e:
		print bcolors.FAIL+str(e)+bcolors.ENDC+"\n"
	except:
		# Return the response packet
		# return response_packet
		print bcolors.FAIL+"\nError! - Invalid response code!"+bcolors.ENDC+"\n"
	return response_packet



#################################################################################################################

# Program start

#################################################################################################################


#################################################################################################################
# Terminal Mode
#################################################################################################################
if args.mode == 'c':
	print bcolors.HEADER+"Enter 0x before raw hex input, otherwise format is as follows:\n"
	print "----------------------------------------------------------------------------------------------------------"
	print "Functions |\t1 & 2:\t<unit addr>\t<1 or 2>\t<coil addr>\t<quantity>"
	print "----------------------------------------------------------------------------------------------------------"
	print "\t  |\t3 & 4:\t<unit addr>\t<3 or 4>\t<reg addr>\t<quantity>"
	print "----------------------------------------------------------------------------------------------------------"
	print "\t  |\t5:\t<unit addr>\t<5>\t\t<coil addr>\t<value>"
	print "----------------------------------------------------------------------------------------------------------"
	print "\t  |\t6:\t<unit addr>\t<6>\t\t<reg addr>\t<value>"
	print "----------------------------------------------------------------------------------------------------------"
	print "\t  |\t15:\t<unit addr>\t<15>\t\t<coil addr>\t<value 1> <value 2> ... <value n>"
	print "----------------------------------------------------------------------------------------------------------"
	print "\t  |\t16:\t<unit addr>\t<16>\t\t<reg addr>\t<value 1> <value 2> ... <value n>"
	print "----------------------------------------------------------------------------------------------------------"
	print "\t\tinput for <value> is int, for float prefix with f, d for double (e.g. \"f123.456\")"
	print "\t\tcoils are 0 or 1, obviously\n"+bcolors.ENDC
while args.mode == 'c':

	# Grab input
	incoming = raw_input("Your command? : ")

	# Handle it!
	try:
		# Null input
		if incoming == "":
			continue

		# Quit
		elif incoming[0].upper() == 'Q':
			print "Exiting ..."
			raise ValueError("quit")

		# Raw hex, should be formatted already
		elif incoming[1].upper() == 'X':
			incoming = incoming.replace(" ","")
			incoming = incoming[2:]

		# Format input per instructions above
		else:
			print "Interpreting input..."
			in_list = incoming.split()
			incoming = data = ""
			index = 0
			for temp in in_list:
				if (index == 0) or (index == 1):
					tempHex = "%x" % int(temp)
					incoming = incoming+tempHex.zfill(2)
				elif (index == 2):
					tempHex = "%x" % int(temp)
					incoming = incoming+tempHex.zfill(4)
				else:
					if temp[0] == 'f':
						tempHex = struct.pack('!f',float(temp[1:]))
						tempHex = tempHex.encode("hex")
						data = data+tempHex.zfill(8)
					elif temp[0] == 'd':
						tempHex = struct.pack('!d',float(temp[1:]))
						tempHex = tempHex.encode("hex")
						data = data+tempHex.zfill(16)
					else:
						tempHex = "%x" % int(temp)
						data = data+tempHex.zfill(4)
				index += 1

			function = incoming[2:4]

			if function == "10":
				bytecount = "%x" % (len(data)/2)
				regcount = "%x" % (len(data)/4)
				incoming = incoming+regcount.zfill(4)+bytecount.zfill(2)+data

			elif function == "0f":
				index = 0
				temp = []
				data = data[3::4]
				for coil in data:
					if (index % 8) == 0:
						temp.append(0)
					temp[-1] |= (int(coil)<<(index%8))
					index += 1
				data = ""
				for block in temp:
					hexBlock = "%x" % block
					data += hexBlock.zfill(2)
				bytecount = "%x" % (len(data)/2)
				outputQty = "%x" % (index+1)
				incoming = incoming + outputQty.zfill(4) + bytecount.zfill(2) + data

			else:
				if function == "05" and data == "0001":
					data = "FF00"
				incoming = incoming+data
				if len(incoming) > 12:
					print bcolors.WARNING+"Invalid input: "+bcolors.ENDC+"("+incoming+")"
					continue
	
	except ValueError as e:
		if str(e)=="quit":
			ALIV.close()
			pdb.close()
			rdb.close()
			ldb.close()
			sys.exit(1)
		print bcolors.WARNING+str(e)
		print "Input error\n"+bcolors.ENDC
		continue

	except Exception as e:
		print bcolors.WARNING+str(e)
		print "Input error\n"+bcolors.ENDC
		continue

	print "Raw hex query: ",incoming

	# Range check the address
	try:
		target_address = int(incoming[4:8],16)
		int(incoming,16)
		if len(incoming)%2:
			raise ValueError("derp")
	except:
		print bcolors.WARNING+"Input is invalid!\n"+bcolors.ENDC
		continue
		
	# Turn the string into hex and send
	incoming = "00000000"+str("{0:0>4}".format(format(len(incoming),'x')))+incoming
	out = incoming.decode("hex")
	ALIV.send(out)

	# Get!
	try:
		data = ALIV.recv(BUFF_SIZE)

	except socket.timeout:
		timeout+=1
		print bcolors.WARNING+"Timed out %i time(s)\n" % timeout,
		print bcolors.ENDC
		continue

	# Hex into string
	data = data[6:]
	string = data.encode("hex")

	if len(string)<6:
		print bcolors.WARNING+"Response too short...\n"+bcolors.ENDC
		continue

	# Error handling
	if (int(string[2],16)&0x8) == 8:
		print bcolors.FAIL+"ERROR RESPONSE:\t",
		if string[5] == '1':
			print "ILLEGAL FUNCTION\n",
		elif string[5] == '2':
			print "ILLEGAL DATA ADDRESS\n",
		elif string[5] == '3':
			print "ILLEGAL DATA VALUE\n",
		elif string[5] == '4':
			print "SERVER DEVICE FAILURE\n",
		elif string[5] == '6':
			print "SERVER DEVICE BUSY\n",
		print bcolors.ENDC
		continue

	# Make the output a little more readable
	out = "Raw hex input:\n"
	j = 0
	for it in string:
		out += it
		j+=1
		if j%4==0:
			out += " "
		if j%8==0:
			out += " "
		if j%16==0:
			out += " "
		if j%64==0:
			out += "\n"

	print bcolors.OKGREEN+out+'\n'

	if function == "01" or function == "02":
		print "Formatted output:\n"

	# Fancy display for registers
	elif function == "03" or function == "04":
		print "Formatted output:\n"
		print "reg\t\tchar\t\tint\t\tfloat\t\t\tdouble"
		print "______\t\t______\t\t______\t\t______\t\t\t______"
		string = string[6:]
		j=0
		listicle = []
		for block in range(0,len(string),4):
			listicle.append(string[block:block+4])
		lastreg = tempint = lasttempint = ""
		regfloat = 0
		for register in listicle:
			if (j-3)%4 == 0:
				lasttempint = lasttempint+lastreg+register
				doubled = struct.unpack('!d', lasttempint.decode('hex'))[0]
				tempint = lastreg+register
				regfloat = struct.unpack('!f', tempint.decode('hex'))[0]
				lasttempint = ""
				print j+target_address,"\t\t",chr(int(register[:-2],16)),chr(int(register[2:],16)),"\t\t",int(register,16),"\t\t",regfloat,"\n\t\t\t\t\t\t\t\t\t",doubled
			elif j%2 == 1:
				tempint = lastreg+register
				regfloat = struct.unpack('!f', tempint.decode('hex'))[0]
				lasttempint += tempint
				lastreg = ""
				print j+target_address,"\t\t",chr(int(register[:-2],16)),chr(int(register[2:],16)),"\t\t",int(register,16),"\t\t",regfloat
			else:
				print j+target_address,"\t\t",chr(int(register[:-2],16)),chr(int(register[2:],16)),"\t\t",int(register,16)
			tempint = ""
			lastreg = register
			j += 1


	print bcolors.ENDC


#################################################################################################################
# Native mode
# Code to run on BBB, checking modbus against the database
#################################################################################################################
if args.mode == 'n':
	random.seed()
	pdb_c = pdb.cursor()
	rdb_c = rdb.cursor()
	ldb_c = ldb.cursor()
	i = 0
	for line in inputfile:
		i+=1
		passed = True
		string = data = transNO = batchNO = ""
		alist = line.split()

		# Process comments
		if len(alist)==0:
			continue
		if alist[0][0] == '#':
			outputfile.write("\n")
			for it in alist:
				print it,
				outputfile.write(it+" ")
			print " "
			continue
		if alist[0][0] == "/":
			continue

		# Get information from the file
		incoming = ""
		dbTable = dbColumn = Number = dbName = datatype = "NOPE"
		index = 0
		for it in alist:
			if (not it == '#') and (index == 0):
				incoming += it
				continue
			elif index == 1:
				dbName = it
			elif index == 2:
				dbTable = it
			elif index == 3:
				dbColumn = it
			elif index == 4:
				Number = it
			elif index == 5:
				datatype = it
			elif index == 6:
				batchNO = it
			index += 1
		identifier = dbTable + "_id"

		# Log function and register to output file
		outputfile.write("\nfxn {} reg {} ".format(incoming[:2],int(incoming[2:6],16)))

		# Handle special cases for Number variable
		if Number == 'A':
			query = "SELECT trans_no from trans_arm_data WHERE arm_no = "+arm
			rdb_c.execute(query)
			fetched = rdb_c.fetchone()
			if fetched is not None:
				transNO = str(fetched[0])
			if transNO == "":
				outputfile.write("\n****ERROR**** ")
				outputfile.write("- no trans number\n")
				print bcolors.FAIL+"No trans number!"+bcolors.ENDC
				continue

			if batchNO == "10" or batchNO == "":
				Number = args.arm
			else:
				query = "SELECT batch_data_id FROM batch_data WHERE arm_no = "+arm+" AND trans_no = "+transNO
				query += " AND batch_no = "+batchNO
				print query
				ldb_c.execute(query)
				fetched = ldb_c.fetchone()
				if fetched is not None:
					Number = str(fetched[0])
				if Number == "":
					outputfile.write("\n****ERROR**** ")
					outputfile.write("- no batch ID\n")
					print bcolors.FAIL+"No batch ID!"+bcolors.ENDC
					continue

		elif Number == 'B':
			query = "SELECT bay_assignment FROM arm_config WHERE arm_config_id = "+arm
			pdb_c.execute(query)
			fetched = pdb_c.fetchone()
			if fetched is not None:
				Number = str(fetched[0])

		elif Number[0] == 'P':
			query = "SELECT trans_no from trans_arm_data WHERE arm_no = "+arm
			rdb_c.execute(query)
			fetched = rdb_c.fetchone()
			if fetched is not None:
				transNO = str(fetched[0])
			if transNO == "":
				outputfile.write("\n****ERROR**** ")
				outputfile.write("- no trans number\n")
				print bcolors.FAIL+"No trans number!"+bcolors.ENDC
				continue

			query = "SELECT batch_product_data_id from batch_product_data WHERE arm_no = "
			query += arm+" AND trans_no = "+transNO+" AND prd_no = "+Number[1]+" AND batch_no = "+batchNO
			if not batchNO == "10":
				ldb_c.execute(query)
				fetched = ldb_c.fetchone()
				if fetched is not None:
					thing = str(fetched[0])
				else:
					thing = None
			else:
				rdb_c.execute(query)
				fetched = rdb_c.fetchone()
				if fetched is not None:
					thing = str(fetched[0])
				else:
					thing = None

			if not thing == None:
				Number = str(thing)
			else:
				print "Product was not used"
				outputfile.write("\tProduct was not used\n")
				continue;

		elif Number[0] == 'D':
			Number = str((((int(arm)-1)*6)+int(Number[1])))

#		print "Number: ",Number

		if debug>0:
			print bcolors.HEADER+"\nfxn {} reg {}".format(incoming[:2],int(incoming[2:6],16))+bcolors.ENDC


		if debug>10:
			print incoming
			print "Using ",dbName," database"
			outputfile.write("\n\t"+incoming)
			outputfile.write("\n\tUsing "+dbName+" database")
		
		# Send modbus query, get response
		string = send_command(incoming)
		if string == "-1":
			continue

		# Process data here
		data = string[6:]

		if datatype == "I" or datatype == "L" or datatype == "C":
			nice_data = int(data,16)
		elif datatype == "F":
			nice_data = struct.unpack('!f', data.decode('hex'))[0]
		elif datatype == "D":
			nice_data = struct.unpack('!d', data.decode('hex'))[0]
		else:
			check_string(data, dbName, dbTable, dbColumn, Number, incoming)
			outputfile.write("\n")
			continue

		try:
			if dbName == "rdb":
				rand = random.randint(0,65535)
				if datatype == "C":
					if nice_data == 1:
						rand = 0;
					else:
						rand = 1;
				query = "SELECT "+dbColumn+" FROM "+dbTable+" WHERE "+identifier+" = "+Number
				if debug > 2:
					print query
					outputfile.write("\n\t"+query)
				rdb_c.execute(query)
				fetched = rdb_c.fetchone()
				if fetched is not None:
					old_data = fetched[0]
				else:
					old_data = 0

				if debug > 0:
					print "nice_data: ",nice_data,", old_data: ",old_data
					outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

				if not abs(nice_data - old_data)<0.0001:
					passed = False
					outputfile.write("\n****ERROR**** ")
					print "n=",nice_data,". o=",old_data,"."
					outputfile.write("- Value in database does not match what Modbus reported"+"\n")
					outputfile.write("nice_data: "+str(nice_data)+", old_data: "+str(old_data)+"\n\n")
				query = "UPDATE "+dbTable+" SET "+dbColumn+" = "+str(rand)+" WHERE "+identifier+" = "+Number
				if debug > 2:
					print query
					outputfile.write("\n\t"+query)
				rdb_c.execute(query)
				rdb.commit()
			
			elif dbName == "pdb":
				rand = random.randint(0,65535)
				if datatype == "C":
					rand = random.randint(0,1)
				query = "SELECT "+dbColumn+" FROM "+dbTable+" WHERE "+identifier+" = "+Number
				if debug > 2:
					print query
					outputfile.write("\n\t"+query)
				pdb_c.execute(query)
				fetched = pdb_c.fetchone()
				if fetched is not None:
					old_data = fetched[0]
				else:
					old_data = 0

				if debug > 0:
					print "nice_data: ",nice_data,", old_data: ",old_data
					outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

				if not nice_data == old_data:
					passed = False
					outputfile.write("\n****ERROR**** ")
					print "n=",nice_data,". o=",old_data,"."
					outputfile.write("- Value in database does not match what Modbus reported"+"\n")
					outputfile.write("nice_data: "+str(nice_data)+", old_data: "+str(old_data)+"\n\n")
				query = "UPDATE "+dbTable+" SET "+dbColumn+" = "+str(rand)+" WHERE "+identifier+" = "+Number
				if debug > 2:
					print query
					outputfile.write("\n\t"+query)
				pdb_c.execute(query)
				pdb.commit()
			
			elif dbName == "ldb":
				rand = random.randint(0,65535)
				if datatype == "C":
					rand = random.randint(0,1)
				query = "SELECT "+dbColumn+" FROM "+dbTable+" WHERE "+identifier+" = "
				query += Number#+" AND trans_no = "+transNO
				if debug > 2:
					print query
					outputfile.write("\n\t"+query)
				ldb_c.execute(query)
				fetched = ldb_c.fetchone()
				if fetched is not None:
					old_data = fetched[0]
				else:
					old_data = 0

				if debug > 0:
					print "nice_data: ",nice_data,", old_data: ",old_data
					outputfile.write("\n\tnice_data: "+str(nice_data)+", old_data: "+str(old_data))

				if not abs(nice_data - old_data)<0.0001:
					passed = False
					outputfile.write("\n****ERROR**** ")
					print "n=",nice_data,". o=",old_data,"."
					outputfile.write("- Value in database does not match what Modbus reported"+"\n")
					outputfile.write("nice_data: "+str(nice_data)+", old_data: "+str(old_data)+"\n\n")
				query = "UPDATE "+dbTable+" SET "+dbColumn+" = "+str(rand)+" WHERE "+identifier+" = "
				query += Number+" AND trans_no = "+transNO
				if debug > 2:
					print query
					outputfile.write("\n\t"+query)
				ldb_c.execute(query)
				ldb.commit()

		except TypeError as e:
			outputfile.write("- Database error!"+str(e)+"\n")
			print e
			continue
		except Exception as e:
			outputfile.write("- Database error!"+str(e)+"\n")
			print e
			continue
		except:
			outputfile.write("General exception caught.\n")
			print "General exception caught."
			continue

		string = send_command(incoming)
		if string == "-1":
			continue
	
		data = string[6:]
		if datatype == "I" or datatype == "L" or datatype == "C":
			nice_data = int(data,16)
		elif datatype == "F":
			nice_data = struct.unpack('!f', data.decode('hex'))[0]
		elif datatype == "D":
			nice_data = struct.unpack('!d', data.decode('hex'))[0]


		if debug > 0:
			print "nice_data: ",nice_data,", rand: ",rand
			outputfile.write("\n\tnice_data: "+str(nice_data)+", rand: "+str(rand))

		if not nice_data == rand:
			print "n=",nice_data,". r=",rand,"."
			passed = False
			outputfile.write("\n****ERROR**** ")
			outputfile.write("- Reported value did not change with the database\n")
			outputfile.write("nice_data: "+str(nice_data)+", rand: "+str(rand)+"\n\n")

		
		query = "UPDATE "+dbTable+" SET "+dbColumn+" = "+str(old_data)+" WHERE "+identifier+" = "+Number

		try:
			if dbName == "rdb":
				rdb_c.execute(query)
				rdb.commit()
			if dbName == "pdb":
				pdb_c.execute(query)
				pdb.commit()
			if dbName == "ldb":
				query = query+" AND trans_no = "+transNO
				ldb_c.execute(query)
				ldb.commit()
		except TypeError as e:
			outputfile.write("- Database error!"+str(e)+"\n")
			print e
			continue
		except Exception as e:
			outputfile.write("- Database error!"+str(e)+"\n")
			print e
			continue
		except:
			outputfile.write("General exception caught.\n")
			print "General exception caught."
			continue

		if passed:
			outputfile.write("\nOK\n\n")
			print bcolors.OKGREEN+"OK"+bcolors.ENDC
		else:
			print bcolors.FAIL+"fxn {} reg {} ERROR".format(incoming[:2],int(incoming[2:6],16))+bcolors.ENDC


#################################################################################################################
# Function 3 mode
#################################################################################################################
if args.mode == 'F3':

	# Read in old params, save to temp file
	print "Reading ALIV and saving config ..."
	OldCfg = open("ModOldConfig.txt", 'w')
	loopcount = 0
	for line in inputfile:
		string = data = ""
		alist = line.split()

		# Process comments
		if len(alist)==0:
			continue
		if alist[0][0] == '#':
			outputfile.write("\n")
			for it in alist:
				print it,
				outputfile.write(it+" ")
			print " "
			continue
		if alist[0][0] == "/":
			continue

		# Get information from the file
		ModAddr = ModLen = ModValue = ModMax = ModMin = ""
		index = 0
		for it in alist:
			if index == 0:
				ModAddr = str(hex(int(it))[2:]).zfill(4)
			elif index == 1:
				ModLen = str(hex(int(it))[2:]).zfill(4)
			elif index == 2:
				ModMin = it
			elif index == 3:
				ModMax = it
			index += 1

		# Generate and send modbus query
		out_command = "03"+ModAddr+ModLen
		string = send_command(out_command)

		# Check modbus response
		if len(string)<9:
			data = "0000"
		else:
			data = string[6:]

		# Save configuration to file
		OldCfg.write(ModAddr+"\t"+ModLen+"\t"+data+"\t"+ModMin +"\t"+ModMax +"\t"+"\n")

		loopcount += 1
		if debug > 9:
			print "Register: ",int(ModAddr,16),", cycle: ",loopcount
	OldCfg.close()

	# check program mode is OK to log into
	print "Checking program mode OK"
	out_command = "0608020000"
	send_command(out_command)
	time.sleep(0.1)

	# Check program mode state
	out_command = "0308010001"
	program_ok = send_command(out_command)

	if not (program_ok[9] == '0'):
		print "Program mode in use, closing..."
		ALIV.close()
		pdb.close()
		rdb.close()
		ldb.close()
		sys.exit(1)

	# Write 0 to program mode result
	send_command("0608020000")

	########################################################################################
	# Write garbage to all the registers
	print "Writing garbage to registers ..."
	OldCfg = open("ModOldConfig.txt", 'r')
	RandData = open("ModRandData.txt", 'w')
	loopcount = 0
	for line in OldCfg:
		alist = line.split()

		# Get information from the file
		ModAddr = ModLen = ModMax = ModMin = ""
		index = 0
		for it in alist:
			if index == 0:
				ModAddr = it
			elif index == 1:
				ModLen = it
			elif index == 3:
				ModMin = it
			elif index == 4:
				ModMax = it
			index += 1
		if ModMin == "" or ModMax == "":
			ModMin = "0"
			ModMax = "65535"
		ByteCount = str(int(ModLen,16)*2).zfill(2)
		HexByteCount = str(hex(int(ByteCount)))[2:].zfill(2)

		# Generate garbage for ints, chars, etc
		if ModLen == "0001":
			rand = ""
			if int(ModMin) < 0:
				ModMin = "0"
			if int(ModMax) > 0xFFFF:
				ModMax = "65535"
			rnum = random.randint(int(ModMin),int(ModMax))
			rand += str(hex(rnum)[2:]).zfill(4)
			RandData.write(rand+"\n")
			out_command = "10"+ModAddr+ModLen+HexByteCount+rand

		# Generate garbage for long and floats
		elif ModLen == "0002":
			isLong = ( (int(ModAddr,16) == 5952) or (int(ModAddr,16) == 6272) or (int(ModAddr,16) == 6592) or (int(ModAddr,16) == 6912) or (int(ModAddr,16) == 22400) or (int(ModAddr,16) == 22720) )
			if ((int(ModAddr,16) < 4180 and int(ModAddr,16) > 4159)) or isLong:
				if int(ModMin) < 0:
					ModMin = "0"
				if int(ModMax) > 0xFFFFFFFF:
					ModMax = "4294967295"
				rnum = random.randint(int(ModMin),int(ModMax))
				rand = str(hex(rnum)[2:]).zfill(8)
			else:
				if float(ModMin) < -10**38:
					ModMin = "-100000000000000000000000000000000000000"
				if float(ModMax) > 10**38:
					ModMax = "100000000000000000000000000000000000000"
				rand = random.uniform(float(ModMin),float(ModMax))
				rand = round(rand,3)
				rand = "%x" % struct.unpack('<I', struct.pack('<f', rand))[0]
#			if str(rand)[-1]=="L":
#				rand = rand[:-1]
			RandData.write(str(rand).zfill(4)+"\n")
			out_command = "10"+ModAddr+ModLen+HexByteCount+str(rand).zfill(int(ByteCount)/2)

		# Generate garbage for text
		else:
			rand = ""
			if int(ModMax)>32:
				ModMax = 32
			if int(ModMin)<0:
				ModMin = 0
			for it in range(int(ModMax)):
				rnum = random.randint(47,126)
				rand += str(hex(rnum)[2:]).zfill(2)
			HexByteCount = hex(int(ModMax))[2:].zfill(2)
			oldLen = ModLen
			if int(ModMax)%2:
				ModLen = hex((int(ModMax)/2)+1)[2:].zfill(4)
				rand = rand+"00"
				RandData.write(rand.ljust(int(oldLen,16)*4,'0')+"\n")
				HexByteCount = str(hex(int(HexByteCount,16)+1)[2:]).zfill(2)
			else:
				ModLen = hex(int(ModMax)/2)[2:].zfill(4)
				RandData.write(rand.ljust(int(oldLen,16)*4,'0')+"\n")
			out_command = "10"+ModAddr+ModLen+HexByteCount+rand

		# Output modbus message
		program_ok = send_command(out_command)
		if program_ok == "-1":
			outputfile.write("\tregister "+str(int(ModAddr,16))+"\n")

		loopcount += 1
		if debug > 9:
			print "Register: ",int(ModAddr,16),", cycle: ",loopcount
	RandData.close()
	OldCfg.close()

	########################################################################################
	# log out
	# raw_input("Grab the edit buff NOW!")
	print "Logging out"
	out_command = "0608000001"
	program_ok = send_command(out_command)
	while True:	
		out_command = "0308010003"
		program_ok = send_command(out_command)
		if program_ok[6:10]=="0000":
			break;
		time.sleep(0.1)
	
	# Check program mode result
	out_command = "0308020001"
	send_command(out_command)
	time.sleep(2)
	loopcount = 0


	########################################################################################
	# check configuration
	RandData = open("ModRandData.txt", 'r')
	OldCfg = open("ModOldConfig.txt", 'r')
	CfgLines = OldCfg.readlines()
	RandLines = RandData.readlines()
	lineIndex = 0
	outputfile.write("\n\n**********************************************\nConducting actual test\n**********************************************\n\n")
	print "Checking config matches garbage ..."
	for curline in CfgLines:
		alist = CfgLines[lineIndex].split()

		# Get information from the file
		ModAddr = ModLen = rand = ModData = ""
		index = 0
		for it in alist:
			if index == 0:
				ModAddr = it
			elif index == 1:
				ModLen = it
			elif index == 2:
				ModData = it
			index += 1
		rand = RandLines[lineIndex][:-1]
		lineIndex += 1

		# get information from the accuload
		out_command = "03"+ModAddr+ModLen
		program_ok = send_command(out_command)

		# compare them!
		print str(int(ModAddr,16)),":",
		if rand == program_ok[6:]:
			print "OK!"
			outputfile.write("Register "+str(int(ModAddr,16))+" OK\n\n")
			if debug > 1:
				print "\trand: ",rand,", register: ",program_ok[6:]
		else:
			print "BOO."
			outputfile.write("Register "+str(int(ModAddr,16))+" ERROR - rand: "+rand+", data: "+program_ok[6:]+"\n\n")
			if debug > 1:
				print "\trand: ",rand,", register: ",program_ok[6:]
	outputfile.write("**********************************************\nActual test completed\n**********************************************\n\n")
	OldCfg.close()
	RandData.close()

	########################################################################################

	# Write 0 to program mode result
	send_command("0608020000")

	# rewrite old configuration
	OldCfg = open("ModOldConfig.txt", 'r')
	print "Restoring configuration ..."
	loopcount = 0
	for line in OldCfg:
		alist = line.split()

		# Get information from the file
		ModAddr = ModLen = ModData = ""
		index = 0
		for it in alist:
			if index == 0:
				ModAddr = it
			elif index == 1:
				ModLen = it
			elif index == 2:
				ModData = it
			index += 1

		loopcount += 1

		if debug > 9:
			print "Register: ",int(ModAddr,16),", cycle: ",loopcount

		# write file information to accuload
		HexByteCount = str(hex(int(ModLen,16)*2))[2:].zfill(2)
		out_command = "10"+ModAddr+ModLen+HexByteCount+ModData
		program_ok = send_command(out_command)
		if program_ok == "-1":
			outputfile.write("\tregister "+str(int(ModAddr,16))+"\n")


	RandData.close()
	OldCfg.close()

	# log out
	print "Done! logging out ..."
	out_command = "0608000001"
	program_ok = send_command(out_command)

	while True:	
		out_command = "0308010003"
		program_ok = send_command(out_command)
		if program_ok[6:10]=="0000":
			break;
		time.sleep(0.1)
	print "Later nerds!"



#################################################################################################################
# Backwards compatability mode				* not entirely working presently
# Directly compare an AL3 vs ALIV
#################################################################################################################
if args.mode == 'b':
	i = 0
	for line in inputfile:
		i+=1
		passed = True
		string = data = ""
		alist = line.split()

		# Process comments
		if len(alist)==0:
			continue
		if alist[0][0] == '#':
			outputfile.write("\n")
			for it in alist:
				print it,
				outputfile.write(it+" ")
			print " "
			continue
		if alist[0][0] == "/":
			continue

		# Get information from the file
		incoming = ""
		dbTable = dbColumn = Number = dbName =datatype = "NOPE"
		index = 0
		for it in alist:
			if (not it == '#') and (index == 0):
				incoming += it
				continue
			elif index == 1:
				dbName = it
			elif index == 2:
				dbTable = it
			elif index == 3:
				dbColumn = it
			elif index == 4:
				Number = it
			elif index == 5:
				datatype = it
			index += 1
		identifier = dbTable + "_id"


		if debug>0:
			print bcolors.HEADER+"\nfxn {} reg {}".format(incoming[:2],int(incoming[2:6],16))+bcolors.ENDC
		if debug>4:
			print "Sending: ",incoming


		outputfile.write("\nfxn {} reg {} ".format(incoming[:2],int(incoming[2:6],16)))
		
		# Send modbus query, get response
		both = send_both(incoming)
		string = both[0]
		string3 = both[1]
		if string == "-1" or string3 == "-1":
			continue

		# Process data here
		data = string[6:]
		if datatype == "I" or datatype == "L":
			nice_data = int(data,16)
		elif datatype == "F":
			nice_data = struct.unpack('!f', data.decode('hex'))[0]
		elif datatype == "D":
			nice_data = struct.unpack('!d', data.decode('hex'))[0]
		else:
			for i in range(0,len(data), 2):
				if data[i:i+2]=="00":
					data = data[0:i]
			nice_data = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

		data3 = string3[6:]
		if datatype == "I" or datatype == "L":
			nice_data3 = int(data3,16)
		elif datatype == "F":
			nice_data3 = struct.unpack('!f', data3.decode('hex'))[0]
		elif datatype == "D":
			nice_data3 = struct.unpack('!d', data3.decode('hex'))[0]
		else:
			for i in range(0,len(data3), 2):
				if data3[i:i+2]=="00":
					data3 = data3[0:i]
			nice_data3 = ''.join(chr(int(data3[i:i+2], 16)) for i in range(0, len(data3), 2))

		if debug>0:
			print "nice_data:\t",nice_data
			print "nice_data3:\t",nice_data3
		if debug>1:
			print "data: ",data
		if debug>2:
			print "string: ",string
			print "datatype: ",datatype

		if nice_data == nice_data3:
			print bcolors.OKGREEN+"OK",bcolors.ENDC
			outputfile.write(" OK\n")
		else:
			print bcolors.FAIL+"FAIL",bcolors.ENDC
			outputfile.write(" FAIL\n")
			

		outputfile.write(str(nice_data)+"\n"+str(nice_data3)+"\n")


#################################################################################################################
# Remote mode
#################################################################################################################
if args.mode == 'r':
	i = 0
	for line in inputfile:
		i+=1
		passed = True
		string = data = ""
		alist = line.split()


		# Process comments
		if len(alist)==0:
			continue
		if alist[0][0] == '#':
			outputfile.write("\n")
			for it in alist:
				print it,
				outputfile.write(it+" ")
			print " "
			continue
		if alist[0][0] == "/":
			continue

		# Get information from the file
		incoming = ""
		dbTable = dbColumn = Number = dbName =datatype = "NOPE"
		index = 0
		for it in alist:
			if (not it == '#') and (index == 0):
				incoming += it
				continue
			elif index == 1:
				dbName = it
			elif index == 2:
				dbTable = it
			elif index == 3:
				dbColumn = it
			elif index == 4:
				Number = it
			elif index == 5:
				datatype = it
			index += 1
		identifier = dbTable + "_id"

		if debug>0:
			print bcolors.HEADER+"\nfxn {} reg {}".format(incoming[:2],int(incoming[2:6],16))+bcolors.ENDC


		outputfile.write("fxn {} reg {} ".format(incoming[:2],int(incoming[2:6],16)))
		
		# Send modbus query, get response
		string = send_command(incoming)
		if string == "-1":
			continue

		# Process data here
		data = string[6:]
		if datatype == "I" or datatype == "L":
			nice_data = int(data,16)
		elif datatype == "F":
			nice_data = struct.unpack('!f', data.decode('hex'))[0]
		elif datatype == "D":
			nice_data = struct.unpack('!d', data.decode('hex'))[0]
		else:
			for i in range(0,len(data), 2):
				if data[i:i+2]=="00":
					data = data[0:i]
			nice_data = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

		if debug>0:
			print bcolors.OKGREEN+"nice_data: ",nice_data,bcolors.ENDC
		if debug>1:
			print bcolors.OKGREEN+"data: ",data,bcolors.ENDC
		if debug>2:
			print bcolors.OKGREEN+"string: ",string
			print "datatype: ",datatype,bcolors.ENDC
			

		outputfile.write(str(nice_data)+"\n")


#################################################################################################################
# Set mode
#################################################################################################################
if args.mode == 'set':

	# Write 0 to program mode result
	send_command("0608020000")

	# write configuration
	#OldCfg = open("ModOldConfig.txt", 'r')
	print "Setting configuration ..."
	for line in inputfile:
		alist = line.split()

		# Get information from the file
		ModAddr = ModLen = ModData = ""
		index = 0
		for it in alist:
			if index == 0:
				ModAddr = it
			elif index == 1:
				ModLen = it
			elif index == 2:
				ModData = it
			index += 1

		# write file information to accuload
		HexByteCount = str(hex(int(ModLen,16)*2))[2:].zfill(2)
		out_command = "10"+ModAddr+ModLen+HexByteCount+ModData
		if debug:
			print out_command
		program_ok = send_command(out_command)
		if program_ok == "-1":
			outputfile.write("\tregister "+str(int(ModAddr,16))+"\n")


	# log out
	print "Done! logging out ..."
	out_command = "0608000001"
	program_ok = send_command(out_command)

	while True:	
		out_command = "0308010001"
		program_ok = send_command(out_command)
		if program_ok[6:10]=="0000":
			break;
		time.sleep(0.1)

	program_ok = send_command("0308020001")
	print "program ok: ", program_ok[6:10]
	print "Later nerds!"


#################################################################################################################
# Function 1 mode
#################################################################################################################
if args.mode == "F1":

	print "Running test for functions 1, 5 and 15"

	# Init database cursors
	pdb_c = pdb.cursor()
	rdb_c = rdb.cursor()
	ldb_c = ldb.cursor()

	passed = []
	reason = []
	HexCoilAddress = []
	loopcount = 0

	# Loop over input file
	for line in inputfile:
		string = data = transNO = batchNO = ""
		alist = line.split()

		# Process comments
		if len(alist)==0:
			continue
		if alist[0][0] == '#':
			outputfile.write("\n")
			for it in alist:
				print it,
				outputfile.write(it+" ")
			print " "
			continue
		if alist[0][0] == "/":
			continue

		# Get information from the file
		incoming = ""
		dbTable = dbColumn = Number = dbName = datatype = "NOPE"
		index = 0
		for it in alist:
			if (not it == '#') and (index == 0):
				incoming += it
				continue
			elif index == 1:
				dbName = it
			elif index == 2:
				dbTable = it
			elif index == 3:
				dbColumn = it
			elif index == 4:
				Number = it
			elif index == 5:
				datatype = it
			elif index == 6:
				batchNO = it
			index += 1
		identifier = dbTable + "_id"

		# Figure out what Number means
		if Number == 'A':
			Number = args.arm

		elif Number[0] == 'D':
			Number = Number[1]

		# Set coil to 1 to start the test
		try:
			if dbTable == "Bool_dig_out_status":
				query = "INSERT INTO delivery_queue (delivery_cmd, cmd_arg_1, cmd_arg_2, cmd_arg_3, arm_no) VALUES ('Set Dig Out', "+str(Number)+", 1, 1, "+str(arm)+")"
			else:
				query = "INSERT INTO delivery_queue (delivery_cmd, arm_no, cmd_arg_1, cmd_arg_2, cmd_arg_3) VALUES ('Set Alarm', "+str(arm)+", '"+dbTable+"', '"+dbColumn+"', "+Number+")"

			rdb_c.execute(query)
			rdb.commit()

			if debug > 2:
				print query
				outputfile.write(query+"\n")

		except TypeError as e:
			outputfile.write("- Database error!"+str(e)+"\n")
			print e
			continue
		except Exception as e:
			outputfile.write("- Database error!"+str(e)+"\n")
			print e
			continue
		except:
			outputfile.write("General exception caught.\n")
			print "General exception caught."
			continue

		HexCoilAddress.append(incoming[2:6])
		passed.append(True)
		reason.append(0)
		loopcount += 1
		if debug > 9:
			print loopcount
		# if (loopcount % 5) == 0:
		# 	print "Nap time..."
		rdb.commit()
		time.sleep(0.20)

	################################################################################################################

	if debug > 0:
		outputfile.write("\nChecking 1's\n")
	loopcount = 0
	time.sleep(2)
	print "Check 1 was set"
	for addr in HexCoilAddress:
		# Check 1 was set
		string = send_command("01"+addr+"0001")
		if string == "-1":
			passed[loopcount] = False
			continue
		data = string[6:]
		if not bool(int(data)):
			passed[loopcount] = False
			reason[loopcount] = 1
			# print "One not set"
			outputfile.write("Coil "+str(int(addr,16))+" ****** FAILED - 1 not set\n")
			# outputfile.write("oops - "+string+"\n")
		loopcount += 1
		if debug > 9:
			print loopcount
		# if (loopcount % 25) == 0:
		# 	time.sleep(1)
		time.sleep(0.005)

	if debug > 0:
		outputfile.write("\nSetting 0's\n")
	loopcount = 0
	print "Set to 0 via Modbus"
	time.sleep(1)
	for addr in HexCoilAddress:
		# Set to 0 via Modbus
		incoming = "05"+addr+"0000"
		string = send_command(incoming)
		if string == "-1":
			passed[loopcount] = False
			continue
		data = string[8:]
		if bool(int(data)):
			passed[loopcount] = False
			reason[loopcount] = 2
			outputfile.write("Coil "+str(int(addr,16))+" ****** FAILED - did not set 0\n")
			# outputfile.write("oops - "+string+"\n")
			# print "did not set 0"
		loopcount += 1
		if debug > 9:
			print loopcount
		# if (loopcount % 25) == 0:
		# 	time.sleep(1)
		time.sleep(0.005)

	if debug > 0:
		outputfile.write("\nChecking 0's\n")
	time.sleep(1)
	loopcount = 0
	print "Check 0 via Modbus"
	for addr in HexCoilAddress:
		# Check 0 via Modbus
		if passed[loopcount]:
			incoming = "01"+addr+"0001"
			string = send_command(incoming)
			if string == "-1":
				passed[loopcount] = False
				continue
			data = string[6:]
			if bool(int(data)):
				passed[loopcount] = False
				reason[loopcount] = 3
				outputfile.write("Coil "+str(int(addr,16))+" ****** FAILED - value is not 0\n")
				# outputfile.write("oops - "+string+"\n")
				# print "Value is not 0"
		loopcount += 1
		if debug > 9:
			print loopcount
		# if (loopcount % 25) == 0:
		# 	time.sleep(1)
		time.sleep(0.005)

	if debug > 0:
		outputfile.write("\nOutput test results\n")
	loopcount = 0
	print "Output test results"
	for addr in HexCoilAddress:
		# Output test result for this coil
		if passed[loopcount]:
			print bcolors.OKGREEN+"OK",bcolors.ENDC
			outputfile.write("Coil "+str(int(addr,16))+" passed\n")
		else:
			print bcolors.FAIL+"BOO",bcolors.ENDC
			outputfile.write("Coil "+str(int(addr,16))+" ****** FAILED")
			if reason[loopcount] == 1:
				outputfile.write(" - one not set\n")
			elif reason[loopcount] == 2:
				outputfile.write(" - did not set 0\n")
			else:
				outputfile.write(" - value is not 0\n")
		loopcount += 1

#################################################################################################################
# Extended Services mode
#################################################################################################################
if args.mode == "EX":

	print "Extended services testing"
	# outputfile.write("Extended services testing\n")
	incoming = raw_input("Enter Extended Services packet hex : ")
	incoming = incoming.replace(" ","")
	while not incoming == 'q':
		output = send_ext_packet(incoming)
		if not (output == "-1"):
			print "\nraw hex:\n",output
			print "\nExt output:\n\nReg\t0x\tint\tchar\tuint\t\tfloat (or double)\n____\t____\t____\t____\t____\t\t___________________"
			index = 1
			print "1\t",output[0:4],"\t",int(output[0:4],16)
			output = output[4:]
			for byte in output:
				if not (index % 4):
					print "\n",(index+4)/4,"\t",output[index-4:index],"\t",int(output[index-4:index],16),"\t",output[index-4:index].decode("hex"),
				if not (index % 8):
					print "\t","{0:0>10}".format(int(output[index-8:index],16)), "\t",struct.unpack('!f', output[index-8:index].decode('hex'))[0],"[f]",
					if not (index % 16):
						print "\t",struct.unpack('!d', output[index-16:index].decode('hex'))[0],"[d]",
				index += 1

			# index=1
			# for byte in output:
			# 	if not (index % 2):
			# 		print output[index-2:index].decode("hex"),
			# 		index+=1
			print "\n"
		incoming = raw_input("Enter Extended Services packet hex : ")
		incoming = incoming.replace(" ","")




#################################################################################################################
# Extended Services File mode
#################################################################################################################
if args.mode == "EXf":

	print "Extended services testing (from file)\n"
	outputfile.write("Extended services testing (from file)\n\n")

	# Loop over input file
	for line in inputfile:
		string = ""
		alist = line.split()

		# Process comments
		if len(alist)==0:
			continue
		if alist[0][0] == '#':
			outputfile.write("\n")
			for it in alist:
				print it,
				outputfile.write(it+" ")
			print " "
			continue

		if alist[0][0] == "/":
			continue

		if alist[0].upper() == 'W':
			del alist[0]
			msg = " ".join(alist)
			raw_input(msg)
			continue

		if alist[0].upper() == "ARM":
			if int(alist[1])<99:
				arm = alist[1].zfill(2)
			continue

		# Get information from the file
		incoming = ""
		index = 0
		for it in alist:
			if (not it == '#') and (index == 0):
				incoming += it
				continue
			elif index == 1:
				something = it
			index += 1

		if incoming[0].upper() == 'P':
			timer = float(incoming[1:])
			time.sleep(timer)
			continue

		output = send_ext_packet(incoming)
		outputfile.write("Ext input: "+incoming+"\n")
		
		if not (output == "-1"):
			print "Ext output:\n\nReg\tint\t0x\n___\t___\t___"
			outputfile.write("Ext output:\n\nReg\t\tint\t\t0x\n___\t\t___\t\t___\n")
			index = 1
			for byte in output:
				if not (index % 4):
					print index/4,"\t",int(output[index-4:index],16),"\t",output[index-4:index]
					outputfile.write(str(index/4)+"\t\t"+str(int(output[index-4:index],16))+"\t\t"+output[index-4:index]+"\n")
				index += 1
			outputfile.write("\n")
			print "\n"


	

# shut down everything and exit!
if not ((args.mode == 'c') or (args.mode == "EX")):
	inputfile.close()
	outputfile.close()
ALIV.close()
AL3.close()
pdb.close()
rdb.close()
ldb.close()
sys.exit(1)