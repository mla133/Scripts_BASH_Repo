#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
import socket
import sys
import struct
import codecs
import time
import binascii
import serial

Port = 502
BUFF_SIZE = 2048
# IPADDR = "192.168.181.172"
serial_mode = False
ser = serial.Serial()
ser.baudrate = 115200
serial_mode = False
ALIV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ALIV.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 4)
global DO_HAMMER 
DO_HAMMER = False
global seq_num
seq_num = 1

# /* 				CRC Table															*
#  * NOTE: in the original table, crc16tbl[26] was 0xc881; this has been corrected 	*
#  *       to 0xcb81. 																*/
crc16tbl =[
		0x0000,	0xC0C1,	0xC181,	0x0140,	0xC301,	0x03C0,	0x0280,	0xC241,
		0xC601,	0x06C0,	0x0780,	0xC741,	0x0500,	0xC5C1,	0xC481,	0x0440,
		0xCC01,	0x0CC0,	0x0D80,	0xCD41,	0x0F00,	0xCFC1,	0xCE81,	0x0E40,
		0x0A00,	0xCAC1,	0xCB81,	0x0B40,	0xC901,	0x09C0,	0x0880,	0xC841,
		0xD801,	0x18C0,	0x1980,	0xD941,	0x1B00,	0xDBC1,	0xDA81,	0x1A40,
		0x1E00,	0xDEC1,	0xDF81,	0x1F40,	0xDD01,	0x1DC0,	0x1C80,	0xDC41,
		0x1400,	0xD4C1,	0xD581,	0x1540,	0xD701,	0x17C0,	0x1680,	0xD641,
		0xD201,	0x12C0,	0x1380,	0xD341,	0x1100,	0xD1C1,	0xD081,	0x1040,
		0xF001,	0x30C0,	0x3180,	0xF141,	0x3300,	0xF3C1,	0xF281,	0x3240,
		0x3600,	0xF6C1,	0xF781,	0x3740,	0xF501,	0x35C0,	0x3480,	0xF441,
		0x3C00,	0xFCC1,	0xFD81,	0x3D40,	0xFF01,	0x3FC0,	0x3E80,	0xFE41,
		0xFA01,	0x3AC0,	0x3B80,	0xFB41,	0x3900,	0xF9C1,	0xF881,	0x3840,
		0x2800,	0xE8C1,	0xE981,	0x2940,	0xEB01,	0x2BC0,	0x2A80,	0xEA41,
		0xEE01,	0x2EC0,	0x2F80,	0xEF41,	0x2D00,	0xEDC1,	0xEC81,	0x2C40,
		0xE401,	0x24C0,	0x2580,	0xE541,	0x2700,	0xE7C1,	0xE681,	0x2640,
		0x2200,	0xE2C1,	0xE381,	0x2340,	0xE101,	0x21C0,	0x2080,	0xE041,
		0xA001,	0x60C0,	0x6180,	0xA141,	0x6300,	0xA3C1,	0xA281,	0x6240,
		0x6600,	0xA6C1,	0xA781,	0x6740,	0xA501,	0x65C0,	0x6480,	0xA441,
		0x6C00,	0xACC1,	0xAD81,	0x6D40,	0xAF01,	0x6FC0,	0x6E80,	0xAE41,
		0xAA01,	0x6AC0,	0x6B80,	0xAB41,	0x6900,	0xA9C1,	0xA881,	0x6840,
		0x7800,	0xB8C1,	0xB981,	0x7940,	0xBB01,	0x7BC0,	0x7A80,	0xBA41,
		0xBE01,	0x7EC0,	0x7F80,	0xBF41,	0x7D00,	0xBDC1,	0xBC81,	0x7C40,
		0xB401,	0x74C0,	0x7580,	0xB541,	0x7700,	0xB7C1,	0xB681,	0x7640,
		0x7200,	0xB2C1,	0xB381,	0x7340,	0xB101,	0x71C0,	0x7080,	0xB041,
		0x5000,	0x90C1,	0x9181,	0x5140,	0x9301,	0x53C0,	0x5280,	0x9241,
		0x9601,	0x56C0,	0x5780,	0x9741,	0x5500,	0x95C1,	0x9481,	0x5440,
		0x9C01,	0x5CC0,	0x5D80,	0x9D41,	0x5F00,	0x9FC1,	0x9E81,	0x5E40,
		0x5A00,	0x9AC1,	0x9B81,	0x5B40,	0x9901,	0x59C0,	0x5880,	0x9841,
		0x8801,	0x48C0,	0x4980,	0x8941,	0x4B00,	0x8BC1,	0x8A81,	0x4A40,
		0x4E00,	0x8EC1,	0x8F81,	0x4F40,	0x8D01,	0x4DC0,	0x4C80,	0x8C41,
		0x4400,	0x84C1,	0x8581,	0x4540,	0x8701,	0x47C0,	0x4680,	0x8641,
		0x8201,	0x42C0,	0x4380,	0x8341,	0x4100,	0x81C1,	0x8081,	0x4040
]

