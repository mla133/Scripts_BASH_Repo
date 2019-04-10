import sys
import os
import serial
import time
import glob
import socket

from PySide.QtGui import *
from PySide.QtCore import *

smith_errors={
	'NO00': 'Command Nonexistent',
	'NO01': 'In Program Mode',
	'NO02': 'Released',
	'NO03': 'Value Rejected',
	'NO04': 'Flow Active',
	'NO05': 'No Transaction Ever Done',
	'NO06': 'Operation Not Allowed',
	'NO07': 'Wrong Control Mode',
	'NO08': 'Transaction In Progress',
	'NO09': 'Alarm Condition',
	'NO10': 'Storage Full',
	'NO11': 'Operation Out Of Sequence',
	'NO12': 'Power Fail During Transaction',
	'NO13': 'Authorized',
	'NO14': 'Program Code Not Used',
	'NO15': 'Display/Keypad In Use',
	'NO16': 'Ticket Not In Printer',
	'NO17': 'No Keypad Data Pending',
	'NO18': 'No Transaction In Progress',
	'NO19': 'Option Not Installed',
	'NO20': 'Start After Stop Delay',
	'NO21': 'Permissive Delay Active',
	'NO22': 'Print Request Pending',
	'NO23': 'No Meter Enabled',
	'NO24': 'Must Be In Program Mode',
	'NO25': 'Ticket Alarm During Transaction',
	'NO26': 'Volume Type Not Selected',
	'NO27': 'Exactly One Recipe Must Be Enabled',
	'NO28': 'Batch Limit Reached',
	'NO29': 'Checking Entries',
	'NO30': 'Product/Recipe/Additive Not Assigned',
	'NO31': 'Invalid Argument for Configuration',
	'NO32': 'No Key Ever Pressed',
	'NO33': 'Maximum Active Arms in Use',
	'NO34': 'Transaction Not Standby',
	'NO35': 'Comm Swing Arm Out of Position',
	'NO36': 'Card-In Required',
	'NO37': 'Data Not Available',
	'NO38': 'Too Many Shared Additives Selected',
	'NO39': 'No Current Batch on This Arm',
	'NO40': 'Invalid on Virtual Arm',
	'NO41': 'No Pending Reports',
	'NO90': 'Must Use Mini Protocol',
	'NO91': 'Buffer Error',
	'NO92': 'Keypad Locked',
	'NO93': 'Data Recall Error',
	'NO94': 'Not In Program Mode',
	'NO95': 'Security Access Not Available',
	'NO96': 'Data Request Queued Ask Later',
	'NO97': 'Comflash Archiving',
	'NO99': 'Internal Error'
}

class command(object):
	def __init__(self, cmd_string, cmd_min, cmd_max, cmd_arg_list, rsp_min, rsp_max, rsp_arg_list):
		self.cmdString = cmd_string
		self.cmdArgList = cmd_arg_list
		self.cmdMin = cmd_min
		self.cmdMax = cmd_max
		self.rspArgList = rsp_arg_list
		self.rspMin = rsp_min
		self.rspMax = rsp_max

	def getAllCommands(self):
		rtnCommands = []

		if self.cmdArgList is not None:
			for i in self.cmdArgList:
				rtnCommands.append(self.cmdString + i)
		elif self.cmdMax != 0:
			for i in range(self.cmdMin, self.cmdMax + 1):
				rtnCommands.append(self.cmdString + str(i))
		else:
			rtnCommands.append(self.cmdString)
			
		return rtnCommands
		
	def getSingleCommand(self, index):
		if self.cmdArgList is not None:
			return CmdString + self.cmdArgList[index]
		return None

	def checkCommand(self, index):
		if index is not None:
			print "None"

	def getCommandHeader(self):
                return self.cmdString
		
full_zz_options = [
"split_arch",
"pulse_in_config",
"pulse_out_config",
"analog_io_config",
"system_config",
"alarm_config",
"load_arm_layout"
]

