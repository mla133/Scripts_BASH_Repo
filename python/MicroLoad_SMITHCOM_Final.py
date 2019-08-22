while(1):

    #importing PyQt5 to connect to GUI
    from PyQt5 import QtWidgets, uic

    #importing sys to include certain variables and functions
    import sys

    #importing socket library to setup initial TCP connection to MicroLoad
    import socket
    ################################################################################
    import visa #National Instruments ni-visa library

    import time

    #declaring IP of the DMM to setup TCP connection
    VISA_ADDRESS = 'TCPIP0::192.168.181.173::INSTR'
    
    try:
        # Create a connection (session) to the TCP/IP socket on the instrument.
        resourceManager = visa.ResourceManager()
        session = resourceManager.open_resource(VISA_ADDRESS)

        # For Serial and TCP/IP socket connections enable the read Termination 
        # Character or reads will timeout
        if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
            session.read_termination = '\n'
    

    except visa.Error as ex:
        print('An error occurred: %s' % ex)

        print('Done.')
    
    
    
    #declaring IP of the MicroLoad
    MicroLoad = '192.168.0.1'
    #setting up the port for SmithCOM
    MLport = 7734
    #declaring buffer size
    BUFF_SIZE = 1024
    #setting up a socket to connect via ethernet
    ML_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Telling the socket to timeout after 1 second if no connection
    ML_socket.settimeout(1)
    
    SocketConnectedFlag = False

    #setting up the initial connection between the code and GUI  
    class Ui(QtWidgets.QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            uic.loadUi('MicroLoad.ui', self)
            
            #connecting the retrieve lower resistance button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'retrieve_lower_resistance')
            self.button.clicked.connect(self.retrieve_lower_resistancePressed)
            
            #connecting the retrieve lower A/D count button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'retrieve_lower_AD')
            self.button.clicked.connect(self.retrieve_lower_ADPressed)
             
            #connecting the retrieve upper resistance button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'retrieve_upper_resistance')
            self.button.clicked.connect(self.retrieve_upper_resistancePressed)
        
            #connecting the retrieve upper A/D count button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'retrieve_upper_AD')
            self.button.clicked.connect(self.retrieve_upper_ADPressed)
        
            #connecting the first calculate button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'calculate_calibration')
            self.button.clicked.connect(self.calculate_calibrationPressed)
        
            #connecting the third enter retrieve button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'enter_retrieve_3')
            self.button.clicked.connect(self.enter_retrieve_3Pressed)
        
            #connecting the fourth enter retrieve button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'enter_retrieve_4')
            self.button.clicked.connect(self.enter_retrieve_4Pressed)
        
            #connecting the first calculate button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'calculate_calibration_2')
            self.button.clicked.connect(self.calculate_calibration_2Pressed)
        
            #connecting the connect button bewteen python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'setup_connection')
            self.button.clicked.connect(self.setup_connectionPressed)
        
           #connecting the MicroLoad IP address button between python script and GUI
            self.button = self.findChild(QtWidgets.QPushButton, 'ip_addr_button')
            self.button.clicked.connect(self.ip_addr_buttonPressed)
            
            #setting the IP textbox in the GUI to specific MicroLoad IP address
            self.ip_addr.setText(MicroLoad)      
            
            #connecting the DMM IP address button between python script and GUI
            #self.button = self.findChild(QtWidgets.QPushButton, 'ip_addr_button_2')
            #self.button.clicked.connect(self.ip_addr_button_2Pressed)
        
            self.show()

        #function defining what to do when ip_addr button is pressed
        def ip_addr_buttonPressed(self):
            
            #declaring Microload as a global variable, allowing initial value to be used
            global MicroLoad
            #printing the Microloads IP
            print(self.ip_addr.text())
            #setting the new variable ip_adr to the IP entered through the GUI
            ip_adr = str(self.ip_addr.text())
            #setting the MicroLoad variable to the new user entered IP
            MicroLoad = ip_adr
            print(MicroLoad)
            
        #function defining what to do when the setup_connection button is pressed   
        def setup_connectionPressed(self):
        
            global SocketConnectedFlag
            global ML_socket
            
            ML_socket.close()
            
            if SocketConnectedFlag == False:   
                ML_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #Telling the socket to timeout after 1 second if no connection 
                ML_socket.settimeout(1)
                
                ML_socket.connect((MicroLoad, MLport))
                print("======> Connection to MicroLoad is Successful <=====")
                self.setup_connection.setStyleSheet('background-color: green')
                self.setup_connection.setText('Connected')
                self.status.setText('Device Connected')
                SocketConnectedFlag = True
                
            else: 
                print("Closed Connection to MicroLoad")
                self.setup_connection.setStyleSheet('background-color: red')
                self.setup_connection.setText('Disconnected')
                self.status.setText('Device Disconnected')
                ML_socket.close()
                SocketConnectedFlag = False
                  
        def retrieve_lower_resistancePressed(self):
            FOURWIRERTD = True
             
            if FOURWIRERTD:
                session.write('MEAS:FRES?') # <-- SCPI call
                measurement = session.read()
                (RTD_measurement) = '%s'%float(measurement.rstrip('n'))
                print(RTD_measurement)
                RTD_MEASUREMENT = RTD_measurement[:6]
                print(RTD_MEASUREMENT)
                
                self.lower_resistance.setText(RTD_MEASUREMENT)
                
                
        def retrieve_lower_ADPressed(self):
        
            ML_socket.sendall(b'*17ZX 1 \r\n')
            data = ML_socket.recv(BUFF_SIZE)
            data = str(data.decode('ascii'))
            print(data)
            DATA = data[7:]
            print(DATA)
        
            self.lower_AD.setText(str(DATA)) 
        
        def retrieve_upper_resistancePressed(self):
            FOURWIRERTD = True
            
            if FOURWIRERTD:
                session.write('MEAS:FRES?') # <-- SCPI call
                measurement = session.read()
                (RTD_measurement) = '%s'%float(measurement.rstrip('n'))
                print(RTD_measurement)
                RTD_MEASUREMENT = RTD_measurement[:7]
                print(RTD_MEASUREMENT)
                
                self.upper_resistance.setText(RTD_MEASUREMENT)
            
       
        def retrieve_upper_ADPressed(self):
        
            ML_socket.sendall(b'*17ZX 1 \r\n')
            data = ML_socket.recv(BUFF_SIZE)
            data = str(data.decode('ascii'))
            DATA = data[7:]
            print(DATA)
            self.upper_AD.setText(str(DATA))
            self.status.setText('Retrieved & Entered')

        
        def calculate_calibrationPressed(self):
            user1 =float(self.lower_resistance.text())
            user2 =float(self.upper_resistance.text())
            AD1 = int(self.lower_AD.text())
            AD2 = int(self.upper_AD.text())
            y_int =(1048576.0/500)*((user2 - (AD2*(user2 - user1)/(AD2-AD1))))
            slope = (1048576.0/500)*((user2-user1)/(AD2-AD1))
            CAL1 = ((slope*(131072)) + (y_int))
            CAL2 = ((slope*(917504)) + (y_int))
        
            self.cal1_value.setText(str(int(round(CAL1,0))))
            
            self.cal2_value.setText(str(int(round(CAL2,0))))
            self.slope.setText(str(round(slope,4)))
            self.y_int.setText(str(round(y_int,2)))
            
            
            if 133695>CAL1 and CAL1>128450 and 935853>CAL2 and CAL2>899153:
                print("Calibration Values are valid!")
                self.cal1_value.setStyleSheet('background-color: green')
                self.cal2_value.setStyleSheet('background-color: green')
                
            else:
                self.cal1_value.setStyleSheet('background-color: red')
                self.cal2_value.setStyleSheet('background-color: red')
            
            
            msg1 = "*17ZY 1 " + "0" +str(int(round(CAL1,0))) + "\r\n"
            try:
                msg1 = msg1.encode('ascii')
                ML_socket.send(msg1)
            except socket.timeout:
                print("***ERROR***")
            
            ML_socket.recv(BUFF_SIZE)
        
            msg2 = "*17ZZ 1 " + "0" + str(int(round(CAL2,0))) + "\r\n"
            try:
                msg2 = msg2.encode('ascii')
                ML_socket.send(msg2)
            except socket.timeout:
                print("***ERROR***")
            
            ML_socket.recv(BUFF_SIZE)
            
            self.status.setText('RTD CAL Complete')
            
        
        def enter_retrieve_3Pressed(self):
            DCCURRENT = True
            
            time.sleep(4)
            
            if DCCURRENT:
                session.write('MEAS:CURR:DC?') # <-- SCPI call
                measurement = session.read()
                # remember that 'measurement' is a string, must cast it to float
                # to print the decimal value instead of exponential notation.
                current_measurement = ('%s' % (1000*float(measurement.rstrip('\n'))))
                print(current_measurement)
                CURRENT_MEASUREMENT =current_measurement[:5]
                print(CURRENT_MEASUREMENT)
                self.lower_current.setText(CURRENT_MEASUREMENT)
                
        
            ML_socket.sendall(b'*17ZX 2 \r\n')
            data = ML_socket.recv(BUFF_SIZE)
            data = str(data.decode('ascii'))
            DATA = data[7:]
            print(DATA)
            
            
            self.lower_AD_count.setText(str(DATA))
            self.status.setText('Retrieved & Entered')
            
            
        def enter_retrieve_4Pressed(self):
            DCCURRENT = True
            
            time.sleep(4)
            if DCCURRENT:
                session.write('MEAS:CURR:DC?') # <-- SCPI call
                measurement = session.read()
                # remember that 'measurement' is a string, must cast it to float
                # to print the decimal value instead of exponential notation.
                current_measurement = ('%s' % (1000*float(measurement.rstrip('\n'))))
                print(current_measurement)
                CURRENT_MEASUREMENT =current_measurement[:6]
                print(CURRENT_MEASUREMENT)
                self.upper_current.setText(CURRENT_MEASUREMENT)
        
            ML_socket.sendall(b'*17ZX 2 \r\n')
            data = ML_socket.recv(BUFF_SIZE)
            data = str(data.decode('ascii'))
            DATA = data[7:]
            print(DATA)
            self.upper_AD_count.setText(str(DATA))
            self.status.setText('Retrieved & Entered')
        
        def calculate_calibration_2Pressed(self):
            user3 =float(self.lower_current.text())
            user4 =float(self.upper_current.text())
            AD3 = int(self.lower_AD_count.text())
            AD4 = int(self.upper_AD_count.text())
            y_int1 =(1048576.0/25.0)*((user4 - (AD4*(user4 - user3)/(AD4-AD3))))
            slope1 =(1048576.0/25.0)*((user4-user3)/(AD4-AD3))
            CAL3 =((slope1*(131072)) + (y_int1))
            CAL4 =((slope1*(917504)) + (y_int1))
            
        
            self.cal1_value_2.setText(str(int(round(CAL3,0))))
            self.cal2_value_2.setText(str(int(round(CAL4,0))))
            self.slope_2.setText(str(round(slope1,4)))
            self.y_int_2.setText(str(round(y_int1,2)))
            
            if 131300>CAL3 and CAL3>130800 and 919300>CAL4 and CAL4>915700:
                print("Calibration Values are valid!")
                self.cal1_value_2.setStyleSheet('background-color: green')
                self.cal2_value_2.setStyleSheet('background-color: green')
                
            else:
                self.cal1_value_2.setStyleSheet('background-color: red')
                self.cal2_value_2.setStyleSheet('background-color: red')
        
        
            msg3 = "*17ZY 2 " + "0" +str(int(round(CAL3,0))) + "\r\n"
            try:
                msg3 = msg3.encode('ascii')
                ML_socket.send(msg3)
            except socket.timeout:
                print("***ERROR***")
                
            ML_socket.recv(BUFF_SIZE)
            
            msg4 = "*17ZZ 2 " + "0" + str(int(round(CAL4,0))) + "\r\n"
            try:
                msg4 = msg4.encode('ascii')
                ML_socket.send(msg4)
            except socket.timeout:
                print("***ERROR***")
                
            ML_socket.recv(BUFF_SIZE)
                
            self.status.setText('4-20 CAL Complete')
                    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

    ML_socket.close()
    session.close()
    resourceManager.close()