# /*=========================	   	Calculate Cyclic Redundancy Check		  ==============================*
#  * 																										*
#  * 				This function calculates a CRC for modbus communications								*
#  * 																										*
#  * 																										*/
def calc_crc16 ( buffer ):

	crc = 0xFFFF;
	for stuff in buffer:
		crc = crc16tbl[(crc & 0x00ff) ^ (stuff)] ^ ( crc >> 8 );

	return (crc);


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def selectall(event):
	event.widget.tag_add("sel","1.0","end")

def delete_results(*args):
	T.delete('1.0',END)

def HAMMER(*args):
	if DO_HAMMER:
		T.delete('1.0',END)
		send_modbus_command()
	root.after(1,HAMMER)

def Stop_HAMMER(*args):
	global DO_HAMMER 
	DO_HAMMER = False
	HAMMER()

def Start_HAMMER(*args):
	global DO_HAMMER 
	DO_HAMMER = True

def connect_to_accuload(*args):
	try:
		global serial_mode
		global ser
		if not ip_address.get().find("/dev/ttyUSB") == -1:
			serial_mode = True

		if serial_mode:
			ser.port=ip_address.get();
			ser.open()
			ser.reset_input_buffer()
			ser.reset_output_buffer()
		else:
			ALIV.connect((ip_address.get(),Port))
		# ALIV.settimeout(2)
	except:
		print ("Could not open port!")
		sys.exit(1)
	for child in mainframe.grid_slaves(row=1,column=3):
		child.destroy()
	for child in mainframe.grid_slaves(row=1,column=1):
		child.destroy()

	ttk.Label(mainframe, text=ip_address.get()).grid(column=1, row=1, sticky=W)
	ttk.Label(mainframe, text="<connected>").grid(column=3, row=1, sticky=W)
	ttk.Button(mainframe, text="Send Command", command=send_modbus_command).grid(column=1, row=6, sticky=W)

	ttk.Button(mainframe, text="Clear", command=delete_results).grid(column=2, row=6, sticky=W)

	ttk.Button(mainframe, text="HAMMER", command=Start_HAMMER).grid(column=2, row=6, sticky=E)

	ttk.Button(mainframe, text="Stop HAMMER", command=Stop_HAMMER).grid(column=3, row=6, sticky=W)

	# outgoing_command = ttk.Entry(mainframe, width=30, textvariable=command_out)
	# outgoing_command.grid(column=1, row=3, sticky=(W, E))

	s_a = ttk.Entry(mainframe, width=5, textvariable=slave_address)
	ttk.Label(mainframe, text="Slave address").grid(column=1, row=2, sticky=W)
	s_a.grid(column=2, row=2, sticky=(W, E))

	qty = ttk.Entry(mainframe, width=5, textvariable=quantity)
	ttk.Label(mainframe, text="Quantity").grid(column=1, row=3, sticky=W)
	qty.grid(column=2, row=3, sticky=(W, E))

	start_reg = ttk.Entry(mainframe, width=5, textvariable=start_register)
	ttk.Label(mainframe, text="Start address").grid(column=1, row=4, sticky=W)
	start_reg.grid(column=2, row=4, sticky=(W, E))

	new_val = ttk.Entry(mainframe, width=40, textvariable=new_value)
	ttk.Label(mainframe, text="New value").grid(column=1, row=5, sticky=W)
	new_val.grid(column=2, row=5, sticky=(W, E))

	# outgoing_command.focus()
	root.bind('<Return>', send_modbus_command)
	s_a.focus()

def send_modbus_command(*args):

	# incoming = command_out.get()

