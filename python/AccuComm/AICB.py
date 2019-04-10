import sys
import os
import serial
import time
import glob
import socket
import commands

from PySide.QtGui import *
from PySide.QtCore import *

aicb_commands = {

}

class InjectorClass(object):
	def __init__(self, window):
		self.label = QLabel(window)
		self.countsEdit = QLineEdit(window)
		self.volumeEdit = QLineEdit(window)
		self.dataButton = QToolButton(window)
		self.dataButton.setText("...")
		self.pumpButton = QPushButton(window)
		self.pumpButton.setText("Pump")
		self.solButton = QPushButton(window)
		self.solButton.setText("Sol")

		self.volume = 0
		self.counts = 0
		self.alarms = 0xFFFF
		self.state = 0
		self.pump = 0
		self.solenoid = 0
		self.revision = 0

	def setRevision(self, revisionNum):
		self.revision = revisionNum

	def requestStatus(self):
		return "ST 0000"

	def requestTotals(self):
		return "TS %5.3f %01X%01X%01X%01X" % (self.volume, (self.alarms >> 24 & ~0x0F), ((self.alarms >> 16) & ~0x0F), ((self.alarms >> 8) & ~0x0F), (self.alarms & ~0x0F))

	def energizePump():
		print ""

	def deEnergizePump(self):
		return "OK"

	def inject():
		print ""

	def clearAlarm(self):
		return "OK"

	def parameterRead():
		print ""

	def parameterWrite(self, parameterNum):
		return "OK"

	def setOutput():
		print ""

	def readOutput():
		print ""

	def resetPulseCount():
		print ""

	def pulseCount():
		print ""

	def initialize():
		self.volume = 0
		self.counts = 0
		self.alarm = 0
		self.state = 0
		self.pump = 0
		self.solenoid = 0
		return "OK"

	def softwareVersion(self):
		return "SV 04 B42F1AFB"

	def authorizeIO():
		print ""

	def readInputs():
		print ""

	def IOHandler():
		print ""

	def executeCommand(self, addr, command):

		if command == "ST":
			return self.requestStatus()
		elif command == "TS":
			return self.requestTotals()
		elif command == "EP": 
			return self.energizePump()
		elif command == "DP": 
			return self.deEnergizePump()
		elif command == "IN": 
			return self.inject()
		elif command == "CA": 
			return self.clearAlarm()
		elif command == "PR": 
			return self.parameterRead()
		elif command == "PW": 
			return self.parameterWrite(10)
		elif command == "SO": 
			return self.setOutput()
		elif command == "OS": 
			return self.readOutput()
		elif command == "RC": 
			return self.resetPulseCount()
		elif command == "PC": 
			return self.pulseCount()
		elif command == "IZ": 
			return self.initialize()
		elif command == "SV": 
			return self.softwareVersion()
		elif command == "AU": 
			return self.authorizeIO()
		elif command == "IO":
			if command[3:4] == "O":
				print "Output"
			else:
				print "Input" 
			return self.IOHandler()

		return ""
	

