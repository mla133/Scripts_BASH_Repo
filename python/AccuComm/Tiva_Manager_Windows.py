#!/usr/bin/python

#Changle Log
#1.0.0 - Initial Release
#2.0.0 - Modified to use the new MD5 Checksum Image Verification Scheme

import socket
import yaml
import sys
import os
from ttk import *
from Tkinter import *
import tkMessageBox
import time
import socket
import json
import hashlib
import hmac
import base64
import array
from collections import OrderedDict
from collections import namedtuple
from struct import *
from ScrolledText import ScrolledText
import tkFont
import tkFileDialog
#mport pyudev
#from pyudev import Context, Monitor
#import glib

#Defines
FIRMWARE_FILE_NAME = "./liop.bin"
TIVA_BOARDS = {'A4M':0, 'A4B':0, 'A4I1':0, 'A4I2':0,}
TIVA_IP_ADDR = {'A4M':'fd00::2', 'A4B':'fd00::3', 'A4I1':'fd00::4', 'A4I2':'fd00::5'}
COMMAND_PORT=6083
UPDATE_PORT=3210
PACKET_SIZE=1400
ERRORS = {0:'No Error', 1:'Tiva TCP Timeout', 2:'Boot Error', 3:'Upgrade Error', 4:'No firmware', 5:'Firmware CRC Error', 6:'Bootloader CRC Error'}
STATES = {0:'Normal State', 1:'Bootloader State', 2:'Erasing State', 3:'Upgrading State'}
BOARDS = ["A4M", "A4B", "A4I1", "A4I2"]