# command_out = StringVar()
# response = StringVar()
# slave_address = StringVar()
# ip_address = StringVar()
# function = StringVar()
# quantity = StringVar()
# start_register = StringVar()
# new_value = StringVar()

	incoming = slave_address.get() +" "+ mod_function.get() +" "+ start_register.get() +" "
	if int(mod_function.get()) > 4:
		incoming += new_value.get()
	else:
		incoming += quantity.get()
	# print (incoming)
	return_value = ""

	# Handle it!
	try:
		# Null input
		if incoming == "":
			return

		# Quit
		elif incoming[0].upper() == 'Q':
			print ("Exiting ...")
			raise ValueError("quit")

		# Raw hex, should be formatted already
		elif incoming[1].upper() == 'X':
			incoming = incoming.replace(" ","")
			incoming = incoming[2:]

		# Format input per instructions above
		else:
			print ("Interpreting input...")
			in_list = incoming.split()
			incoming = data = ""
			index = 0
			inside_string = False
			end_string = False
			for temp in in_list:
				if (index == 0) or (index == 1):
					tempHex = "%x" % int(temp)
					incoming = incoming+tempHex.zfill(2)
				elif (index == 2):
					tempHex = "%x" % int(temp)
					incoming = incoming+tempHex.zfill(4)
				else:
					if inside_string:
						if temp[-1:] == '\"':
							inside_string = False
							end_string = True
							temp = temp[:-1]
						tempHex = binascii.hexlify(bytes((" "+temp),'utf-8')).decode('utf-8')
						if not len(tempHex)%4==0 and end_string:
							end_string = False
							data = data+tempHex.ljust(len(tempHex)+(4-len(tempHex)%4),'0')
						else:
							data += tempHex
					elif temp[0] == 'f':
						tempHex = struct.pack('!f',float(temp[1:]))
						tempHex = codecs.encode(tempHex,"hex")
						print ("data:",data,tempHex)
						data = data+tempHex.decode('utf-8').zfill(8)
					elif temp[0] == 'd':
						tempHex = struct.pack('!d',float(temp[1:]))
						tempHex = codecs.encode(tempHex,"hex")
						data = data+tempHex.decode('utf-8').zfill(16)
					elif temp[0] == 'x':
						tempHex = "%x" % int(temp[1:],16)
						data = data+tempHex.zfill(4)
					elif temp[0] == '\"':
						if temp[-1:] != '\"':
							inside_string = True
						else:
							temp = temp[:-1]
						tempHex = binascii.hexlify(bytes(temp[1:],'utf-8')).decode('utf-8')
						if not len(tempHex)%4==0 and not inside_string:
							data = data+tempHex.ljust((len(tempHex)+2),'0')
						else:
							data += tempHex
					else:
						tempHex = "%x" % int(temp)
						data = data+tempHex.zfill(4)
				index += 1

			function = incoming[2:4]
			print ("data: ",data)

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
				outputQty = "%x" % (index)
				incoming = incoming + outputQty.zfill(4) + bytecount.zfill(2) + data

			else:
				if function == "05" and data == "0001":
					data = "FF00"
				incoming = incoming+data
				if len(incoming) > 12:
					print (bcolors.WARNING+"Invalid input: "+bcolors.ENDC+"("+incoming+")")
					response.set("Invalid input")
					return
	

	except ValueError as e:
		if str(e)=="quit":
			ALIV.close()
			sys.exit(1)
		print (bcolors.WARNING+str(e))
		print ("Input error\n"+bcolors.ENDC)
		return

	except Exception as e:
		print (bcolors.WARNING+str(e))
		print ("Input error\n"+bcolors.ENDC)
		return

	print ("Raw hex query: ",incoming)

	# Range check the address
	try:
		target_address = int(incoming[4:8],16)
		int(incoming,16)
		if len(incoming)%2:
			raise ValueError("derp")
	except:
		print (bcolors.WARNING+"Input is invalid!\n"+bcolors.ENDC)
		return
		
	# Turn the string into hex and send
	global seq_num
	hex_seq_num = "%x" % seq_num
	incoming = str(hex_seq_num).zfill(4)+"0000"+str("{0:0>4}".format(format(int((len(incoming)/2)),'x')))+incoming
	seq_num += 1
	if seq_num > 0xFFFF: seq_num = 1
	out = codecs.decode(incoming,"hex")

	if serial_mode:
		out = out[6:]
		crc = calc_crc16(out)
		out += (crc).to_bytes(2, byteorder='little')

		print (ser.write(out))
		time.sleep(.1)
	else:
		ALIV.send(out)

	# Get!
	function_code = 0;
	try:
		bytes_recvd = tries = 0
		waiting_on = 1
		data = b""
		while True:
			temp_data = b""
			if serial_mode:
				n = ser.inWaiting()
				if n:
					temp_data += ser.read(n)
				time.sleep(0.05)
			else:
				temp_data += ALIV.recv(BUFF_SIZE)

			# temp_data = ALIV.recv(BUFF_SIZE)

			bytes_recvd += len(temp_data)
			data += temp_data

			if serial_mode:
				if bytes_recvd > 3:
					function_code = struct.unpack(">L", b"\x00\x00\x00"+data[1:2])[0]
					if function_code < 5:
						waiting_on = struct.unpack(">L", b"\x00\x00\x00"+data[2:3])[0]+2
						waiting_on -= len(data)-3
					elif bytes_recvd > 5: break
			else:
				if bytes_recvd > 5:	
					waiting_on = struct.unpack(">L", data[2:6])[0]
					waiting_on -= len(temp_data)-6

			if waiting_on == 0: break

			if function_code & 0xF0:
				break;

			tries += 1
			if tries > 9999:
				T.insert(END, "No response\n")
				T.see(END)
				return

	except Exception as e:
		print (e)
		return

	# Hex into string
	if not serial_mode:
		data = data[6:]
	string = codecs.encode(data,"hex")

	if len(string)<6:
		print (bcolors.WARNING+"Response too short...\n"+bcolors.ENDC)
		return

	output_string = string.decode('utf-8')
	# Error handling
	if (string[2]&0x8) == 8:
		out = "ERROR RESPONSE\t"
		if output_string[5] == '1':
			out += "ILLEGAL FUNCTION\n"
		elif output_string[5] == '2':
			out += "ILLEGAL DATA ADDRESS\n"
		elif output_string[5] == '3':
			out += "ILLEGAL DATA VALUE\n"
		elif output_string[5] == '4':
			out += "SERVER DEVICE FAILURE\n"
		elif output_string[5] == '6':
			out += "SERVER DEVICE BUSY\n"
		response.set(out)
		T.insert(END, out)
		T.see(END)
		return

	# Make the output a little more readable
	out = "Raw hex input:\n"
	j = 0
	for it in output_string:
		out += it
		j+=1
		if j%4==0:
			out += " "
		if j%8==0:
			out += " "
		if j%16==0:
			out += "\t"
		if j%64==0:
			out += "\n"

	print (bcolors.OKGREEN+out+'\n')
	out += "\n"

	if function == "01" or function == "02":
		out += "Formatted output:\n"
		coil_data = data[3:-2]
		j=0
		for stuff in coil_data:
			out += str(target_address+j)+"\t"
			for offset in range(0,8):
				if (stuff&(1<<offset)) == 0:
					out += "0 "
				else:
					out += "1 "
			out += "\n"
			j+=8
			if j%(8*4)==0:
				out += "\n"

	# Fancy display for registers
	elif function == "03" or function == "04":
		# print ("Formatted output:\n")
		out += "Formatted output:\n\n"
		# print ("reg\t\thex\t\tint\t\tfloat\t\t\tdouble")
		out += "reg\t\thex\t\tint\t\tfloat\t\t\tdouble\n"
		# print ("______\t\t______\t\t______\t\t______\t\t\t______")
		out += "______\t\t______\t\t______\t\t______\t\t\t______\n"
		string = string[6:]
		j=0
		listicle = []
		for block in range(0,len(string),4):
			if endian.get()=="Little8":
				half_reg = string[block+2:block+4]
				half_reg +=string[block:block+2]
				listicle.append(half_reg)
			else:
				listicle.append(string[block:block+4])
		lastreg = tempint = lasttempint = b""
		regfloat = 0
		for register in listicle:
			if (j-3)%4 == 0:
				lasttempint = lasttempint+lastreg+register
				doubled = struct.unpack('!d', codecs.decode(lasttempint,'hex'))[0]
				if (endian.get()=="Little16"):
					tempint = register+lastreg
				else:
					tempint = lastreg+register
				regfloat = struct.unpack('!f', codecs.decode(tempint,'hex'))[0]
				lasttempint = b""
				#print (j+target_address,"\t\t",chr(int(register[:-2],16)),chr(int(register[2:],16)),"\t\t",int(register,16),"\t\t",regfloat,"\n\t\t\t\t\t\t\t\t\t",doubled)
				out += str(j+target_address)+"\t\t"+(str(register[:-2],'utf-8'))+(str(register[2:],'utf-8'))+"\t\t"+str(int(register,16))+"\t\t"+str(regfloat)+"\n\t\t\t\t\t\t\t\t\t"+str(doubled)
			elif j%2 == 1:
				if (endian.get()=="Little16"):
					tempint = register+lastreg
				else:
					tempint = lastreg+register
				regfloat = struct.unpack('!f', codecs.decode(tempint,'hex'))[0]
				lasttempint += tempint
				lastreg = b""
				#print (j+target_address,"\t\t",chr(int(register[:-2],16)),chr(int(register[2:],16)),"\t\t",int(register,16),"\t\t",regfloat)
				out += str(j+target_address)+"\t\t"+(str(register[:-2],'utf-8'))+(str(register[2:],'utf-8'))+"\t\t"+str(int(register,16))+"\t\t"+str(regfloat)
			else:
				#print (j+target_address,"\t\t",chr(int(register[:-2],16)),chr(int(register[2:],16)),"\t\t",int(register,16))
				out += str(j+target_address)+"\t\t"+(str(register[:-2],'utf-8'))+(str(register[2:],'utf-8'))+"\t\t"+str(int(register,16))
			tempint = b""
			lastreg = register
			j += 1
			out += "\n"
	print(bcolors.ENDC)

	# response.set(out)
	# T.config(state=ENABLED)
	T.insert(END, out)
	T.see(END)
	# T.config(state=DISABLED)
	