backwards_compatability_test_commands = [
        command("PV CF", 0, 0, [" %03i" % i for i in range(1, 21)], 0, 0, None),
        command("PV CF", 0, 0, [" %03i" % i for i in range(100, 149)], 0, 0, None),
        command("PV CF", 0, 0, [" %03i" % i for i in range(200, 226)], 0, 0, None),
        command("PV CF", 0, 0, [" %03i" % i for i in range(300, 961)], 0, 0, None),
        command("PV SY", 0, 0, [" %03i" % i for i in range(0, 999)], 0, 0, None),
        command("PV AR", 0, 0, [" %03i" % i for i in range(1, 311)], 0, 0, None),
        command("PV AR", 0, 0, [" %03i" % i for i in range(701, 710)], 0, 0, None),
        command("PV M1", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("PV M2", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("PV M3", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("PV M4", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("PV M5", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("PV M6", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("PV P1", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV P2", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV P2", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV P3", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV P4", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV P5", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV P6", 0, 0, [" %03i" % i for i in range(100, 530)], 0, 0, None),
        command("PV 01", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 02", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 03", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 04", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 05", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 06", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 07", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 08", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 09", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 10", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 11", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 12", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 13", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 14", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 15", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 16", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 17", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 18", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 19", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 20", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 21", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 22", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 23", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 24", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 25", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 26", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 27", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 28", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 29", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 30", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 31", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 32", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 33", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 34", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 35", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 36", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 37", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 38", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 39", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 40", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 41", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 42", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 43", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 44", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 45", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 46", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 47", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 48", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 49", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV 50", 0, 0, [" %03i" % i for i in range(1, 100)], 0, 0, None),
        command("PV BA", 0, 0, [" %03i" % i for i in range(101, 110)], 0, 0, None),
        command("PV BA", 0, 0, [" %03i" % i for i in range(701, 706)], 0, 0, None),
        command("PV BB", 0, 0, [" %03i" % i for i in range(101, 110)], 0, 0, None),
        command("PV BB", 0, 0, [" %03i" % i for i in range(701, 706)], 0, 0, None)
        ]

full_command_test_commands = [
        #command("BV serial_port_config baud_rate 3", 0, 0, None, 0, 0, None),
        #command("BV serial_port_config comm_timeout 3", 0, 0, None, 0, 0, None),
        #command("BV recipe_inj_config inj_vol 25 3", 0, 0, None, 0, 0, None),
        #command("BV product_config diff_press 5 5", 0, 0, None, 0, 0, None),
        #command("BV meter_config od1_units 6 6", 0, 0, None, 0, 0, None),
        #command("BV recipe_config recipe_used 5", 0, 0, None, 0, 0, None),

        #command("XW serial_port_config baud_rate 3 2", 0, 0, None, 0, 0, None),
        #command("XW serial_port_config baud_rate 3 1", 0, 0, None, 0, 0, None),
        #command("PC SY 718 2", 0, 0, None, 0, 0, None),
        #command("PC SY 718 3", 0, 0, None, 0, 0, None),
        #command("PV SY 718", 0, 0, None, 0, 0, None),
        #command("PV SY 713", 0, 0, None, 0, 0, None),
        
        #command("PV SY 718", 0, 0, None, 0, 0, None),
       # command("VT G P1", 0, 0, None, 0, 0, None),
        command("PV M1", 0, 0, [" %03i" % i for i in range(200, 500)], 0, 0, None),
        command("RB 01 001", 0, 0, None, 0, 0, None),
        command("EQ", 0, 0, None, 0, 0, None),
       # command("HI", 0, 0, None, 0, 0, None),
        command("DY SY", 0, 0, ["%02i" % i for i in range(0, 37)], 0, 0, None),
        command("DY IN", 0, 0, ["%02i" % i for i in range(0, 48)], 0, 0, None),
        command("DY P1", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        command("DY P2", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        command("DY P3", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        command("DY P4", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        command("DY P5", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        command("DY P6", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        command("DY CP", 0, 0, ["%02i" % i for i in range(0, 34)], 0, 0, None),
        
        command("DY 01", 0, 0, ["%02i" % i for i in range(0, 5)], 0, 0, None),
        command("DY 02", 0, 0, ["%02i" % i for i in range(0, 5)], 0, 0, None),
        command("DY 03", 0, 0, ["%02i" % i for i in range(0, 5)], 0, 0, None),
        command("DY 04", 0, 0, ["%02i" % i for i in range(0, 5)], 0, 0, None),
        command("DY 05", 0, 0, ["%02i" % i for i in range(0, 5)], 0, 0, None),
        command("DY CR", 0, 0, ["%02i" % i for i in range(0, 5)], 0, 0, None),
        
        command("DY B1", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B2", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B3", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B4", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B5", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B6", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B7", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B8", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY B9", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY BA", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        command("DY CB", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        
        command("DY TR", 0, 0, ["%02i" % i for i in range(0, 36)], 0, 0, None),
        
        command("DY FA", 0, 0, ["%02i" % i for i in range(0, 48)], 0, 0, None),
       # command("WD 000 Test&00", 0, 0, None, 0, 0, None),

        #command("PV 01 ", 0, 0, [" %03i" % i for i in range(1, 91)], 0, 0, None),

        #command("PC SY 718 2", 0, 0, None, 0, 0, None),
        #command("PC SY 718 3", 0, 0, None, 0, 0, None),

        #command("PV P1", 0, 0, ["%03i" % i for i in range(201, 210)], 0, 0, None),
        #command("PV 50", 0, 0, ["%03i" % i for i in range(1, 10)], 0, 0, None)
        ]

full_serial_test_commands = [
	command("EQ", 0, 0, None, 0, 0, None),
]



def formatCommand(commandType, text):
	currentCommand = bytearray()

	if commandType == "Smithcomm Mini Host" or commandType == "AICB":
		lrc = 0

		currentCommand.append(0x02)

		for i in text:
			currentCommand.append(ord(i))
			lrc = lrc ^ ord(i)
		currentCommand.append(0x03)
		lrc = lrc ^ 0x03
		currentCommand.append(lrc)
		if commandType == "AICB":
			currentCommand.append(0x7F)

	elif commandType == "Smithcomm Term Host":
		currentCommand.append('*')

		for i in text:
			currentCommand.append(ord(i))

		currentCommand.append(0x0d)
		currentCommand.append(0x0a)
		
	elif commandType == "Modbus":
                currentCommand.extend(text.decode("hex"))
	elif commandType == "Titan":
		print "Titan"
	elif commandType == "Mini/Blend Pack":
		print "Blend"
	elif commandType == "Terminal \\r\\n":

		if "ctrl+" in text.lower():
			control = ord(str(text)[5]) - 0x40
			if control >= 0 and control <= 31:
				currentCommand.append(control)
				currentCommand.append(0x0d)
				currentCommand.append(0x0a)
		else:
			for i in text:
				currentCommand.append(ord(i))
			currentCommand.append(0x0d)
			currentCommand.append(0x0a)

	elif commandType == "Terminal \\n":

		if "ctrl+" in self.command_line.text().lower():
			control = ord(str(text)[5]) - 0x40
			if control >= 0 and control <= 31:
				currentCommand.append(control)
				currentCommand.append(0x0a)

		else:
			for i in text:
				currentCommand.append(ord(i))
			currentCommand.append(0x0a)

	return currentCommand


class FormatTest(QThread):
	updateText = Signal(bytearray, str, int)
        updateStatusText = Signal(str)
        testStopTest = Signal()
        
	def __init__(self, args = None):
		super(FormatTest, self).__init__()
		self.stopFlag = False
		self.responseStatus = 0
		self.currentResponse = bytearray()
		self.totalLoops = 0
		self.startTest = False
		self.sendCommand = ""
		self.minArms = 0
		self.maxArms = 0

		if args is not None:
			self.port = args[0]
			self.protocol = args[1]
			self.serialConn = args[2]
			self.currentTCP = args[3]

                #Create the GUI
		self.window = QWidget()
                self.window.resize(250, 150)
                self.window.setWindowTitle("Full Command Test")
                self.test_verticalLayout = QVBoxLayout(self.window)
                self.test_verticalLayout.setObjectName("test_verticalLayout")

                self.test_command_chooser_label = QLabel(self.window)
                self.test_command_chooser_label.setObjectName("test_command_chooser_label")
                self.test_command_chooser_label.setText("Choose Commad(s)")
                self.test_verticalLayout.addWidget(self.test_command_chooser_label)
                
                self.test_command_chooser = QComboBox(self.window)
                self.test_command_chooser.addItem("All Commands")
                self.test_verticalLayout.addWidget(self.test_command_chooser)

                #Add All of the Available Commands
                self.test_command_chooser.addItems([i.getCommandHeader() for i in full_command_test_commands])

                self.test_arm_chooser_label = QLabel(self.window)
                self.test_arm_chooser_label.setObjectName("test_arm_chooser_label")
                self.test_arm_chooser_label.setText("Arms Range")
                self.test_verticalLayout.addWidget(self.test_arm_chooser_label)

                self.test_arm_min_chooser_edit = QLineEdit(self.window)
                self.test_arm_min_chooser_edit.setObjectName("test_arm_min_chooser_edit")
                self.test_verticalLayout.addWidget(self.test_arm_min_chooser_edit)

                self.test_arm_max_chooser_edit = QLineEdit(self.window)
                self.test_arm_max_chooser_edit.setObjectName("test_arm_max_chooser_edit")
                self.test_verticalLayout.addWidget(self.test_arm_max_chooser_edit)

                self.test_number_loops_label = QLabel(self.window)
                self.test_number_loops_label.setObjectName("test_number_loops_label")
                self.test_number_loops_label.setText("Number of Loops")
                self.test_verticalLayout.addWidget(self.test_number_loops_label)

                self.test_number_loops = QLineEdit(self.window)
                self.test_number_loops.setObjectName("test_number_loops")
                self.test_verticalLayout.addWidget(self.test_number_loops)

                self.status_label = QLabel(self.window)
                self.status_label.setObjectName("status_label")
                self.status_label.setText("Ready")
                self.updateStatusText.connect(self.status_label.setText)
                self.test_verticalLayout.addWidget(self.status_label)
               
                self.test_start_button = QPushButton(self.window)
                self.test_start_button.setText("Start")
                self.test_start_button.pressed.connect(self.buttonPressed)
                self.test_verticalLayout.addWidget(self.test_start_button)

                self.window.show()

	def stop(self):
		print "Stopping"
		self.stopFlag = True
	
	def stopped(self):
		return self.stopFlag

	def running(self):
		return self.isRunning
	
	def buttonPressed(self):
                #Get the Commands that We Want to Send
                self.sendCommand = str(self.test_command_chooser.currentText())
                self.minArms = int(self.test_arm_min_chooser_edit.text())
                self.maxArms = int(self.test_arm_max_chooser_edit.text()) + 1
                self.totalLoops = int(self.test_number_loops.text())
                
                print "Starting Test"
                self.startTest = True
	
	def setResponse(self, response):
		self.currentResponse = response
		self.responseStatus = True

	def run(self):
                self.updateStatusText.emit("Ready")
		self.isRunning = True

                #Wait for the In Test Start Button
                while not self.startTest:
                        time.sleep(1)
  			if self.stopFlag:
		                self.isRunning = False
		                print "Exiting"
		                return	

                self.updateStatusText.emit("Running")
                for loops in range(0, self.totalLoops):        
                        for arm in range(self.minArms, self.maxArms):
                                for i in full_command_test_commands:
                                        if self.sendCommand != "All Commands":
                                                if self.sendCommand != i.getCommandHeader():
                                                        continue
                                                
                                        for j in i.getAllCommands():
                                                command = "%02i%s" % (arm,j)
                                                byteCommand = formatCommand(self.protocol ,command)
                                                self.updateText.emit(byteCommand, command + "\n", len(byteCommand))
                                                if(self.serialConn.isChecked()):
                                                        self.port.write(byteCommand)
                                                        startTime = time.time()
                                                else:
                                                        self.currentTCP.sendall(byteCommand)
                                                        startTime = time.time()
                                                if self.stopFlag:
                                                        self.isRunning = False
                                                        print "Exiting"
                                                        return	

                                                retries = 0
                                                while 1:
                                                        if self.stopFlag:
                                                                self.updateStatusText.emit("Done")
                                                                self.isRunning = False
                                                                print "Exiting"
                                                                return	

                                                        time.sleep(0.1)
                                                        if self.responseStatus == 1:
                                                                self.responseStatus = 0
                                                                break
                                                        else:
                                                                if retries <= 10:
                                                                        retries += 1
                                                                else:
                                                                        print "Timeout"
                                                                        self.responseStatus = 0
                                                                        retires = 0
                                                                        break

                self.updateStatusText.emit("Done")
                print "Stopping Test"
                self.isRunning = False
                self.testStopTest.emit()

		return


class FullCommandTest(QThread):
	updateText = Signal(bytearray, str, int)
        updateStatusText = Signal(str)
        updateMinText = Signal(str)
        updateMaxText = Signal(str)
        updateAvgText = Signal(str)
	updateCountText = Signal(str)
        testStopTest = Signal()
        
	def __init__(self, args = None):
		super(FullCommandTest, self).__init__()
		self.stopFlag = False
		self.responseStatus = 0
		self.currentResponse = bytearray()
		self.averageTime = 0
		self.minTime = 0xFFFFFFFF
		self.maxTime = 0
		self.numLoops = 0
		self.totalLoops = 0
		self.startTest = False
		self.sendCommand = ""
		self.minArms = 0
		self.maxArms = 0

		if args is not None:
			self.port = args[0]
			self.protocol = args[1]
			self.serialConn = args[2]
			self.currentTCP = args[3]

                #Create the GUI
		self.window = QWidget()
                self.window.resize(250, 150)
                self.window.setWindowTitle("Full Command Test")
                self.test_verticalLayout = QVBoxLayout(self.window)
                self.test_verticalLayout.setObjectName("test_verticalLayout")

                self.test_command_chooser_label = QLabel(self.window)
                self.test_command_chooser_label.setObjectName("test_command_chooser_label")
                self.test_command_chooser_label.setText("Choose Commad(s)")
                self.test_verticalLayout.addWidget(self.test_command_chooser_label)
                
                self.test_command_chooser = QComboBox(self.window)
                self.test_command_chooser.addItem("All Commands")
                self.test_verticalLayout.addWidget(self.test_command_chooser)

                #Add All of the Available Commands
                self.test_command_chooser.addItems([i.getCommandHeader() for i in full_command_test_commands])

                self.test_arm_chooser_label = QLabel(self.window)
                self.test_arm_chooser_label.setObjectName("test_arm_chooser_label")
                self.test_arm_chooser_label.setText("Arms Range")
                self.test_verticalLayout.addWidget(self.test_arm_chooser_label)

                self.test_arm_min_chooser_edit = QLineEdit(self.window)
                self.test_arm_min_chooser_edit.setObjectName("test_arm_min_chooser_edit")
                self.test_verticalLayout.addWidget(self.test_arm_min_chooser_edit)

                self.test_arm_max_chooser_edit = QLineEdit(self.window)
                self.test_arm_max_chooser_edit.setObjectName("test_arm_max_chooser_edit")
                self.test_verticalLayout.addWidget(self.test_arm_max_chooser_edit)

                self.test_number_loops_label = QLabel(self.window)
                self.test_number_loops_label.setObjectName("test_number_loops_label")
                self.test_number_loops_label.setText("Number of Loops")
                self.test_verticalLayout.addWidget(self.test_number_loops_label)

                self.test_number_loops = QLineEdit(self.window)
                self.test_number_loops.setObjectName("test_number_loops")
                self.test_verticalLayout.addWidget(self.test_number_loops)

                self.status_label = QLabel(self.window)
                self.status_label.setObjectName("status_label")
                self.status_label.setText("Ready")
                self.updateStatusText.connect(self.status_label.setText)
                self.test_verticalLayout.addWidget(self.status_label)
               
                self.test_avg_label = QLabel(self.window)
                self.test_avg_label.setObjectName("test_avg_label")
                self.test_avg_label.setText("Average Time")
                self.test_verticalLayout.addWidget(self.test_avg_label)

                self.test_avg_label_val = QLabel(self.window)
                self.test_avg_label_val.setObjectName("test_avg_label_val")
                self.test_avg_label_val.setText("0")
                self.updateAvgText.connect(self.test_avg_label_val.setText)
                self.test_verticalLayout.addWidget(self.test_avg_label_val)

                self.test_max_label = QLabel(self.window)
                self.test_max_label.setObjectName("test_max_label_val")
                self.test_max_label.setText("Maximum Time")
                self.test_verticalLayout.addWidget(self.test_max_label)
                
                self.test_max_label_val = QLabel(self.window)
                self.test_max_label_val.setObjectName("label")
                self.test_max_label_val.setText("0")
                self.updateMaxText.connect(self.test_max_label_val.setText)
                self.test_verticalLayout.addWidget(self.test_max_label_val)
                
                self.test_min_label = QLabel(self.window)
                self.test_min_label.setObjectName("test_min_label")
                self.test_min_label.setText("Minimum Time")
                self.test_verticalLayout.addWidget(self.test_min_label)

                self.test_min_label_val = QLabel(self.window)
                self.test_min_label_val.setObjectName("test_min_label_val")
                self.test_min_label_val.setText("0")
                self.updateMinText.connect(self.test_min_label_val.setText)
                self.test_verticalLayout.addWidget(self.test_min_label_val)

                self.test_count_label = QLabel(self.window)
                self.test_count_label.setObjectName("test_count_label")
                self.test_count_label.setText("Count")
                self.test_verticalLayout.addWidget(self.test_count_label)

                self.test_count_label_val = QLabel(self.window)
                self.test_count_label_val.setObjectName("test_count_label_val")
                self.test_count_label_val.setText("0")
                self.updateCountText.connect(self.test_count_label_val.setText)
                self.test_verticalLayout.addWidget(self.test_count_label_val)

                self.test_start_button = QPushButton(self.window)
                self.test_start_button.setText("Start")
                self.test_start_button.pressed.connect(self.buttonPressed)
                self.test_verticalLayout.addWidget(self.test_start_button)

                self.window.show()

	def stop(self):
		self.window.close()
		self.stopFlag = True
	
	def stopped(self):
		return self.stopFlag

	def running(self):
		return self.isRunning
	
	def buttonPressed(self):
                #Get the Commands that We Want to Send
                self.sendCommand = str(self.test_command_chooser.currentText())
                self.minArms = int(self.test_arm_min_chooser_edit.text())
                self.maxArms = int(self.test_arm_max_chooser_edit.text()) + 1
                self.totalLoops = int(self.test_number_loops.text())
                
                print "Starting Test"
                self.startTest = True
	
	def setResponse(self, response):
		self.currentResponse = response
		self.responseStatus = True

	def run(self):
                self.updateStatusText.emit("Running Test")

                #Wait for the In Test Start Button
                while not self.startTest:
                        time.sleep(1)
                        if self.stopFlag:
                                self.updateStatusText.emit("Done")
                                self.isRunning = False
                                self.testStopTest.emit()
				return

                self.updateStatusText.emit("Running")
                for loops in range(0, self.totalLoops):        
                        for arm in range(self.minArms, self.maxArms):
                                for i in full_command_test_commands:
                                        if self.sendCommand != "All Commands":
                                                if self.sendCommand != i.getCommandHeader():
                                                        continue
                                                
                                        for j in i.getAllCommands():
                                                command = "%02i%s" % (arm,j)
                                                byteCommand = formatCommand(self.protocol ,command)
                                                self.updateText.emit(byteCommand, command + "\n", len(byteCommand))
                                                if(self.serialConn.isChecked()):
                                                        self.port.write(byteCommand)
                                                        startTime = time.time()
                                                else:
                                                        self.currentTCP.sendall(byteCommand)
                                                        startTime = time.time()
                                                if self.stopFlag:
                                                        self.isRunning = False
                                                        self.testStopTest.emit()
                                                        print "Exiting"
                                                        return	

                                                retries = 0
                                                while 1:
                                                        if self.stopFlag:
                                                                self.updateStatusText.emit("Done")
                                                                if self.numLoops > 0:
                                                                        self.updateAvgText.emit(str(self.averageTime / self.numLoops))
                                                                        self.updateMinText.emit(str(self.minTime))
                                                                        self.updateMaxText.emit(str(self.maxTime))
									self.updateCountText.emit(str(self.numLoops))

                                                                self.isRunning = False
                                                                self.testStopTest.emit()
                                                                print "Exiting"
                                                                return	

                                                        time.sleep(0.001)
                                                        if self.responseStatus == 1:
                                                                duration = time.time() - startTime

                                                                if (duration < self.minTime) and (duration > 0):
                                                                        self.minTime = duration
                                                                        print "Minimum Time " + str(duration)
                                                                        self.updateMinText.emit(str(self.minTime))
                                                                if (duration > self.maxTime) and (duration > 0):
                                                                        self.maxTime = duration
                                                                        self.updateMaxText.emit(str(self.maxTime))
                                                                        print "Maximum Time " + str(duration)

                                                                self.averageTime += duration
                                                                self.numLoops += 1
								self.updateCountText.emit(str(self.numLoops))
                                                                if self.numLoops % 10:
                                                                        self.updateAvgText.emit(str(self.averageTime / self.numLoops))
                                                                self.responseStatus = 0
                                                                break
                                                        else:
                                                                if retries <= 500:
                                                                        retries += 1
                                                                else:
                                                                        print "Timeout"
                                                                        self.responseStatus = 0
                                                                        retires = 0
                                                                        break

                self.updateAvgText.emit(str(self.averageTime / self.numLoops))
                self.updateMinText.emit(str(self.minTime))
                self.updateMaxText.emit(str(self.maxTime))
                self.updateStatusText.emit("Done")
                print "Stopping Test"
                self.isRunning = False
                self.testStopTest.emit()

		return

class BackwardsCompatability(QThread):
	updateText = Signal(bytearray, str, int)
        updateStatusText = Signal(str)
        testStopTest = Signal()

	def __init__(self, args = None):
		super(BackwardsCompatability, self).__init__()
		self.stopFlag = False
		self.responseStatus = 0
		self.currentResponse = bytearray()
		self.averageTime = 0
		self.minTime = 0xFFFFFFFF
		self.maxTime = 0
		self.numLoops = 0
		self.totalLoops = 0
		self.startTest = False
		self.sendCommand = ""
		self.secondTCP = None

		if args is not None:
			self.port = args[0]
			self.protocol = args[1]
			self.serialConn = args[2]
			self.currentTCP = args[3]

                #Create the GUI
		self.backwardscompatability_window = QWidget()
                self.backwardscompatability_window.resize(250, 150)
                self.backwardscompatability_window.setWindowTitle("Full Command Test")
                self.backwardscompatability_verticalLayout = QVBoxLayout(self.backwardscompatability_window)
                self.backwardscompatability_verticalLayout.setObjectName("backwardscompatability_verticalLayout")

                self.backwardscompatability_gridlayout = QGridLayout(self.backwardscompatability_window)
                self.backwardscompatability_gridlayout.setObjectName("backwardscompatability_gridLayout")

                self.backwardscompatability_connection_label = QLabel(self.backwardscompatability_window)
                self.backwardscompatability_connection_label.setObjectName("backwardscompatability_connection_label")
                self.backwardscompatability_connection_label.setText("Second Connection")
                self.backwardscompatability_verticalLayout.addWidget(self.backwardscompatability_connection_label)

                self.backwardscompatability_serial_radio = QRadioButton()
                self.backwardscompatability_serial_radio.setObjectName("backwardscompatability_serial_radio")
                self.backwardscompatability_gridlayout.addWidget(self.backwardscompatability_serial_radio, 0, 0, 1, 1)
                
                self.backwardscompatability_tcp_radio = QRadioButton()
                self.backwardscompatability_tcp_radio.setChecked(True)
                self.backwardscompatability_tcp_radio.setObjectName("backwardscompatability_tcp_radio")
                self.backwardscompatability_gridlayout.addWidget(self.backwardscompatability_tcp_radio, 0, 1, 1, 1)

                self.backwardscompatability_serial_radio.setText("Serial")
                self.backwardscompatability_tcp_radio.setText("TCP")

                self.backwardscompatability_ip_line = QLineEdit()
                self.backwardscompatability_ip_line.setObjectName("backwardscompatability_ip_line")
                self.backwardscompatability_gridlayout.addWidget(self.backwardscompatability_ip_line, 1, 0, 3, 3)

                self.backwardscompatability_verticalLayout.addLayout(self.backwardscompatability_gridlayout)

                self.backwardscompatability_chooser_label = QLabel(self.backwardscompatability_window)
                self.backwardscompatability_chooser_label.setObjectName("backwardscompatability_chooser_label")
                self.backwardscompatability_chooser_label.setText("Errors")
                self.backwardscompatability_verticalLayout.addWidget(self.backwardscompatability_chooser_label)

                self.backwardscompatability_status_label = QLabel(self.backwardscompatability_window)
                self.backwardscompatability_status_label.setObjectName("backwardscompatability_status_label")
                self.backwardscompatability_status_label.setText("Ready")
                self.updateStatusText.connect(self.backwardscompatability_status_label.setText)
                self.backwardscompatability_verticalLayout.addWidget(self.backwardscompatability_status_label)

                self.backwardscompatability_start_button = QPushButton(self.backwardscompatability_window)
                self.backwardscompatability_start_button.setText("Start")
                self.backwardscompatability_start_button.pressed.connect(self.buttonPressed)
                self.backwardscompatability_verticalLayout.addWidget(self.backwardscompatability_start_button)

                self.backwardscompatability_window.show()

	def stop(self):
		self.backwardscompatability_window.close()
		self.stopFlag = True
	
	def stopped(self):
		return self.stopFlag

	def running(self):
		return self.isRunning
	
	def buttonPressed(self):               
                print "Starting Test"
                self.startTest = True
                text = ""
                
                #Connect to the Second IP Address
                text = str(self.backwardscompatability_ip_line.text())
                if not text:
                        return

                if ":" in text:
                        pos = text.find(':')
                        if pos > len(text):
                                return

                        port = int(text[pos + 1:])
                else:
                        return

                self.secondTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip_addr = socket.gethostbyname(text[:pos])
                print "Connecting to " + ip_addr + " On Port " + str(port)
                
                try:
                        self.secondTCP.settimeout(1)
                        self.secondTCP.connect((ip_addr, port))
                except socket.error as msg:
                        self.secondTCP.close()
                        return
                
	def setResponse(self, response):
		self.currentResponse = response
		self.responseStatus = True

	def run(self):
                #Wait for the In Test Start Button
                while not self.startTest:
                        time.sleep(1)
                        if self.stopFlag:
                                self.updateStatusText.emit("Done")
                                self.isRunning = False
                                self.testStopTest.emit()
				return

                self.updateStatusText.emit("Running")
                for arm in range(1, 2):
                        for i in backwards_compatability_test_commands:          
                                for j in i.getAllCommands():
                                        command = "%02i%s" % (arm,j)
                                        byteCommand = formatCommand(self.protocol, command)
                                        self.updateText.emit(byteCommand, command + "\n", len(byteCommand))
                                        
                                        #Send to the First AccuLoad IV
                                        self.currentTCP.sendall(byteCommand)
                                        
                                        if self.stopFlag:
                                                self.isRunning = False
                                                self.testStopTest.emit()
                                                print "Exiting"
                                                return	

                                        retries = 0
                                        while 1:
                                                if self.stopFlag:
                                                        self.updateStatusText.emit("Done")

                                                        self.isRunning = False
                                                        self.testStopTest.emit()
                                                        print "Exiting"
                                                        return	

                                                time.sleep(0.001)
                                                if self.responseStatus == 1:
                                                        self.responseStatus = 0
                                                        break
                                                else:
                                                        if retries <= 500:
                                                                retries += 1
                                                        else:
                                                                print "Timeout"
                                                                self.responseStatus = 0
                                                                retires = 0
                                                                break

                self.updateStatusText.emit("Done")
                print "Stopping Test"
                self.isRunning = False
                self.testStopTest.emit()

                return

smith_test = {
	"Full Format Test" : FormatTest,
	"Backwards Compatability" : BackwardsCompatability,
	"Full Command Test" : FullCommandTest
}
