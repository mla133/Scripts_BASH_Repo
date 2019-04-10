import sys
import os
import serial
import time
import glob
import socket
import commands

from PySide.QtGui import *
from PySide.QtCore import *

MACRO_COMMANDS = {
"REPEAT",
"ARM",
"WAITFOR",
"WHILE",
"DO",
"DELAY",
"END",
"IF",
"FI",
"GOTO"
}

		
class MacroEngine(QThread):
	updateText = Signal(bytearray, str, int)
       	testStopTest = Signal()
        
	def __init__(self, args = None):
		super(MacroEngine, self).__init__()
		print "Init"
		self.stopFlag = False
		self.responseStatus = 0
		self.currentResponse = bytearray()

		if args is not None:
			self.isSerial = args[0]
			self.currentSerial = args[1]
			self.currentTCP = args[2]
			self.commandBuffer = args[3]
			self.protocol = args[4]

	def stop(self):
		self.stopFlag = True
	
	def stopped(self):
		return self.stopFlag

	def running(self):
		return self.isRunning
	
	def setResponse(self, response):
		self.currentResponse = response
		self.responseStatus = True

	def sendCommand(self, command):
		byteCommand = commands.formatCommand(self.protocol ,command)
		self.updateText.emit(byteCommand, command + "\n", len(byteCommand))
		if(self.isSerial):
		        self.currentSerial.write(byteCommand)
		else:
		        self.currentTCP.sendall(byteCommand)
		if self.stopFlag:
		        self.isRunning = False
		        print "Exiting"
		        return	

		retries = 0
		while 1:
		        if self.stopFlag:
		                self.isRunning = False
		                print "Exiting"
		                return	

		        time.sleep(0.0001)
		        if self.responseStatus == 1:
		                self.responseStatus = 0
		                break
		        else:
		                if retries <= 100000000:
		                        retries += 1
		                else:
		                        print "Timeout"
		                        self.responseStatus = 0
		                        retires = 0
		                        break
		
	def run(self):
		print "Starting Test"
		retries = 0
		command = ""
		tmp_command = ""
		macro_command = ""
		loop_count = []
		loop_type = []
		start_index = []
	
		tmp_start_index = 0
		tmp_index = 0
		tmp_stop_index = 0
		delay_time = 0.0
		total_time = 0.0
		i = 0
		tmp_cmd_index = 0
		not_flag = False
		arm_no = 1

                print self.commandBuffer
		while i < len(self.commandBuffer):
			cmd = self.commandBuffer[i]

	                if self.stopFlag:
	                        self.isRunning = False
	                        print "Exiting"
	                        return
	                
			for j in MACRO_COMMANDS:
				if cmd.find(j, 0, len(j)) == 0:
					macro_command = j
					break
                        print macro_command
			if len(macro_command) > 0:
				if "REPEAT" in macro_command:
					loop_count.append(int(cmd[len("REPEAT "):]))
					loop_type.append(0)

					#Find the Indexes
					start_index.append(i)

				elif "DO" in macro_command:
                                        flag = cmd[len("DO "):]
					
					if flag[0:1] == "!":
						not_flag = True
						flag = flag[1:]
					else:
						not_flag  = False

					#Find the Indexes
					start_index.append(i)
					loop_type.append(1)

				elif "WHILE" in macro_command:
                                        flag = cmd[len("WHILE "):]
					
					if flag[0:1] == "!":
						not_flag = True
						flag = flag[1:]
						print flag
					else:
						not_flag  = False

					#Find the Ending Index
					tmp_cmd_index = i + 1
					while tmp_cmd_index < len(self.commandBuffer):
                                                tmp_cmd = self.commandBuffer[j]
                                                if tmp_cmd == "END":
                                                        break
                                                tmp_cmd_index += 1
                                                                                                
                                        #Check the Status and Jump If Needed
                                        if tmp_cmd_index == i:
                                                print "Error: Missing END Statement"
                                                return

                                        #Do We Need to Skip the Loop Block
                                        self.sendCommand("%02iRS" % arm_no)
                                        if not_flag:
                                                if flag in self.currentResponse:
                                                        i = tmp_cmd_index
                                        elif flag not in self.currentResponse:
                                                i = tmp_cmd_index
                                        else:
                                                tmp_cmd_index = 0        
                                                start_index.append(i)
                                                loop_type.append(2)

				
				elif "END" in macro_command:
                                        #What Type of End is This
                                        if loop_type[len(loop_type) - 1] == 1:
                                                self.sendCommand("%02iRS" % arm_no)
						if not_flag:
							if flag not in self.currentResponse:
								i = start_index[len(loop_type) - 1] 
						elif flag in self.currentResponse:
							i = start_index[len(loop_type) - 1] 
                                                else:
                                                        start_index.pop()
                                                        loop_type.pop()
					else:
                                                loop_count[len(loop_count) - 1] -= 1

                                                if loop_count[len(loop_count) - 1] <= 0:
                                                        start_index.pop()
                                                        loop_count.pop()
                                                        loop_type.pop()
                                                else:
                                                        i = start_index[len(loop_type) - 1]

                                elif "IF" in macro_command:
                                        flag = cmd[len("IF "):]
					
                                        if flag[0:1] == "!":
                                                not_flag = True
                                                flag = flag[1:]
                                        else:
						not_flag  = False
						
					#Find the Ending Index
					tmp_cmd_index = i + 1
					while tmp_cmd_index < len(self.commandBuffer):
                                                tmp_cmd = self.commandBuffer[tmp_cmd_index]
                                                if tmp_cmd == "FI":
                                                        break
                                                tmp_cmd_index += 1
                                        #Check the Status and Jump If Needed
                                        if tmp_cmd_index == i:
                                                print "Error: Missing FI Statement"
                                                return

                                        #Do We Need to Skip the Code Block
                                        self.sendCommand("%02iRS" % arm_no)
                                        if not_flag:
                                                if flag in self.currentResponse:
                                                        i = tmp_cmd_index
                                        elif flag not in self.currentResponse:
                                                i = tmp_cmd_index
                                        else:
                                                tmp_cmd_index = 0        
						
				elif "ARM" in macro_command:
                                        arm_no = int(cmd[len("ARM "):])
                                        
				elif "DELAY" in macro_command:
					total_time = 0.0

					delay_time = float(cmd[len("DELAY "):])
					print delay_time
					if delay_time <= 0.001:
						time.sleep(0.001)
					else:
						while total_time < delay_time:
							total_time += 0.001
							time.sleep(0.001)
							if self.stopFlag:
								self.isRunning = False
								print "Exiting"
								return	

				elif "WAITFOR" in macro_command:
					flag = cmd[len("WAITFOR "):]
					
					if flag[0:1] == "!":
						not_flag = True
						flag = flag[1:]
						print flag
					else:
						not_flag  = False
						print flag

					while True:
						self.sendCommand("%02iRS" % arm_no)
						if self.stopFlag:
							self.isRunning = False
							print "Exiting"
							return	
						if not_flag:
							if flag not in self.currentResponse:
								break
						elif flag in self.currentResponse:
							break

                                elif "GOTO" in macro_command:
                                        tmp_index = int(cmd[len("GOTO "):])
                                        if tmp_index > len(self.commandBuffer):
                                                print "Invalid GOTO Index"
                                        else:
                                                i = tmp_index

				macro_command = ""
				i += 1

				continue

			self.sendCommand(cmd)
			i += 1

                print "Stopping Test"
                self.isRunning = False
                self.testStopTest.emit()

		return