root = Tk()
root.title("Modbus")
root.bind_class("Text","<Control-a>", selectall)

mainframe = ttk.Frame(root, padding="20 20 20 20")
mainframe.grid(column=0, row=0, sticky=(N, W, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

command_out = StringVar()
response = StringVar()
slave_address = StringVar()
ip_address = StringVar()
mod_function = StringVar()
quantity = StringVar()
start_register = StringVar()
new_value = StringVar()
endian = StringVar()

# response.set("Waiting for your command!\n")
ip_address.set("/dev/ttyUSB0")
slave_address.set("1")
quantity.set("10")
mod_function.set("3")
start_register.set("2106")
endian.set("Big")

ip_set = ttk.Entry(mainframe, width=30, textvariable=ip_address)
ttk.Label(mainframe, text="address").grid(column=2, row=1, sticky=W)
ip_set.grid(column=1, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Connect", command=connect_to_accuload).grid(column=3, row=1, sticky=W)

ttk.Label(mainframe, text="Function").grid(column=3, row=2, sticky=W)
ttk.Radiobutton(mainframe,text="1",variable=mod_function, value="1").grid(column=4,row=2,sticky=N)
ttk.Radiobutton(mainframe,text="2",variable=mod_function, value="2").grid(column=4,row=3,sticky=N)
ttk.Radiobutton(mainframe,text="3",variable=mod_function, value="3").grid(column=4,row=4,sticky=N)
ttk.Radiobutton(mainframe,text="4",variable=mod_function, value="4").grid(column=4,row=5,sticky=N)
ttk.Radiobutton(mainframe,text="5",variable=mod_function, value="5").grid(column=5,row=2,sticky=N)
ttk.Radiobutton(mainframe,text="6",variable=mod_function, value="6").grid(column=5,row=3,sticky=N)
ttk.Radiobutton(mainframe,text="15",variable=mod_function, value="15").grid(column=5,row=4,sticky=N)
ttk.Radiobutton(mainframe,text="16",variable=mod_function, value="16").grid(column=5,row=5,sticky=N)

ttk.Label(mainframe, text="Endian-ness").grid(column=6, row=2, sticky=W)
ttk.Radiobutton(mainframe,text="Big",variable=endian, value="Big").grid(column=7,row=3,sticky=W)
ttk.Radiobutton(mainframe,text="Little8",variable=endian, value="Little8").grid(column=7,row=4,sticky=W)
ttk.Radiobutton(mainframe,text="Little16",variable=endian, value="Little16").grid(column=7,row=5,sticky=W)

# ttk.Label(mainframe, textvariable=response).grid(column=1, row=7, sticky=(W, E, N, S))

T = Text(root, height=40, width=100)
T.grid(column=0, row=1, sticky=(W, E, N, S), )
# T.config(state=DISABLED)
Scroll = Scrollbar(root)
Scroll.grid(column=1, row=1, sticky=(N, E, W, S), ipadx=2)
Scroll.config(command=T.yview)
T.config(yscrollcommand=Scroll.set)
T.insert(END, "Waiting for your command!\n")

for child in mainframe.winfo_children(): 
	child.grid_configure(padx=5, pady=5)

ip_set.focus()
root.bind('<Return>', connect_to_accuload)

root.after(250,HAMMER)
root.mainloop()

ALIV.close()