class AICBEngine(QThread):
	updateText = Signal(bytearray, str, int)
        
	def __init__(self, args = None):
		super(AICBEngine, self).__init__()
		self.stopFlag = False
		self.responseStatus = 0
		self.currentResponse = bytearray()
		self.currentAddress = 100

		self.injectors = []

		if args is not None:
			self.port = args[0]
			self.protocol = args[1]
			self.serialConn = args[2]
			self.currentTCP = args[3]

                #Create the GUI
		self.aicb_window = QWidget()
                self.aicb_window.resize(400, 400)
                self.aicb_window.setWindowTitle("AICB Engine")

		#Settings Layout
		self.aicb_verticalLayout = QVBoxLayout(self.aicb_window)
		self.aicb_verticalLayout.setObjectName("test_verticalLayout")
		self.aicb_horizontalLayout = QHBoxLayout()
 		self.aicb_horizontalLayout.setObjectName("test_horizontalLayout")
                self.aicb_gridLayout = QGridLayout()
                self.aicb_gridLayout.setObjectName("test_gridLayout")

		self.aicb_version_label = QLabel(self.aicb_window)
		self.aicb_version_label.setObjectName("aicb_version_label")
		self.aicb_version_label.setText("Version Number")
		self.aicb_horizontalLayout.addWidget(self.aicb_version_label)

		self.aicb_version_edit = QLineEdit(self.aicb_window)
                self.aicb_version_edit.setObjectName("aicb_version_edit")
                self.aicb_horizontalLayout.addWidget(self.aicb_version_edit)

		self.aicb_address_label = QLabel(self.aicb_window)
		self.aicb_address_label.setObjectName("aicb_address_label")
		self.aicb_address_label.setText("Address Base")
		self.aicb_horizontalLayout.addWidget(self.aicb_address_label)

		self.aicb_address_100 = QRadioButton(self.aicb_window)
		self.aicb_address_100.setObjectName("aicb_address_100")
		self.aicb_address_100.setText("100")
		self.aicb_address_100.setText("100")
		self.aicb_horizontalLayout.addWidget(self.aicb_address_100)

		self.aicb_address_200 = QRadioButton(self.aicb_window)
		self.aicb_address_200.setObjectName("aicb_address_200")
		self.aicb_address_200.setText("200")
		self.aicb_horizontalLayout.addWidget(self.aicb_address_200)

		self.aicb_verticalLayout.addLayout(self.aicb_horizontalLayout)
		self.aicb_verticalLayout.addLayout(self.aicb_gridLayout)

		#Grid Layout Headings
		self.aicb_counts_heading_label = QLabel(self.aicb_window)
		self.aicb_counts_heading_label.setObjectName("aicb_counts_heading_label")
		self.aicb_counts_heading_label.setText("Counts")
		self.aicb_gridLayout.addWidget(self.aicb_counts_heading_label, 0, 1)

		self.aicb_volume_heading_label = QLabel(self.aicb_window)
		self.aicb_volume_heading_label.setObjectName("aicb_volume_heading_label")
		self.aicb_volume_heading_label.setText("Volume")
		self.aicb_gridLayout.addWidget(self.aicb_volume_heading_label, 0, 2)

		for i in range(0,10):
			self.injectors.append(InjectorClass(self.aicb_window))

			if i < 10:
				self.injectors[i].label.setText(str((i + 1) + 100))

				self.aicb_gridLayout.addWidget(self.injectors[i].label, i + 1, 0)
				self.aicb_gridLayout.addWidget(self.injectors[i].countsEdit, i + 1, 1)
				self.aicb_gridLayout.addWidget(self.injectors[i].volumeEdit, i + 1, 2)
				self.aicb_gridLayout.addWidget(self.injectors[i].pumpButton, i + 1, 3)
				self.injectors[i].pumpButton.setStyleSheet("background-color: red")
				self.injectors[i].solButton.setStyleSheet("background-color: red")
				self.aicb_gridLayout.addWidget(self.injectors[i].solButton, i + 1, 4)
				self.aicb_gridLayout.addWidget(self.injectors[i].dataButton, i + 1, 5)

                self.aicb_window.show()

	def stop(self):
		self.stopFlag = True
	
	def stopped(self):
		return self.stopFlag

	def running(self):
		return self.isRunning
	
	def buttonPressed(self):
               "Print Pressed"
	
	def setResponse(self, response):
		self.currentResponse = response
		self.responseStatus = True

	def run(self):
		print "Starting Test"
		retries = 0
		command = ""
                while 1:
                        if self.stopFlag:
                                self.isRunning = False
                                print "Exiting"
                                return	

                        if self.responseStatus == 1:
                                self.responseStatus = 0
				temp_addr = int(self.currentResponse[:3])
				print temp_addr

				if (temp_addr >= self.currentAddress) and (temp_addr <= (self.currentAddress + 10)):
					temp_addr = temp_addr - self.currentAddress
					command = self.currentResponse[:3]
					rtn = self.injectors[temp_addr - 1].executeCommand(temp_addr, self.currentResponse[3:5])
					if len(rtn) > 0:
						command += rtn
						byteCommand = commands.formatCommand("AICB", command)
						self.updateText.emit(byteCommand, command + "\n", len(byteCommand))
						self.port.write(byteCommand)



                        else:
                        	time.sleep(0.001)

                print "Stopping Test"
                self.isRunning = False

		return