KEY = bytearray(    [0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B, 0x0B,
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

crc32_reset_value = 0xffffffff;

crc32tab = array.array('I', [
0x00000000L, 0x77073096L, 0xEE0E612CL, 0x990951BAL, 0x076DC419L, 0x706AF48FL, 0xE963A535L, 0x9E6495A3L,
0x0EDB8832L, 0x79DCB8A4L, 0xE0D5E91EL, 0x97D2D988L, 0x09B64C2BL, 0x7EB17CBDL, 0xE7B82D07L, 0x90BF1D91L,
0x1DB71064L, 0x6AB020F2L, 0xF3B97148L, 0x84BE41DEL, 0x1ADAD47DL, 0x6DDDE4EBL, 0xF4D4B551L, 0x83D385C7L,
0x136C9856L, 0x646BA8C0L, 0xFD62F97AL, 0x8A65C9ECL, 0x14015C4FL, 0x63066CD9L, 0xFA0F3D63L, 0x8D080DF5L,
0x3B6E20C8L, 0x4C69105EL, 0xD56041E4L, 0xA2677172L, 0x3C03E4D1L, 0x4B04D447L, 0xD20D85FDL, 0xA50AB56BL,
0x35B5A8FAL, 0x42B2986CL, 0xDBBBC9D6L, 0xACBCF940L, 0x32D86CE3L, 0x45DF5C75L, 0xDCD60DCFL, 0xABD13D59L,
0x26D930ACL, 0x51DE003AL, 0xC8D75180L, 0xBFD06116L, 0x21B4F4B5L, 0x56B3C423L, 0xCFBA9599L, 0xB8BDA50FL,
0x2802B89EL, 0x5F058808L, 0xC60CD9B2L, 0xB10BE924L, 0x2F6F7C87L, 0x58684C11L, 0xC1611DABL, 0xB6662D3DL,
0x76DC4190L, 0x01DB7106L, 0x98D220BCL, 0xEFD5102AL, 0x71B18589L, 0x06B6B51FL, 0x9FBFE4A5L, 0xE8B8D433L,
0x7807C9A2L, 0x0F00F934L, 0x9609A88EL, 0xE10E9818L, 0x7F6A0DBBL, 0x086D3D2DL, 0x91646C97L, 0xE6635C01L,
0x6B6B51F4L, 0x1C6C6162L, 0x856530D8L, 0xF262004EL, 0x6C0695EDL, 0x1B01A57BL, 0x8208F4C1L, 0xF50FC457L,
0x65B0D9C6L, 0x12B7E950L, 0x8BBEB8EAL, 0xFCB9887CL, 0x62DD1DDFL, 0x15DA2D49L, 0x8CD37CF3L, 0xFBD44C65L,
0x4DB26158L, 0x3AB551CEL, 0xA3BC0074L, 0xD4BB30E2L, 0x4ADFA541L, 0x3DD895D7L, 0xA4D1C46DL, 0xD3D6F4FBL,
0x4369E96AL, 0x346ED9FCL, 0xAD678846L, 0xDA60B8D0L, 0x44042D73L, 0x33031DE5L, 0xAA0A4C5FL, 0xDD0D7CC9L,
0x5005713CL, 0x270241AAL, 0xBE0B1010L, 0xC90C2086L, 0x5768B525L, 0x206F85B3L, 0xB966D409L, 0xCE61E49FL,
0x5EDEF90EL, 0x29D9C998L, 0xB0D09822L, 0xC7D7A8B4L, 0x59B33D17L, 0x2EB40D81L, 0xB7BD5C3BL, 0xC0BA6CADL,
0xEDB88320L, 0x9ABFB3B6L, 0x03B6E20CL, 0x74B1D29AL, 0xEAD54739L, 0x9DD277AFL, 0x04DB2615L, 0x73DC1683L,
0xE3630B12L, 0x94643B84L, 0x0D6D6A3EL, 0x7A6A5AA8L, 0xE40ECF0BL, 0x9309FF9DL, 0x0A00AE27L, 0x7D079EB1L,
0xF00F9344L, 0x8708A3D2L, 0x1E01F268L, 0x6906C2FEL, 0xF762575DL, 0x806567CBL, 0x196C3671L, 0x6E6B06E7L,
0xFED41B76L, 0x89D32BE0L, 0x10DA7A5AL, 0x67DD4ACCL, 0xF9B9DF6FL, 0x8EBEEFF9L, 0x17B7BE43L, 0x60B08ED5L,
0xD6D6A3E8L, 0xA1D1937EL, 0x38D8C2C4L, 0x4FDFF252L, 0xD1BB67F1L, 0xA6BC5767L, 0x3FB506DDL, 0x48B2364BL,
0xD80D2BDAL, 0xAF0A1B4CL, 0x36034AF6L, 0x41047A60L, 0xDF60EFC3L, 0xA867DF55L, 0x316E8EEFL, 0x4669BE79L,
0xCB61B38CL, 0xBC66831AL, 0x256FD2A0L, 0x5268E236L, 0xCC0C7795L, 0xBB0B4703L, 0x220216B9L, 0x5505262FL,
0xC5BA3BBEL, 0xB2BD0B28L, 0x2BB45A92L, 0x5CB36A04L, 0xC2D7FFA7L, 0xB5D0CF31L, 0x2CD99E8BL, 0x5BDEAE1DL,
0x9B64C2B0L, 0xEC63F226L, 0x756AA39CL, 0x026D930AL, 0x9C0906A9L, 0xEB0E363FL, 0x72076785L, 0x05005713L,
0x95BF4A82L, 0xE2B87A14L, 0x7BB12BAEL, 0x0CB61B38L, 0x92D28E9BL, 0xE5D5BE0DL, 0x7CDCEFB7L, 0x0BDBDF21L,
0x86D3D2D4L, 0xF1D4E242L, 0x68DDB3F8L, 0x1FDA836EL, 0x81BE16CDL, 0xF6B9265BL, 0x6FB077E1L, 0x18B74777L,
0x88085AE6L, 0xFF0F6A70L, 0x66063BCAL, 0x11010B5CL, 0x8F659EFFL, 0xF862AE69L, 0x616BFFD3L, 0x166CCF45L,
0xA00AE278L, 0xD70DD2EEL, 0x4E048354L, 0x3903B3C2L, 0xA7672661L, 0xD06016F7L, 0x4969474DL, 0x3E6E77DBL,
0xAED16A4AL, 0xD9D65ADCL, 0x40DF0B66L, 0x37D83BF0L, 0xA9BCAE53L, 0xDEBB9EC5L, 0x47B2CF7FL, 0x30B5FFE9L,
0xBDBDF21CL, 0xCABAC28AL, 0x53B39330L, 0x24B4A3A6L, 0xBAD03605L, 0xCDD70693L, 0x54DE5729L, 0x23D967BFL,
0xB3667A2EL, 0xC4614AB8L, 0x5D681B02L, 0x2A6F2B94L, 0xB40BBE37L, 0xC30C8EA1L, 0x5A05DF1BL, 0x2D02EF8DL
])

ERROR_ENUMS = {"ERR:00":"Unknown Command", "ERR:01":"Incorrect Number of Arguments", "ERR:02":"Unknown Argument",
		"ERR:03":"Argument Out of Range","ERR:04":"Internal Error"}


#Global Variables
Connections={('A4M','command'):-1, ('A4B','command'):-1, ('A4I1','command'):-1, ('A4I2','command'):-1}
tiva_data=dict()
tiva_firmware_file_path = ""
FTDI = 0
running_loopback = [False, False, False, False]
config_file = -1
current_config = 0
filemenu = 0

#Event Functions
def update_button_press(board):
	print "File" + tiva_firmware_file_path

	if not board:
		if(not tiva_firmware_file_path):
			exit_w_window("", "Firmware Image Not Loaded", 0)
			return 1
		for i in BOARDS:
			if board_views[i,'checkbox_var'].get():
				if Connections[i,'command'] != -1:
					update_firmware(i)
				else:
					board_views[i,'status'].config(text="Not Connected", fg="red")
					window.update_idletasks()
					print i + " Not Connected"
			else:
				board_views[i,'status'].config(text="Not Enabled", fg="orange")
				window.update_idletasks()
				print i + " Not Enabled"
	else:
		print "File" + tiva_firmware_file_path
		if(not tiva_firmware_file_path):
			exit_w_window(board, "Firmware Image Not Loaded", 0)
			return 1
		if board_views[board,'checkbox_var'].get():
				if Connections[board,'command'] != -1:
					update_firmware(board)
				else:
					board_views[board,'status'].config(text="Not Connected", fg="red")
					window.update_idletasks()
					print board + " Not Connected"
		else:
			board_views[board,'status'].config(text="Not Enabled", fg="orange")
			window.update_idletasks()
			print board + " Not Enabled"

def connect_button_press(board):
	if not board:
		for i in BOARDS:
			if board_views[i,'checkbox_var'].get():
				tiva_connect(i)
			else:
				board_views[i,'status'].config(text="Not Enabled", fg="orange")
				window.update_idletasks()
				print i + " Not Enabled"
	else:
		if board_views[board,'checkbox_var'].get():
			tiva_connect(board)
		else:
			board_views[board,'status'].config(text="Not Enabled", fg="orange")
			window.update_idletasks()
			print board + " Not Enabled"

def process_entry(event):
	current_tab = BOARDS[tiva_notebook.index(tiva_notebook.select())]

	if Connections[current_tab,'command'] >= 0:
		if(not current_command.get()):
			return

		print command_entry.get()
		board_views[current_tab, 'text_window'].configure(state='normal')
		board_views[current_tab, 'text_window'].insert(END, current_command.get(), 'send')
		board_views[current_tab, 'text_window'].insert(END, '\n')
		board_views[current_tab, 'text_window'].see(END)


		try:
			print current_command.get()
			command_ret = send_command(current_command.get(), Connections[current_tab, 'command'])
			current_command.set("")
			print command_ret
		except NameError, msg:
			print msg
			exit_w_window(current_tab, msg, 0)
			board_views[current_tab,'status'].config(text="Command Failed", fg="red")
			board_views[current_tab, 'text_window'].configure(state=DISABLED)
			board_views[current_tab,'update_button'].config(state=DISABLED)
			return

		if command_ret in ERROR_ENUMS:
			board_views[current_tab, 'text_window'].insert('end', command_ret + '\n', 'err')
			board_views[current_tab, 'text_window'].see(END)
		else:
			board_views[current_tab, 'text_window'].insert('end', command_ret + '\n', 'recv')
			board_views[current_tab, 'text_window'].see(END)
	else:
		current_command.set("")
		exit_w_window(current_tab,"Not Connected" , 0)
		board_views[current_tab,'status'].config(text="Not Connected", fg="red")

	board_views[current_tab, 'text_window'].configure(state=DISABLED)
	return

def clear_button_pressed():
	current_tab = BOARDS[tiva_notebook.index(tiva_notebook.select())]

	board_views[current_tab, 'text_window'].configure(state='normal')
	board_views[BOARDS[tiva_notebook.index(tiva_notebook.select())], 'text_window'].delete("1.0",END)
	board_views[current_tab, 'text_window'].configure(state=DISABLED)
	window.update_idletasks()

def tab_changed(event):
	current_tab = tiva_notebook.index(tiva_notebook.select())
	#Stop Any SPLB Tests
	for i in range(0, 4):
		if running_loopback[i]:
			if start_splb(i, 0, 0):
				running_loopback[i] = False

			splb_label.configure(fg="red")
			serial_mode.set(0)
			splb_off.select()

def port_changed(event):
	for i in range(0, 4):
		if running_loopback[i]:
			if start_splb(i, 0, 0):
				running_loopback[i] = False

			splb_label.configure(fg="red")
			serial_mode.set(0)
			splb_off.select()
			splb()

def splb():
	global running_loopback
	current_tab = tiva_notebook.index(tiva_notebook.select())
	mode = serial_mode.get()
	port =  splb_port_val.get()

	if running_loopback[current_tab]:
		if start_splb(current_tab, 0, 0):
			print "Stopping Test"
			running_loopback[current_tab] = False
			splb_label.configure(fg="red")

	if Connections[BOARDS[current_tab],'command'] == -1:
		exit_w_window(BOARDS[current_tab],"Not Connected" , 0)
		serial_mode.set(0)
		splb_off.select()
		return

	if not board_views[BOARDS[current_tab],'checkbox_var'].get():
		exit_w_window(BOARDS[current_tab],"Not Enabled" , 0)
		serial_mode.set(0)
		splb_off.select()
		return

	#There are No Serial Ports on the A4B
	if BOARDS[current_tab] == "A4B" and mode != 0:
		exit_w_window(BOARDS[current_tab],"No Serial Ports Available" , 0)
		serial_mode.set(0)
		splb_off.select()
		return

	if BOARDS[current_tab] == "A4I1":
		if port != "1":
			exit_w_window(BOARDS[current_tab],"Only Port 1 is Available" , 0)
			serial_mode.set(0)
			splb_off.select()
			return
	elif BOARDS[current_tab] == "A4I2":
		if port != "1":
			exit_w_window(BOARDS[current_tab],"Only Port 1 is Available" , 0)
			serial_mode.set(0)
			splb_off.select()
			return

	if mode == 1:
		#Make Sure the Port Support RS232
		if BOARDS[current_tab] == "A4M":
			if port == "3":
				exit_w_window(BOARDS[current_tab],"Port 3 Only Supports RS485" , 0)
				serial_mode.set(0)
				splb_off.select()
				return

		if start_splb(current_tab, mode, port):
			running_loopback[current_tab] = True
			splb_label.configure(fg="green4")
		else:
			splb_label.configure(fg="red")
			serial_mode.set(0)
			splb_off.select()

	elif mode == 2:
		#Make Sure the Port Support RS232
		if BOARDS[current_tab] == "A4M":
			if port == "4":
				exit_w_window(BOARDS[current_tab],"Port 4 Only Supports RS232" , 0)
				serial_mode.set(0)
				splb_off.select()
				return

		if start_splb(current_tab, mode, port):
			running_loopback[current_tab] = True
			splb_label.configure(fg="green4")
		else:
			splb_label.configure(fg="red")
			serial_mode.set(0)
			splb_off.select()

	elif mode == 3:
		#Make Sure the Port Support RS232
		if BOARDS[current_tab] == "A4M":
			if port != "1":
				exit_w_window(BOARDS[current_tab],"Only Port 1 Supports CTS/RTS" , 0)
				serial_mode.set(0)
				splb_off.select()
				return

			if start_splb(current_tab, mode, port):
				running_loopback[current_tab] = True
				splb_label.configure(fg="green4")
			else:
				splb_label.configure(fg="red")
				serial_mode.set(0)
				splb_off.select()

		else:
			exit_w_window(BOARDS[current_tab],"Only Port 1 on the A4M Supports CTS/RTS" , 0)
			serial_mode.set(0)
			splb_off.select()

def start_splb(board, mode, port):
	if mode == 0:
		print "Stop SPLB Test on Port " + str(port) + " On the " + BOARDS[board]
		splb_command = "SPLB 0"

	elif mode == 1:
		print "Start RS232 SPLB Test on Port " + str(port) + " On the " + BOARDS[board]
		splb_command = "SPLB " + str(port) + " 0"

	elif mode == 2:
		print "Start RS485 SPLB Test on Port " + str(port) + " On the " + BOARDS[board]
		splb_command = "SPLB " + str(port) + " 1"

	elif mode == 3:
		print "Start CTS/RTS SPLB Test on Port " +str(port) + " On the " + BOARDS[board]
		splb_command = "SPLB 1"

	try:
		print "Sending Command"
		command_ret = send_command(splb_command, Connections[BOARDS[board],'command'])
	except NameError, msg:
		print msg
		exit_w_window(board, msg, 0)
		print "Stop SPLB"
		return 0

	print "Sent Command"
	if not command_ret in ERROR_ENUMS:
		splb_label.configure(fg="green4")
		board_views[BOARDS[board], 'text_window'].configure(state='normal')
		board_views[BOARDS[board], 'text_window'].insert(END, command_ret, 'recv')
		board_views[BOARDS[board], 'text_window'].insert(END, '\n')
		board_views[BOARDS[board], 'text_window'].see(END)
		board_views[BOARDS[board], 'text_window'].configure(state=DISABLED)
	else:
		if command_ret in ERROR_ENUMS:
			board_views[BOARDS[board], 'text_window'].configure(state='normal')
			board_views[BOARDS[board], 'text_window'].insert('end', command_ret + '\n', 'err')
			board_views[BOARDS[board], 'text_window'].insert(END, '\n')
			board_views[BOARDS[board], 'text_window'].see(END)
			board_views[BOARDS[board], 'text_window'].configure(state=DISABLED)
			print "Stop SPLB"
			return 0

	return 1

def open_file(file_path):
	global tiva_firmware_file_path
	global filemenu
	if not file_path:
    	# defining options for opening a directory
  		options = {}
		options['initialdir'] = '~/Desktop'
		#options['mustexist'] = False
		options['parent'] = window
		#options['title'] = 'This is a title'
		options['filetypes']=[('Image Files','.bin')]
		tiva_firmware_file_path = tkFileDialog.askopenfilename(**options)
		if tiva_firmware_file_path:
			if not tiva_firmware_file_path in current_config['recent_files']:
				if len(current_config['recent_files']) < 5:
					current_config['recent_files'].append(tiva_firmware_file_path)
					config_file = open(os.path.expanduser("~/.Tiva_Manager/config.txt"), "w")
					yaml.dump(current_config, config_file)
					filemenu.add_command(label=tiva_firmware_file_path, command=make_lambda(tiva_firmware_file_path), font=("Times", 14, "bold"))
					window.update_idletasks()
				else:
					del current_config['recent_files'][0]
					current_config['recent_files'].append(tiva_firmware_file_path)
					config_file = open(os.path.expanduser("~/.Tiva_Manager/config.txt"), "w")
					config_file.write(yaml.dump(current_config))
					filemenu.delete(3, 8)
					for i in current_config['recent_files']:
						filemenu.add_command(label=i, command=make_lambda(i), font=("Times", 14, "bold"))
		else:
			print "Cancel"
	else:
		tiva_firmware_file_path = file_path


def exit_program():

	config_file.close()
	for i in BOARDS:
		if i in Connections:
			if Connections[i]['command'] > 0:
				Connections[i]['command'].close()
			if Connections[i]['update'] > 0:
				Connections[i]['update'].close()
	observer.stop()
	exit(1)

#Utility Functions
def exit_w_window(board, message, exit_after):
	#System Error
	if not board:
		print 'System:' + str(message)
		tkMessageBox.showinfo("Error", 'System:' + str(message))
	else:
		print board + ":" + str(message)
		tkMessageBox.showinfo("Error", board + ':' + str(message))
	if exit_after:
		exit_program()

def create_pad_bufs():

  	for i in range(0, 64):
     		i_pad[i] ^= 0x36;  # These magic values are defined in RFC 2104.
    		o_pad[i] ^= 0x5C;

def format_json(input):
	values = OrderedDict([("ts",279811), ("seq",format_json.counter), ("id","beaglebone"), ("seg",[OrderedDict([("type","cmd"),("ins",0),("text",input)])])])
	json_string = json.dumps(values, separators=(',', ':'), sort_keys=False)

	hash = (hmac.new(KEY, bytes(json_string).encode('utf-8'), digestmod=hashlib.sha256).hexdigest())

	out_packet = "3000"
	out_packet +="{\"h\":["

	for i in range(0, 32):
		out_packet += "\"" + hash[(i*2):((i*2)+2)] + "\","

	out_packet = out_packet[:-1]

	out_packet += "]," + json_string[1:]

	format_json.counter+=1;

	#Pad the Packet
	for i in range(0, 3000 - len(out_packet)):
		out_packet += " "
	return out_packet
format_json.counter = 1

def decode_json(json_input):

	tags = json.loads(json_input)
	recv_hash = ''.join(tags['h'])

	#Find the Hash in the JSON String
	hash_index = json_input.find("\"h\":")
	hash_input = json_input[:hash_index - 1]
	hash_input += '}'

	calc_hash = (hmac.new(KEY, bytes(hash_input).encode('utf-8'), digestmod=hashlib.sha256).hexdigest())

	if recv_hash != calc_hash :
		print "\nCalculated Hash\t" + calc_hash
		print "Received Hash\t" + recv_hash + "\n"
		return -1

	return tags['text']

def send_command(command, sock):

	try:
		sock.send(format_json(command));
	except socket.error, socket.timeout:
		raise NameError('Send Timeout')
		return -1
	try:
		recv_packet = sock.recv(PACKET_SIZE)
	except socket.error, socket.timeout:
		raise NameError('Receive Timeout')
		return -1

	tiva_ret = decode_json(recv_packet)

	#Bootloader CRC
	if tiva_ret == -1:
		raise NameError('HashError')
		return -1
	return tiva_ret


def tiva_connect(board):

	#Open the Connection
	board_views[board,'status'].config(text="Attempting to Connect...", fg="blue")
	board_views[board,'update_button'].config(state=DISABLED)
	window.update_idletasks()
	try:
		Connections[board,'command'] = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		Connections[board,'command'].settimeout(5)
		Connections[board,'command'].setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		#Connections[board,'command'].setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
		#Connections[board,'command'].setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
		#Connections[board,'command'].setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
		Connections[board,'command'].connect((TIVA_IP_ADDR[board], COMMAND_PORT))

	except (socket.error, socket.timeout), msg:
		Connections[board,'command'] = -1;
		board_views[board,'prog'].config(value=0)
		board_views[board,'status'].config(text="Connect Failed", fg="red")
		board_views[board,'update_button'].config(state=DISABLED)
		window.update_idletasks()
		exit_w_window(board, msg, 0)
		return 1

	#Get the Status, State, CRC, and Version
	board_views[board,'status'].config(text="Getting Data", fg="blue")
	board_views[board,'prog'].step(25)
	window.update_idletasks()

	try:
		tiva_data[board,'BL_VER'] = send_command("GET 1", Connections[board,'command'])
		board_views[board,'BL_VER'].config(text="Bootloader Version: \t0x" + tiva_data[board,'BL_VER'])
		board_views[board,'prog'].step(15)
		window.update_idletasks()

		tiva_data[board,'BL_CRC'] =  send_command("GET 2", Connections[board,'command'])
		board_views[board,'BL_CRC'].config(text="Bootloader CRC: \t\t0x" + tiva_data[board,'BL_CRC'][:8])
		board_views[board,'prog'].step(15)
		window.update_idletasks()

		tiva_data[board,'FW_VER'] = send_command("GET 3", Connections[board,'command'])
		board_views[board,'FW_VER'].config(text="Firmware Version: \t0x" + tiva_data[board,'FW_VER'])
		board_views[board,'prog'].step(15)
		window.update_idletasks()

		tiva_data[board,'FW_CRC'] = send_command("GET 4", Connections[board,'command'])
		board_views[board,'FW_CRC'].config(text="Firmware CRC: \t\t0x" + tiva_data[board,'FW_CRC'][:8])
		board_views[board,'prog'].step(15)
		window.update_idletasks()

		tiva_data[board,'STATE'] = send_command("RS", Connections[board,'command'])
		board_views[board,'STATE'].config(text="Tiva State: \t\t" + STATES[int(tiva_data[board,'STATE'])])
		board_views[board,'prog'].step(15)
		window.update_idletasks()

		tiva_data[board,'ERROR'] = send_command("RE", Connections[board,'command'])
		board_views[board,'ERROR'].config(text="Tiva Error: \t\t" + ERRORS[int(tiva_data[board,'ERROR'])])
		board_views[board,'prog'].step(15)
		window.update_idletasks()
	except NameError, msg:
		print msg
		exit_w_window(board, msg, 0)
		board_views[board,'status'].config(text="Connect Failed", fg="red")
		board_views[board,'update_button'].config(state=DISABLED)
		return 1

	board_views[board,'status'].config(text="Connected", fg="green4")
	board_views[board,'prog'].config(value=0)

	#Enable the Update Buttons
	board_views[board,'update_button'].config(state="normal")

#This calculates and returns the crc32 of an entire block
def calc_block_crc32(data, size):

   	running_crc = 0xffffffff;
	i = 0
	#size -= 1

	while(size > 0):
      		running_crc = (running_crc >> 8) ^ crc32tab[(running_crc ^ data[i]) & 0xFF]
		i+=1
		size-=1
   	return ~(running_crc)

def calc_md5_sum(file_name):
    hash_lib = hashlib.md5()

    with open(file_name, "rb") as f:
        for i in iter(lambda: f.read(4096), b""):
            hash_lib.update(i)
    return hash_lib.digest()

def update_firmware(board):

	file_size = os.path.getsize(tiva_firmware_file_path)

	#Open the Firmware File
	tiva_firmware_file = open(tiva_firmware_file_path, 'r')

	image_buffer = bytearray(tiva_firmware_file.read())

	file_crc = calc_md5_sum(tiva_firmware_file_path)

	if str(file_crc) != str(tiva_data[board,'FW_CRC']):

		tiva_data[board,'FW_LEN'] = file_size
		tiva_data[board,'FW_VER'] = 0
		tiva_data[board,'FW_CRC'] = file_crc
		tiva_data[board,'BL_CRC'] = bytearray(32)

		print file_size
		print tiva_data[board,'FW_CRC']
		print tiva_data[board,'BL_CRC']

		board_views[board,'status'].config(text="Attempting to Update...", fg="blue")
		window.update_idletasks()

		try:
			#Force the Tiva into the Update State
			ret_val = send_command("SC 1", Connections[board,'command'])
			ret_val = send_command("PC", Connections[board,'command'])
			time.sleep(3)
		except NameError, msg:
			print msg
			exit_w_window(board, msg, 0)
			board_views[board,'status'].config(text="Update Failed", fg="red")
			board_views[board,'update_button'].config(state=DISABLED)
			return 1

		try:
			Connections[board,'update'] = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			Connections[board,'update'].settimeout(10)
			Connections[board,'update'].connect((TIVA_IP_ADDR[board], UPDATE_PORT))
		except (socket.error, socket.timeout), msg:
			board_views[board,'prog'].config(value=0)
			board_views[board,'status'].config(text="Update Failed", fg="red")
			board_views[board,'update_button'].config(state=DISABLED)
			exit_w_window(board, msg, 0)
			return 1

			sock.setblocking(1)

		#Send the EERPOM Info
		packed_data = pack('=I16sI16sIIIIIII', 0, str(tiva_data[board, 'BL_CRC']), tiva_data[board,'FW_VER'], tiva_data[board,'FW_CRC'], 0x30000, tiva_data[board,'FW_LEN'], 0, 0, 0, 0, 0)	

		num_bytes_sent = Connections[board,'update'].send(packed_data)

		#Send Firmware
		num_bytes_sent = 0
		while num_bytes_sent < file_size:
			try:
				if((file_size - num_bytes_sent) < PACKET_SIZE):
                			rc = Connections[board,'update'].send((image_buffer[num_bytes_sent:file_size]), (file_size - num_bytes_sent));
            			else:
               				rc = Connections[board,'update'].send((image_buffer[num_bytes_sent:(num_bytes_sent+PACKET_SIZE)]), PACKET_SIZE);
				num_bytes_sent += rc;

				if(Connections[board,'update'].recv(PACKET_SIZE) is "OK"):
					return 1
			except (socket.error, socket.timeout), msg:
				board_views[board,'prog'].config(value=0)
				board_views[board,'status'].config(text="Update Failed", fg="red")
				board_views[board,'update_button'].config(state=DISABLED)
				window.update_idletasks()
				Connections[board,'update'].close()
				Connections[board,'command'].close()
				tiva_firmware_file.close()
				exit_w_window(board, msg, 0)
				return 1

			board_views[board,'prog'].config(value=(int((float(num_bytes_sent) / file_size) * 100)))
			window.update_idletasks()

		print "Closing Socket"
		Connections[board,'update'].close()
		Connections[board,'command'].close()
		tiva_firmware_file.close()
		print "Socket Closed"

		board_views[board,'status'].config(text="Finished, Reconnecting...", fg="blue")
		window.update_idletasks()
		time.sleep(5)

		#Reconnect
		tiva_connect(board)

		#Verify the Update Succeeded
		Connections[board,'update'].close()

def create_config_file(file):
	global current_config
	cfg = 0
	cfg = {'recent_files':[]}
	current_config = cfg
	yaml.dump(cfg, file)

def get_block_infos(action, dev):
	global FTDI
	print dev.get('ID_MODEL_ID')
	print dev.get('ID_VENDOR_ID')
	global FTDI
	if dev.get('ID_MODEL_ID') == "6015" and dev.get('ID_VENDOR_ID') == "0403":
		if (dev.get('DEVNAME')) and ('dev/ttyUSB' in dev.get('DEVNAME')):
			print('Device name: %s' % dev.get('DEVNAME'))
			if action == 'add':
				FTDI+=1;
			elif action == 'remove':
				FTDI-=1;

		if FTDI > 0:
			ftdi_num.config(text=FTDI, fg="green4")
			ftdi_label.config(fg="green4")
		else:
			ftdi_num.config(text=FTDI, fg="red")
			ftdi_label.config(fg="red")

def make_lambda(arg):
	return lambda:open_file(arg)

#Open the Configuration File
if not os.path.isdir(os.path.expanduser(".Tiva_Manager")):
	os.makedirs(os.path.expanduser(".Tiva_Manager"))

if not os.path.isfile(os.path.expanduser(".Tiva_Manager/config.txt")):
	print "Creating Configuration File"
	config_file = open(os.path.expanduser(".Tiva_Manager/config.txt"), "w")
	create_config_file(config_file)
else:
	print "Openning Configuration File"
	config_file = open(os.path.expanduser(".Tiva_Manager/config.txt"), "r+")
	current_config = yaml.safe_load(config_file)

config_file.close()

#Create Widget Arrays to Reduce Code
board_views = {}

#Create a Window
window = Tk()
window.title("Tiva Manager 2.0.0")
window.geometry("1200x700")
#window.resizable(width=FALSE, height=FALSE)

#Create the Menu Bar
menu = Menu(window)
window.config(menu=menu)

#dFont=tkFont.Font(family="Arial", size=15)
#style = Style()
#style.configure('.',font=dFont)

filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu, font=("Times", 14, "bold"))

filemenu.add_command(label="Open", command=make_lambda(''), font=("Times", 14, "bold"))
filemenu.add_command(label="Exit", command=exit_program, font=("Times", 14, "bold"))
filemenu.add_command(label="Recent Files", font=("Times", 14, "bold"), background='white', state=DISABLED)
for i in current_config['recent_files']:
	filemenu.add_command(label=i, command=make_lambda(i), font=("Times", 14, "bold"))



connect_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Connections", menu=connect_menu, font=("Times", 14, "bold"))
connect_menu.add_command(label="Connect All", command=lambda:connect_button_press(''), font=("Times", 14, "bold"))
connect_menu.add_command(label="Upload All", command=lambda:update_button_press(''), font=("Times", 14, "bold"))

helpmenu = Menu(menu, tearoff=False)
helpmenu.config(font=("Times", 14, "bold"))
menu.add_cascade(label="Help", menu=helpmenu, font=("Times", 14, "bold"))
helpmenu.add_command(label="About", font=("Times", 14, "bold"))

#Create the Root Frame
root_frame = Frame(window)

Grid.rowconfigure(root_frame, 0, weight=1)
Grid.columnconfigure(root_frame, 0, weight=1)

root_frame.grid(column=0, row=0, sticky=(N, E, W, S))
default_gray = window.cget('bg')

#Create the Tabs
s = Style()

s.theme_settings("default", settings={

        "TButton": {
            "configure": {"width": 15, "anchor": "center", "background":"gray"}
        },
		"Horizontal.TProgressbar": {"configure": {"background":"green4","forground":"green4"}},
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "red", "font":("Times", 14, "bold") },
            "map":       {"background": [("selected", "green4")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )

s.theme_use("default")

tiva_notebook = Notebook(root_frame)
tiva_notebook.grid(column=0, row=1, columnspan=3, sticky=(N, E, W, S))

for i in range(0,4):
	board_views[BOARDS[i],'frame'] = Frame(root_frame, borderwidth=1, width=50, height=50)
	board_views[BOARDS[i],'frame'].grid(column=i, row=0, padx=20, sticky=(N, E, W, S))

	board_views[BOARDS[i],'title'] = Label(board_views[BOARDS[i],'frame'], text=BOARDS[i]);
	board_views[BOARDS[i],'title'].grid(column=i, row=0);

	board_views[BOARDS[i],'status'] = Label(board_views[BOARDS[i],'frame'], text="Not Connected", fg="red");
	board_views[BOARDS[i],'status'].grid(column=i, row=1);

	board_views[BOARDS[i],'prog'] = Progressbar(board_views[BOARDS[i],'frame'], orient=HORIZONTAL, length=250, mode='determinate', value=0, maximum=100)
	board_views[BOARDS[i],'prog'].grid(column=i, row=2, pady=5)

	board_views[BOARDS[i],'BL_CRC'] = Label(board_views[BOARDS[i],'frame'], text="Bootloader CRC: \t\tN/A");
	board_views[BOARDS[i],'BL_CRC'].grid(column=i, row=3, sticky=(W));

	board_views[BOARDS[i],'BL_VER'] = Label(board_views[BOARDS[i],'frame'], text="Bootloader Version: \tN/A");
	board_views[BOARDS[i],'BL_VER'].grid(column=i, row=4, sticky=(W));

	board_views[BOARDS[i],'FW_CRC'] = Label(board_views[BOARDS[i],'frame'], text="Firmware CRC: \t\tN/A");
	board_views[BOARDS[i],'FW_CRC'].grid(column=i, row=5, sticky=(W));

	board_views[BOARDS[i],'FW_VER'] = Label(board_views[BOARDS[i],'frame'], text="Firmware Version: \tN/A");
	board_views[BOARDS[i],'FW_VER'].grid(column=i, row=6, sticky=(W));

	board_views[BOARDS[i],'STATE'] = Label(board_views[BOARDS[i],'frame'], text="Tiva State: \t\tN/A");
	board_views[BOARDS[i],'STATE'].grid(column=i, row=7, sticky=(W));

	board_views[BOARDS[i],'ERROR'] = Label(board_views[BOARDS[i],'frame'], text="Tiva Error: \t\tN/A");
	board_views[BOARDS[i],'ERROR'].grid(column=i, row=8, sticky=(W));

	board_views[BOARDS[i],'connect_button'] = Button(board_views[BOARDS[i],'frame'], text="Connect to " + BOARDS[i])
	board_views[BOARDS[i],'connect_button'].grid(column=i, row=9, sticky=(W))

	board_views[BOARDS[i],'update_button'] = Button(board_views[BOARDS[i],'frame'], text="Update " + BOARDS[i], state=DISABLED)
	board_views[BOARDS[i],'update_button'].grid(column=i, row=10, sticky=(W))

	board_views[BOARDS[i],'checkbox_var'] = IntVar()
	board_views[BOARDS[i],'checkbox'] = Checkbutton(board_views[BOARDS[i],'frame'], text="Enable", variable=board_views[BOARDS[i],'checkbox_var'])
	board_views[BOARDS[i],'checkbox'].grid(column=i, row=0, sticky=(E))

	#Command Window
	board_views[BOARDS[i], 'tab'] = Frame()
	tiva_notebook.add(board_views[BOARDS[i], 'tab'], text=BOARDS[i])

	board_views[BOARDS[i], 'text_window'] = ScrolledText(board_views[BOARDS[i], 'tab'], state='disabled')
	#board_views[BOARDS[i], 'text_window']['font'] = ('consolas', '12')
	board_views[BOARDS[i], 'text_window'].pack(fill='x')
	board_views[BOARDS[i], 'text_window'].tag_config('send', foreground='blue')
	board_views[BOARDS[i], 'text_window'].tag_config('recv', foreground='green4')
	board_views[BOARDS[i], 'text_window'].tag_config('err', foreground='red')

#Bind the Notebook Tabs to the Change Tab Function
tiva_notebook.bind_all("<<NotebookTabChanged>>", tab_changed)

#You Must do the Outside of the Loop
board_views["A4M",'connect_button'].configure(command=lambda:connect_button_press("A4M"))
board_views["A4M",'update_button'].configure(command=lambda:update_button_press("A4M"))

board_views["A4B",'connect_button'].configure(command=lambda:connect_button_press("A4B"))
board_views["A4B",'update_button'].configure(command=lambda:update_button_press("A4B"))

board_views["A4I1",'connect_button'].configure(command=lambda:connect_button_press("A4I1"))
board_views["A4I1",'update_button'].configure(command=lambda:update_button_press("A4I1"))

board_views["A4I2",'connect_button'].configure(command=lambda:connect_button_press("A4I2"))
board_views["A4I2",'update_button'].configure(command=lambda:update_button_press("A4I2"))

#Command Entry
entry_frame = Frame(root_frame)
entry_frame.grid(column=0, row=2, columnspan=3, sticky=(W, E))

current_command = StringVar()
#current_command.set("Enter a Command")
command_entry = Entry(entry_frame, bd=1, bg='white', justify=LEFT, textvariable=current_command)
command_entry.bind('<Return>', process_entry)
command_entry.bind('<KP_Enter>', process_entry)
command_entry.pack(side=LEFT, fill='x', expand=1)

command_button = Button(entry_frame, text="Send", command=lambda:process_entry("Node"))
command_button.pack(side=LEFT)

clear_commands = Button(entry_frame, text="Clear", command=clear_button_pressed)
clear_commands.pack(side=RIGHT)

#SPLB/FTDI Settings
splb_frame = Frame(root_frame, borderwidth=1, width=50, height=50)
splb_frame.grid(column=3, row=1, sticky=(N, E, W, S))

ftdi_label = Label(splb_frame, text='Number of FTDIs Connected:');
ftdi_label.grid(column=0, row=0, sticky=(N, E))
ftdi_num = Label(splb_frame, text='0');
ftdi_num.grid(column=1, row=0)

serial_mode = IntVar()
splb_label = Label(splb_frame, text='Serial Loopback Test', fg='red');
splb_label.grid(column=0, row=1, pady=20, sticky=(N, W))

port_label = Label(splb_frame, text='Comm Port Number: ');
port_label.grid(column=0, row=2, sticky=(N, W))

splb_port_val = StringVar(splb_frame)
splb_port_val.set("1")
splb_port = OptionMenu(splb_frame, splb_port_val, "1", "2", "3", "4", command=port_changed)
splb_port.grid(column=1, row=2,  sticky=(N, W))

splb_off = Radiobutton(splb_frame, text="Off", variable=serial_mode, value=0, command=splb)
splb_off.grid(column=0, row=3, sticky=(W))
rs232 = Radiobutton(splb_frame, text="RS232", variable=serial_mode, value=1, command=splb)
rs232.grid(column=0, row=4, sticky=(W))
rs485 = Radiobutton(splb_frame, text="RS485", variable=serial_mode, value=2, command=splb)
rs485.grid(column=0, row=5, sticky=(W))
rs485 = Radiobutton(splb_frame, text="CTS/RTS", variable=serial_mode, value=3, command=splb)
rs485.grid(column=0, row=6, sticky=(W))

"""
#Udev Hooks
#Get the Initial Number of FTDI Cables
context = Context()

#Initial Search
for device in context.list_devices():
	if device.get('ID_MODEL_ID') == "6015" and device.get('ID_VENDOR_ID') == "0403":
		if (device.get('DEVNAME')) and ('dev/ttyUSB' in device.get('DEVNAME')):
			FTDI += 1
if FTDI > 0:
	ftdi_num.config(text=FTDI, fg="green4")
	ftdi_label.config(fg="green4")
else:
	ftdi_num.config(text=FTDI, fg="red")
	ftdi_label.config(fg="red")

observer = pyudev.MonitorObserver(Monitor.from_netlink(context), get_block_infos)

observer.start()
"""

window.mainloop()

