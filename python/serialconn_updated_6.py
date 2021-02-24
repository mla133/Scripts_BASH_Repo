## !\Importing necessary libraries for serial connection and GUI functionality
import serial, sys, time
from PyQt5 import QtWidgets, uic


## !\creating a serial connection for HMIA and setting baudrate
uiconn = serial.Serial()
uiconn.baudrate = 115200
## !\ creating a second serial connection for HMIB and setting baudrate
ui2conn = serial.Serial()
ui2conn.baudrate = 115200

## !\initializing global connection flags and boardset checks to false
flag = False
flag2 = False
boardset1_check = False   
boardset2_check = False
boardset3_check = False
boardset4_check = False

   

## !\creating a class that will connect the script to a GUI
class Ui (QtWidgets.QMainWindow):
    
    ## !\defining all widgets from GUI
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('core_UI.ui', self)
        
        ## !\initializing a button to connect to HMIA
        self.button = self.findChild(QtWidgets.QPushButton, 'ConnectButton')
        self.button.clicked.connect(self.ConnectButtonPressed)
        ## !\iniitializing a button to enter the com port for HMIA
        self.button = self.findChild(QtWidgets.QPushButton, 'disconnectButton')
        self.button.clicked.connect(self.disconnectButtonPressed)
        ## !\initializing a text box to input the com port for HMIA
        self.QLineEdit = self.findChild(QtWidgets.QLineEdit, 'comtext')
        ## !\initializing a button to send configuration commands for HMIA
        self.button = self.findChild(QtWidgets.QPushButton, 'configurebutton')
        self.button.clicked.connect(self.configurebuttonPressed)
        ## !\initializing a radio button to Select HMIA
        self.radiobutton = self.findChild(QtWidgets.QRadioButton, 'HMIA_button')
        self.radiobutton.toggled.connect(self.HMIA_buttonClicked)
        ## !\initializing a radio button to Select HMIB
        self.radiobutton = self.findChild(QtWidgets.QRadioButton, 'HMIB_button')
        self.radiobutton.toggled.connect(self.HMIB_buttonClicked)
        ## !\initializing a button to select boardset one
        self.radiobutton = self.findChild(QtWidgets.QRadioButton, 'OneBoardButton')
        self.radiobutton.toggled.connect(self.OneBoardButtonClicked)
        ## !\initializing a button to select boardset two
        self.radiobutton = self.findChild(QtWidgets.QRadioButton, 'TwoBoardButton')
        self.radiobutton.toggled.connect(self.TwoBoardButtonClicked)
        ## !\initializing a button to select boardset three
        self.radiobutton = self.findChild(QtWidgets.QRadioButton, 'ThreeBoardButton')
        self.radiobutton.toggled.connect(self.ThreeBoardButtonClicked)
        ## !\initializing a button to select boardset four 
        self.radiobutton = self.findChild(QtWidgets.QRadioButton, 'FourBoardButton')
        self.radiobutton.toggled.connect(self.FourBoardButtonClicked)
        ## !\initializing a button to connect to HMIB
        self.button = self.findChild(QtWidgets.QPushButton, 'ConnectButton2')
        self.button.clicked.connect(self.ConnectButton2Pressed)
        ## !\iniitializing a button to enter the com port for HMIB
        self.button = self.findChild(QtWidgets.QPushButton, 'disconnectButton2')
        self.button.clicked.connect(self.disconnectButton2Pressed)
        ## !\initializing a text box to input the com port for HMIB
        self.QLineEdit = self.findChild(QtWidgets.QLineEdit, 'comtext2')
        ## !\initializing a button to send configuration commands for HMIB
        self.button = self.findChild(QtWidgets.QPushButton, 'configurebutton2')
        self.button.clicked.connect(self.configurebutton2Pressed)
        
       
        
        ## !\making the GUI pop up
        self.show                                                                                  
    
        

        ## !\disabling all buttons except HMIA or HMIB button
        self.comtext2.setEnabled(False)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(False)
        self.OneBoardButton.setEnabled(False)
        self.TwoBoardButton.setEnabled(False)
        self.ThreeBoardButton.setEnabled(False)
        self.FourBoardButton.setEnabled(False)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(False)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(False)
        self.ConnectButton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)


    """ @ defining the HMIA button press
        
        disabling all HMIB buttons and enabling all HMIA buttons
        
    """
    def HMIA_buttonClicked(self):
        
        
        ## !\disabling alll HMIB buttons and enabling all HMIA buttons
        self.comtext2.setEnabled(False)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(False)
        self.OneBoardButton.setEnabled(False)
        self.TwoBoardButton.setEnabled(False)
        self.ThreeBoardButton.setEnabled(False)
        self.FourBoardButton.setEnabled(False)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(False)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(True)
        self.ConnectButton.setEnabled(True)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)
        
        # !\settting button to default
        self.connectionstatus2.setStyleSheet('background-color: white')
        # !\setting status text
        self.connectionstatus2.setText('')
        # !\settting button to default
        self.configuretext2.setStyleSheet('background-color: white')
        # !\setting status text to default
        self.configuretext2.setText('')
        self.comtext.setText('')
        
        
        
        
   
    """ @ defining the HMIB button press
        
        disabling all HMIA buttons and enabling buttons to select the number of boards
        
    """     
    def HMIB_buttonClicked(self):
               
        
        #enabling board buttons if dual hmi is selected 
        self.comtext2.setEnabled(False)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(False)
        self.OneBoardButton.setEnabled(True)
        self.TwoBoardButton.setEnabled(True)
        self.ThreeBoardButton.setEnabled(True)
        self.FourBoardButton.setEnabled(True)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(False)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(False)
        self.ConnectButton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)
        
        # !\settting button to default
        self.connectionstatus.setStyleSheet('background-color: white')
        # !\setting status text
        self.connectionstatus.setText('')
        # !\settting button to default
        self.configuretext.setStyleSheet('background-color: white')
        # !\setting status text
        self.configuretext.setText('')
        self.comtext2.setText('')
         
    
    
    """ @ defining the enter COM port button press
        
        taking in the number entered by the user
        adding COM to the front of the number
        assigning the port to the first serial connection
     
    """
    def disconnectButtonPressed(self):
        
        # !\closing serial connection
        uiconn.close()  
        # !\settting button to red
        self.connectionstatus.setStyleSheet('background-color: red')
        # !\setting status text
        self.connectionstatus.setText('Connection Closed')
        # !\setting flag to false
        flag = False
        self.ConnectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.configurebutton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.comtext.setText('')
        self.configuretext.setText('')
        self.configuretext.setStyleSheet('background-color: white')
        
        
        
    """ @ defining the HMIB com port enter button
    
        taking in the number entered by the user
        adding COM to the front of the number
        assigning the port to the first serial connection
        
    """    
    def disconnectButton2Pressed(self):
        # !\closing serial connection
        ui2conn.close()  
        # !\settting button to red
        self.connectionstatus2.setStyleSheet('background-color: red')
        # !\setting status text
        self.connectionstatus2.setText('Connection Closed')
        # !\setting flag to false
        flag = False
        self.ConnectButton2.setEnabled(True)
        self.disconnectButton2.setEnabled(False)
        self.comtext2.setText('')
        self.configuretext2.setText('')
        self.configuretext2.setStyleSheet('background-color: white')
   
    
    
    """ @ defining the One boardset button press
    
        enabling all of the HMIB buttons
        disabling all of the HMIA buttons
        setting global boardset1_check variable to true
        setting other global boardset_check variables to false
    
    """
    def OneBoardButtonClicked(self):
        
        ## !\declaring global checks for the boardset
        global boardset1_check, boardset2_check, boardset3_check, boardset4_check
        
        ## !\setting values for the boardsets to check with
        boardset1_check = True
        boardset2_check = boardset3_check = boardset4_check = False
        
        ## !\enabling all buttons
        self.comtext2.setEnabled(True)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(True)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(True)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(False)
        self.ConnectButton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)
        
    
    
    """ @ defining the Two boardsets button press
    
        enabling all of the HMIB buttons
        disabling all of the HMIA buttons
        setting global boardset2_check variable to true
        setting other global boardset_check variables to false
    
    """
    def TwoBoardButtonClicked(self):
        
        ## !\declaring global checks for the boardset
        global boardset1_check, boardset2_check, boardset3_check, boardset4_check
        
        ## !\setting values for the boardsets to check with
        boardset2_check = True
        boardset1_check = boardset3_check = boardset4_check = False 
        
        ## !\enabling all buttons
        self.comtext2.setEnabled(True)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(True)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(True)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(False)
        self.ConnectButton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)
    
    
    
    
    """ @ defining the Three boardsets button press
    
        enabling all of the HMIB buttons
        disabling all of the HMIA buttons
        setting global boardset3_check variable to true
        setting other global boardset_check variables to false
    
    """
    def ThreeBoardButtonClicked(self):
        
        ## !\globals to check boardset
        global boardset1_check, boardset2_check, boardset3_check, boardset4_check
        
        ## !\setting boardset check values
        boardset3_check = True
        boardset1_check = boardset2_check = boardset4_check = False
        
        ## !\enabling all buttons
        self.comtext2.setEnabled(True)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(True)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(True)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(False)
        self.ConnectButton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)
    
    
    
    
    """ @ defining the four boardsets button press
    
        enabling all of the HMIB buttons
        disabling all of the HMIA buttons
        setting global boardset4_check variable to true
        setting other global boardset_check variables to false
    
    """
    def FourBoardButtonClicked(self):
        
        ## !\globals to use to check boardset
        global boardset1_check, boardset2_check, boardset3_check, boardset4_check
        
        ## !\setting boardset check values
        boardset4_check = True
        boardset1_check = boardset2_check = boardset3_check = False
        
        ## !\enabling all buttons
        self.comtext2.setEnabled(True)
        self.configuretext2.setEnabled(False)
        self.connectionstatus2.setEnabled(True)
        self.disconnectButton2.setEnabled(False)
        self.ConnectButton2.setEnabled(True)
        self.configurebutton2.setEnabled(False)
        self.comtext.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectionstatus.setEnabled(False)
        self.ConnectButton.setEnabled(False)
        self.configuretext.setEnabled(False)
        self.configurebutton.setEnabled(False)
    
    
    
    
    """ @ defining the HMIA connect button pressed
    
        opening the serial connection
        checking if the connection is open and setting the global flag accordingly
        creating a connection timeout
        creating a serial exception
        setting GUI text and color depending on connection status
    
    """
    def ConnectButtonPressed(self):
        
        #setting port number to the text box value
        portnumber = self.comtext.text()
        if portnumber.isnumeric() == True: 
            #giving a value to the port value
            uiconn.port = str('COM') + str(portnumber)
            #print(ui2conn.port)
            #declaring a global flag
            global flag
            
            #try to connect
            try:
                
                #if (flag == False):
                #opening serial connection
                uiconn.open()
                #providing user feedback if connection is successful
                count = 0
                if uiconn.is_open:
                    self.configurebutton.setEnabled(True)
                    self.configuretext.setEnabled(True)
                    
                    #print("Connection Successful")
                    #setting button color to green
                    self.connectionstatus.setStyleSheet('background-color: green')
                    # !\setting status text
                    self.connectionstatus.setText('Connection Successful')
                    # !\assigning username and password values
                    username = "root" +"\r\n"
                    password = "fMcC0R3d1spL4y" + "\r\n"
                    # !\writing username and password to the coreui
                    uiconn.write(username.encode('ascii'))
                    time.sleep(1)
                    for line in uiconn:
                        if("Password" in line.decode()):
                            print("username entered")
                            break
                        else:
                            break
                        print(line.decode())
                    time.sleep(1)
                    uiconn.write(password.encode('ascii'))
                    count = 0
                    for line in uiconn:
                        # !\printing the line from coreui console
                        print(line.decode())
                        # !\providing feedback to user if login incorrect
                        if("Login incorrect" in line.decode()):
                            #print("login failed")
                            #self.connectionstatus.setText('Login Failed')
                            #self.connectionstatus.setStyleSheet('background-color: red')
                            #self.ConnectButton.setEnabled(True)
                            #self.disconnectButton.setEnabled(False)
                            login = False
                            break
                        else:
                            #telling user login successful
                            if("root@display:~#" in line.decode()):
                               #print("login successful")
                               self.connectionstatus.setText('Login Successful')
                               clear = "clear" + "\r\n"
                               uiconn.write(clear.encode('ascii' + '\r\n'))
                               self.ConnectButton.setEnabled(False)
                               self.disconnectButton.setEnabled(True)
                               print(line.decode())
                               login = True
                               break
                            else:
                                # !\telling user login successful
                               if("not found" in line.decode()):
                                   # !\print("already signed in")
                                   self.connectionstatus.setText('Login Successful')
                                   clear = "clear" + "\r\n"
                                   uiconn.write(clear.encode('ascii' + '\r\n'))
                                   self.ConnectButton.setEnabled(False)
                                   self.disconnectButton.setEnabled(True)
                                   print(line.decode())
                                   login = True
                                   break
                               else:
                                   # !\creating a login timeout
                                   if(count > 10):
                                      #print("error")
                                       #self.connectionstatus.setText('Login Timeout (Please try again)')
                                       #self.connectionstatus.setStyleSheet('background-color: red')
                                       #self.ConnectButton.setEnabled(True)
                                       #self.disconnectButton.setEnabled(False)
                                       login = False
                                       break
                        count = count +1
                        print(line.decode())
                        
                    if(login == False):
                        username = "root" +"\r\n"
                        password = "fM(c*R3)1$pL4y" + "\r\n"
                        # !\writing username and password to the coreui
                        uiconn.write(username.encode('ascii'))
                        time.sleep(1)
                        for line in uiconn:
                            if("Password" in line.decode()):
                                print("username entered")
                                break
                            else:
                                break
                            print(line.decode())
                        time.sleep(1)
                        uiconn.write(password.encode('ascii'))
                        count = 0
                        for line in uiconn:
                            # !\printing the line from coreui console
                            print(line.decode())
                            # !\providing feedback to user if login incorrect
                            if("Login incorrect" in line.decode()):
                                #print("login failed")
                                self.connectionstatus.setText('Login Failed')
                                self.connectionstatus.setStyleSheet('background-color: red')
                                self.ConnectButton.setEnabled(True)
                                self.disconnectButton.setEnabled(False)
                                login = False
                                break
                            else:
                                #telling user login successful
                                if("root@display:~#" in line.decode()):
                                   #print("login successful")
                                   self.connectionstatus.setText('Login Successful')
                                   clear = "clear" + "\r\n"
                                   uiconn.write(clear.encode('ascii' + '\r\n'))
                                   self.ConnectButton.setEnabled(False)
                                   self.disconnectButton.setEnabled(True)
                                   print(line.decode())
                                   login = True
                                   break
                                else:
                                    # !\telling user login successful
                                   if("not found" in line.decode()):
                                       # !\print("already signed in")
                                       self.connectionstatus.setText('Login Successful')
                                       clear = "clear" + "\r\n"
                                       uiconn.write(clear.encode('ascii' + '\r\n'))
                                       self.ConnectButton.setEnabled(False)
                                       self.disconnectButton.setEnabled(True)
                                       print(line.decode())
                                       login = True
                                       break
                                   else:
                                       # !\creating a login timeout
                                       if(count > 10):
                                          #print("error")
                                           self.connectionstatus.setText('Login Timeout (Please try again)')
                                           self.connectionstatus.setStyleSheet('background-color: red')
                                           self.ConnectButton.setEnabled(True)
                                           self.disconnectButton.setEnabled(False)
                                           login = False
                                           break
                            count = count +1
                            print(line.decode())
                        
                    # !\setting flag to true
                    flag = True
                    # !\clearing the pyserial input and output buffers
                    uiconn.flushInput()
                    uiconn.flushOutput()
                    # clear = "reset" + "\r\n"
                    time.sleep(.1)
                    # uiconn.write(clear.encode('ascii'))
            # !\allows user to close connection with another button press        
            
                    
                    
            #creating an exception if the connection fails
            except serial.SerialException as se:
                # !\closes connection attempt
                uiconn.close()
                #print(se)
                # !\sets button color to red
                self.connectionstatus.setStyleSheet('background-color: red')
                # !\sets status text
                self.connectionstatus.setText('Connection unsuccessful')
        else:
            self.connectionstatus.setText('Please Enter a Valid COM Port')
            self.connectionstatus.setStyleSheet('background-color: red')
            
            
        
                 
    
    
   
    
    
    
        
    """ @ defining HMIA configure button pressed
    
        sending commands for eth mode, ip, netmask, gateway, and url configuration
        checking if each command is successful
        setting the gui text/color depending on the success of the commands
        
    """    
    def configurebuttonPressed(self):
       
        
        ## !\ initializing variables to check configuration status
        Ethmode_check = False
        IPconfigure_check1 = False
        IPconfigure_check2 = False
        IPconfigure_check3 = False
        IPconfigure_check4 = False
        Netconfigure_check1 = False
        Netconfigure_check2 = False
        Netconfigure_check3 = False
        Netconfigure_check4 = False
        Gateconfigure_check1 = False
        Gateconfigure_check2 = False
        Gateconfigure_check3 = False
        Gateconfigure_check4 = False
        URLconfigure_check = False
        

        #clear = "clear" + "\r\n"
        #uiconn.write(clear.encode('ascii' + "\r\n"))   
############################ Start of Ethernet Mode #########################################################################
        #clear = "clear" + "\r\n"
        #uiconn.write(clear.encode('ascii' + "\r\n"))
        
        """ @ setting the eth mode (dhcp/fixed)
    
            sending command to set eth mode to fixed 
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
        """ 
        # !\ clearing the pyserial input and output buffer
        uiconn.flushInput()
        uiconn.flushOutput()
        
        
        #setting command as ethmode and writing to coreui
        ethmode = "secure-db -u 5 -p 5555 -c writeparam - n db -i 16  -v 1" + "\r\n"
        uiconn.write(ethmode.encode('ascii'))
        time.sleep(.1)
        count = 0
        for line in uiconn:   
            #writing to gui if coreui not ready
            #self.configuretext.setText('Unit not ready, try again')
            #self.configurebutton.setStyleSheet('background-color: yellow')
            #writing to gui if config failed
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('IP Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Ethmode_check = False
                print("eth hash")
                break
            else:
                #writing to gui if config successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('IP Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Ethmode_check = True
                    #print(line.decode())
                    print("eth diff")
                    break
                else:
                    #writing to gui if config successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('IP Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Ethmode_check = True
                        print("eth equal")
                        #print(line.decode())
                        break
                    else:
                        #writing to gui if config failed
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Ethmode_check = False
                            print("eth not found")
                            #print(line.decode())
                            break
                        else:
                            if("No Change" in line.decode()):
                                Ethmode_check = True
                            else:
                                #writing to gui if config failed
                                if(count > 30):
                                    #self.configuretext.setText('Configure Timeout (Please try again)')
                                    #self.configurebutton.setStyleSheet('background-color: yellow')
                                    Ethmode_check = True
                                    print("eth timeout")
                                    break
            #print(line.decode())
            count = count + 1
############################# End of Ethernet Mode Configuration ###########################################################
        """ cd_sqlite = "cd /media/data/var-lib-QtGUI" + "\r\n"
        uiconn.write(cd_sqlite.encode('ascii'))
        
        sqlite = "sqlite3 db.sqlite" + "\r\n"
        uiconn.write(sqlite.encode('ascii'))
        
        ethval = "select ethernet_mode from display_parameters_networking;" + "\r\n"
        uiconn.write(ethval.encode('ascii'))
        for line in uiconn:
            if("1" in line.decode()):
                ethmode_val = True
                break
            else:
                ethmode_val = False
                break
        sqlite_quit = ".quit" + "\r\n"
        cd_res = "cd" + "\r\n" """
############################# Start of IP Configuration ####################################################################

   
        """ @ setting the first octet of the IP
    
        sending command to set the first octet of the ip
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """    
        #setting command as ip1 and writing to coreui
        ip1 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 17  -v 10" + "\r\n"
        uiconn.write(ip1.encode('ascii'))
        count = 0
        for line in uiconn:
            #writing to gui if coreui not ready
            #self.configuretext.setText('Unit not ready, try again')
            #self.configurebutton.setStyleSheet('background-color: yellow')
            #writing to gui if config failed
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('IP Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                IPconfigure_check1 = False
                print("ip1 hash")
                break
            else:
                #writing to gui if config successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('IP Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    IPconfigure_check1 = True
                    print("ip1 diff")
                    break
                else:
                    #writing to gui if config successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('IP Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        IPconfigure_check1 = True
                        print("ip1 equal")
                        break
                    else:
                        #writing to gui if config failed
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            IPconfigure_check1 = False
                            print("ip1 not found")
                            break
                        else:
                            #writing to gui if config failed
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   IPconfigure_check1 = True
                                   print("ip1 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        
        """ @ setting the second octet of the IP
    
        sending command to set the second octet of the ip
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #setting command as ip2 and writing to coreui
        ip2 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 18  -v 0" + "\r\n"
        uiconn.write(ip2.encode('ascii'))
        count = 0
        for line in uiconn:
            #writing to gui if config failed
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('IP Octet 2 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                IPconfigure_check2 = False
                print("ip2 hash")
                break
            else:
                #writing to gui if config successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('IP Octet 2 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    IPconfigure_check2 = True
                    print("ip2 diff")
                    break
                else:
                    #writing to gui if config successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('IP Octet 2 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        print("ip2 equal")
                        IPconfigure_check2 = True
                        break
                    else:
                        #writing to gui if config failed
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            IPconfigure_check2 = False
                            print("ip2 not found")
                            break
                        else:
                            #writing to gui if config failed
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   IPconfigure_check2 = True
                                   print("ip2 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        """ @ setting the third octet of the IP
    
        sending command to set the third octet of the ip
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #setting command as ip3 and writing to coreui
        ip3 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 19  -v 0" + "\r\n"
        uiconn.write(ip3.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('IP Octet 3 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                IPconfigure_check3 = False
                print("ip3 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('IP Octet 3 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    IPconfigure_check3 = True
                    print("ip3 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('IP Octet 3 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        IPconfigure_check3 = True
                        print("ip3 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            IPconfigure_check3 = False
                            print("ip3 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   IPconfigure_check3 = True
                                   print("ip3 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        

        """ @ setting the fourth octet of the IP
    
        sending command to set the fourth octet of the ip
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """                              
        #writing command to coreui
        ip4 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 20  -v 6" + "\r\n"
        uiconn.write(ip4.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('IP Octet 4 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                IPconfigure_check4 = False
                print("ip4 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('IP Octet 4 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    IPconfigure_check4 = True
                    print("ip4 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('IP Octet 4 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        IPconfigure_check4 = True
                        print("ip4 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            IPconfigure_check4 = False
                            print("ip4 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   IPconfigure_check4 = True
                                   print("ip4 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        """ @ determining if all IP octets were set successfully
    
        setting the overall IP configure check true if all octet checks are true
        setting overall IP configure check false if any octet checks are false
    
        """   
        if (IPconfigure_check1 == True and IPconfigure_check2 == True and IPconfigure_check3 == True and IPconfigure_check4 == True):
           IP_configure_check = True 
        else:
           IP_configure_check = False
                                    
############################################### End of IP configuration ############################################################## 

 
          
############################################### Start of Netmask Configuration #######################################################           
        
        
        """ @ setting the first octet of the netmask
    
        sending command to set the first octet of the netmask
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        net1 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 21  -v 255" + "\r\n"
        uiconn.write(net1.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Netmask Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Netconfigure_check1 = False
                print("net1 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Netmask Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Netconfigure_check1 = True
                    print("net1 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Netmask Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Netconfigure_check1 = True
                        print("net 1 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Netconfigure_check1 = False
                            print("net1 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Netconfigure_check1 = True
                                   print("net1 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        """ @ setting the second octet of the netmask
    
        sending command to set the second octet of the netmask
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        net2 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 22  -v 255" + "\r\n"
        uiconn.write(net2.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Netmask Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Netconfigure_check2 = False
                print("net2 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Netmask Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Netconfigure_check2 = True
                    print("net2 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Netmask Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Netconfigure_check2 = True
                        print("net2 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Netconfigure_check2 = False
                            print("net2 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Netconfigure_check2 = True
                                   print("net2 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        
        """ @ setting the third octet of the netmask
    
        sending command to set the third octet of the netmask
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        net3 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 23  -v 255" + "\r\n"
        uiconn.write(net3.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Netmask Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Netconfigure_check3 = False
                print("net3 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Netmask Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Netconfigure_check3 = True
                    print("net3 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Netmask Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Netconfigure_check3 = True
                        print("net3 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Netconfigure_check3 = False
                            print("net3 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Netconfigure_check3 = True
                                   print("net3 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        """ @ setting the fourth octet of the netmask
    
        sending command to set the fourth octet of the netmask
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing commands to coreui
        net4 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 24  -v 0" + "\r\n"
        uiconn.write(net4.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Netmask Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Netconfigure_check4 = False
                print("net4 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Netmask Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Netconfigure_check4 = True
                    print("net4 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Netmask Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Netconfigure_check4 = True
                        print("net4 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Netconfigure_check4 = False
                            print("net4 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Netconfigure_check4 = True
                                   print("net4 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        """ @ determining if all netmask octets were set successfully
    
        setting the overall netmask configure check true if all octet checks are true
        setting overall netmask configure check false if any octet checks are false
    
        """   
        if (Netconfigure_check1 == True and Netconfigure_check2 == True and Netconfigure_check3 == True and Netconfigure_check4 == True):
           Net_configure_check = True 
        else:
           Net_configure_check = False

############################################### End of Netmask Configuration #############################################################
           
           

############################################### Start of Gateway Configuration ###########################################################

        """ @ setting the first octet of the gateway
    
        sending command to set the first octet of the gateway
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        gate1 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 29  -v 10" + "\r\n"
        uiconn.write(gate1.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Gateway Octet 1 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Gateconfigure_check1 = False
                print("gate1 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Gateway Octet 1 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Gateconfigure_check1 = True
                    print("gate1 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Gateway Octet 1 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Gateconfigure_check1 = True
                        print("gate1 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Gateconfigure_check1 = False
                            print("gate1 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Gateconfigure_check1 = True
                                   print("gate1 timeout")
                                   break
            #print(line.decode())
            count = count + 1

        
        """ @ setting the second octet of the gateway
    
        sending command to set the second octet of the gateway
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        gate2 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 30  -v 0" + "\r\n"
        uiconn.write(gate2.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Gateway Octet 2 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Gateconfigure_check2 = False
                print("gate2 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Gateway Octet 2 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Gateconfigure_check2 = True
                    print("gate2 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Gateway Octet 2 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Gateconfigure_check2 = True
                        print("gate2 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Gateconfigure_check2 = False
                            print("gate2 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Gateconfigure_check2 = True
                                   print("gate2 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        
        """ @ setting the third octet of the gateway
    
        sending command to set the third octet of the gateway
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        gate3 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 31  -v 0" + "\r\n"
        uiconn.write(gate3.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Gateway Octet 3 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Gateconfigure_check3 = False
                print("gate3 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Gateway Octet 3 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Gateconfigure_check3 = True
                    print("gate3 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Gateway Octet 3 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Gateconfigure_check3 = True
                        print("gate3 is equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Gateconfigure_check3 = False
                            print("gate3 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Gateconfigure_check3 = True
                                   print("gate3 timeout")
                                   break
            #print(line.decode())
            count = count + 1
        
        
        """ @ setting the fourth octet of the gateway
    
        sending command to set the fourth octet of the gateway
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to coreui
        gate4 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 32  -v 1" + "\r\n"
        uiconn.write(gate4.encode('ascii'))
        count = 0
        for line in uiconn:
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Gateway Octet 4 Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                Gateconfigure_check4 = False
                print("gate4 hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Gateway Octet 4 Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    Gateconfigure_check4 = True
                    print("gate4 diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Gateway Octet 4 Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        Gateconfigure_check4 = True
                        print("gate4 equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            Gateconfigure_check4 = False
                            print("gate4 not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   Gateconfigure_check4 = True
                                   print("gate4 timeout")
                                   break
            #print(line.decode())
            count = count + 1
      
        
        
        """ @ determining if all gateway octets were set successfully
    
        setting the overall gateway configure check true if all octet checks are true
        setting overall gateway configure check false if any octet checks are false
    
        """   
        if (Gateconfigure_check1 == True and Gateconfigure_check2 == True and Gateconfigure_check3 == True and Gateconfigure_check4 == True):
           Gate_configure_check = True 
        else:
           Gate_configure_check = False
        
################################## End of Gateway Configuration ##############################################################################  


################################## Start of URL Configuration ################################################################################
        
        """ @ setting the url for HMI to connect to
    
        sending command to set url to connect to
        checking if command is successful
        determining success of commands based on console response of HMI
        setting checks based on console responses
    
        """   
        #writing command to set primary url
        URL = "secure-db -u 5 -p 5555 -c writeparam - n db -i 9  -v http://10.0.0.1/?secret=HMI" + "\r\n"
        uiconn.write(URL.encode('ascii'))
        count = 0
        for line in uiconn:
            #t1 = time.perf_counter()
            #print("in url loop")
            #determining if command was failed or was successful
            if ("fail_hash" in line.decode()):
                #self.configuretext.setText('Primary URL Configuration Failed')
                #self.configurebutton.setStyleSheet('background-color: red')
                URLconfigure_check = False
                print("url hash")
                break
            else:
                #determining if command was failed or was successful
                if ("fail_diff" in line.decode()):
                    #self.configuretext.setText('Primary URL Already Configured')
                    #self.configurebutton.setStyleSheet('background-color: green')
                    URLconfigure_check = True
                    print("url diff")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("IS equal" in line.decode()):
                        #self.configuretext.setText('Primary URL Configuration Successful')
                        #self.configurebutton.setStyleSheet('background-color: green')
                        URLconfigure_check = True
                        print("url is equal")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("not found" in line.decode()):
                            #self.configuretext.setText('Unit not ready, try again')
                            #self.configurebutton.setStyleSheet('background-color: yellow')
                            URLconfigure_check = False
                            print("url not found")
                            break
                        else:
                            #determining if command was failed or was successful
                            if(count > 30):
                                   #self.configuretext.setText('Configure Timeout (Please try again)')
                                   #self.configurebutton.setStyleSheet('background-color: yellow')
                                   URLconfigure_check = True
                                   print("url timeout")
                                   break
            #print(line.decode())
            #t2 = time.perf_counter()
            #t = t + (t2 - t1)
            count = count + 1

################################## End of URL Configuration ##################################################################################

           
           
################################## Providing the user with feedback ##########################################################################
        #print(Ethmode_check)
        #print(IP_configure_check)
        #print(Net_configure_check)
        #print(Gate_configure_check)
        #print(URLconfigure_check)
        
        """ @ determining if all network parameters were set successfully
    
        changing gui text and color based on the status of the check for each parameter
    
        """   
        if (Ethmode_check == True and IP_configure_check == True and Net_configure_check == True and Gate_configure_check == True and URLconfigure_check == True):
            self.configuretext.setText('Configuration Complete')
            self.configuretext.setStyleSheet('background-color: green')
            # !\closing serial connection
            uiconn.close()  
            # !\settting button to red
            self.connectionstatus.setStyleSheet('background-color: red')
            # !\setting status text
            self.connectionstatus.setText('Connection Closed')
            #self.configuretext.setText('Configuration Complete')
            #self.configuretext.setStyleSheet('background-color: green')
            # !\setting flag to false
            flag = False
            self.ConnectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
            self.configurebutton.setEnabled(False)
            #self.configuretext.setEnabled(False)
            self.comtext.setText('')
            #self.configuretext.setText('')
            #self.configuretext.setStyleSheet('background-color: white')
            # closing the serial connection
            #uiconn.close()
            #self.connectionstatus.setText('Connection Closed')
            #self.connectionstatus.setStyleSheet('background-color: red')
            #self.disconnectButton.setStyleSheet('background-color: yellow')
        else:
            self.configuretext.setText('Configuration Failed, Try Again')
            self.configuretext.setStyleSheet('background-color: red')
        
###############################################################################################################################################       

       

    """ @ defining the HMIB connect button pressed
    
        opening the serial connection
        checking if the connection is open and setting the global flag accordingly
        creating a connection timeout
        creating a serial exception
        setting GUI text and color depending on connection status
    
    """
    #defining connect button press
    def ConnectButton2Pressed(self):
        
        #setting port number to the text box value
        portnumber = self.comtext2.text()
        if portnumber.isnumeric() == True: 
            #giving a value to the port value
            ui2conn.port = str('COM') + str(portnumber)
            #print(ui2conn.port)
        
            #declaring a global flag
            global flag2
            
            #try to connect
            try:
                print('test')
                #if (flag2 == False):
                #opening serial connection
                ui2conn.open()
                #providing user feedback if connection is successful
                if ui2conn.is_open:
                    print("Connection Successful")
                    self.configurebutton2.setEnabled(True)
                    self.configuretext2.setEnabled(True)
                    #setting button color to green
                    self.connectionstatus2.setStyleSheet('background-color: green')
                    #setting status text
                    self.connectionstatus2.setText('Connection Successful')
                    #assigning username and password values
                    username = "root" +"\r\n"
                    password = "fMcC0R3d1spL4y" + "\r\n"
                    #writing username and password to the coreui
                    ui2conn.write(username.encode('ascii'))
                    time.sleep(1)
                    ui2conn.write(password.encode('ascii'))
                    count = 0
                    for line in ui2conn:
                        #printing the line from coreui console
                        #print(line.decode())
                        #providing feedback to user if login incorrect
                        if("Login incorrect" in line.decode()):
                            #print("login failed")
                            #self.connectionstatus2.setText('Login Failed')
                            #self.ConnectButton2.setStyleSheet('background-color: red')
                            #self.ConnectButton2.setEnabled(True)
                            #self.disconnectButton2.setEnabled(False)
                            login2 = False
                            break
                        else:
                            #telling user login successful
                            if("root@display:~#" in line.decode()):
                               #print("login successful")
                               self.connectionstatus2.setText('Login Successful')
                               self.ConnectButton2.setEnabled(False)
                               self.disconnectButton2.setEnabled(True)
                               login2 = True
                               break
                            else:
                                #telling user login successful
                               if("not found" in line.decode()):
                                   #print("already signed in")
                                   self.connectionstatus2.setText('Login Successful')
                                   self.ConnectButton2.setEnabled(False)
                                   self.disconnectButton2.setEnabled(True)
                                   login2 = True
                                   break
                               else:
                                   #creating a login timeout
                                   if(count > 5):
                                       #print("error")
                                       #self.connectionstatus2.setText('Login Timeout (Please try again)')
                                       #self.ConnectButton2.setStyleSheet('background-color: red')
                                       #self.ConnectButton2.setEnabled(True)
                                       #self.disconnectButton2.setEnabled(False)
                                       login2 = False
                                       break
                        count = count +1
                    
                    if(login2 == False):
                        print("login2")
                        username = "root" +"\r\n"
                        password = "fM(c*R3)1$pL4y" + "\r\n"
                        # !\writing username and password to the coreui
                        ui2conn.write(username.encode('ascii'))
                        time.sleep(1)
                        for line in ui2conn:
                            if("Password" in line.decode()):
                                print("username entered")
                                break
                            else:
                                break
                            print(line.decode())
                        time.sleep(1)
                        ui2conn.write(password.encode('ascii'))
                        count = 0
                        for line in uiconn:
                            # !\printing the line from coreui console
                            print(line.decode())
                            # !\providing feedback to user if login incorrect
                            if("Login incorrect" in line.decode()):
                                #print("login failed")
                                self.connectionstatus2.setText('Login Failed')
                                self.connectionstatus2.setStyleSheet('background-color: red')
                                self.ConnectButton2.setEnabled(True)
                                self.disconnectButton2.setEnabled(False)
                                login2 = False
                                break
                            else:
                                #telling user login successful
                                if("root@display:~#" in line.decode()):
                                   #print("login successful")
                                   self.connectionstatus2.setText('Login Successful')
                                   clear = "clear" + "\r\n"
                                   ui2conn.write(clear.encode('ascii' + '\r\n'))
                                   self.ConnectButton2.setEnabled(False)
                                   self.disconnectButton2.setEnabled(True)
                                   print(line.decode())
                                   login2 = True
                                   break
                                else:
                                    # !\telling user login successful
                                   if("not found" in line.decode()):
                                       # !\print("already signed in")
                                       self.connectionstatus.setText('Login Successful')
                                       clear = "clear" + "\r\n"
                                       ui2conn.write(clear.encode('ascii' + '\r\n'))
                                       self.ConnectButton2.setEnabled(False)
                                       self.disconnectButton2.setEnabled(True)
                                       print(line.decode())
                                       login2 = True
                                       break
                                   else:
                                       # !\creating a login timeout
                                       if(count > 10):
                                          #print("error")
                                           self.connectionstatus2.setText('Login Timeout (Please try again)')
                                           self.connectionstatus2.setStyleSheet('background-color: red')
                                           self.ConnectButton2.setEnabled(True)
                                           self.disconnectButton.setEnabled(False)
                                           login2 = False
                                           break
                            count = count +1
                            print(line.decode())    
                    
                    #setting flag to true
                    flag2 = True
                    
                    ui2conn.flushInput()
                    ui2conn.flushOutput()
                    #clear = "reset" + "\r\n"
                    time.sleep(.1)
                         
                #allows user to close connection with another button press        
                '''else:
                    #closing serial connection
                    ui2conn.close()  
                    #settting button to red
                    self.ConnectButton2.setStyleSheet('background-color: red')
                    #setting status text
                    self.connectionstatus2.setText('Connection Closed')
                    #setting flag to false
                    flag2 = False'''
                    
                   
            #creating an exception if the connection fails
            except serial.SerialException as se:
                #closes connection attempt
                ui2conn.close()
                #print(se)
                #sets button color to red
                self.ConnectButton2.setStyleSheet('background-color: red')
                #sets status text
                self.connectionstatus2.setText('Connection unsuccessful')
        else:
            self.connectionstatus2.setText('Please Enter a Valid COM Port')
            self.connectionstatus2.setStyleSheet('background-color: red')


    
    
    
    """ @ defining HMIB configure button pressed
    
        sending commands for eth mode, ip, netmask, gateway, and url configuration
        checking if each command is successful
        setting the gui text/color depending on the success of the commands
        
    """    
    def configurebutton2Pressed(self):
        
            reset = "reset" + "\r\n"
            ui2conn.write(reset.encode('ascii'))
            #time.sleep(1)
            
            """ @ declaring and initializing variables
    
            declaring global boardset check variables so url can be properly 
            declaring and initializing configuration checks
        
            """
            global boardset1_check, boardset2_check, boardset3_check, boardset4_check
            #initializing variables to check configuration status
            Ethmode_check = False
            IPconfigure_check1 = False
            IPconfigure_check2 = False
            IPconfigure_check3 = False
            IPconfigure_check4 = False
            Netconfigure_check1 = False
            Netconfigure_check2 = False
            Netconfigure_check3 = False
            Netconfigure_check4 = False
            Gateconfigure_check1 = False
            Gateconfigure_check2 = False
            Gateconfigure_check3 = False
            Gateconfigure_check4 = False
            URLconfigure_check = False
            
            
            """ @ determining the value of the url based on the boardset radio button selected
    
            setting the value of the URL that will be written later
        
            """    
            if(boardset1_check == True):
                URL = "secure-db -u 5 -p 5555 -c writeparam - n db -i 9  -v http://10.0.0.1/bay=B/?secret=HMI" + "\r\n"
            else:
                if(boardset2_check == True):
                    URL = "secure-db -u 5 -p 5555 -c writeparam - n db -i 9  -v http://10.0.0.2/bay=B/?secret=HMI" + "\r\n"
                else:
                    if(boardset3_check == True):
                        URL = "secure-db -u 5 -p 5555 -c writeparam - n db -i 9  -v http://10.0.0.3/bay=B/?secret=HMI" + "\r\n"
                    else:
                        if(boardset4_check == True):
                            URL = "secure-db -u 5 -p 5555 -c writeparam - n db -i 9  -v http://10.0.0.4/bay=B/?secret=HMI" + "\r\n"
                       
            clear = "clear" + "\r\n"
            ui2conn.write(clear.encode('ascii'))
    ############################ Start of Ethernet Mode #########################################################################
            
            
            """ @ setting the eth mode (dhcp/fixed)
    
            sending command to set the eth mode
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            clear = "clear" + "\r\n"
            ui2conn.write(clear.encode('ascii'))
            
            ui2conn.flushInput()
            ui2conn.flushOutput()
            
            #setting command as ethmode and writing to coreui
            ethmode = "secure-db -u 5 -p 5555 -c writeparam - n db -i 16  -v 1" + "\r\n"
            ui2conn.write(ethmode.encode('ascii'))
            time.sleep(2)
            count = 0
            for line in ui2conn:
                #writing to gui if coreui not ready
                #self.configuretext2.setText('Unit not ready, try again')
                #self.configurebutton2.setStyleSheet('background-color: yellow')
                #writing to gui if config failed
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('IP Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Ethmode_check = False
                    print("eth hash")
                    break
                else:
                    #writing to gui if config successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('IP Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Ethmode_check = True
                        print("eth diff")
                        break
                    else:
                        #writing to gui if config successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('IP Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Ethmode_check = True
                            print("eth diff")
                            break
                        else:
                            #writing to gui if config failed
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Ethmode_check = False
                                print("not found")
                                break
                            else:
                                if("No Change" in line.decode()):
                                    Ethmode_check = True
                                    print("eth no change")
                                    break
                                else:
                                    #writing to gui if config failed
                                    if(count > 30):
                                           #self.configuretext2.setText('Configure Timeout (Please try again)')
                                           #self.configurebutton2.setStyleSheet('background-color: yellow')
                                           Ethmode_check = True
                                           print("eth timeout")
                                           break
                #print(line.decode())
                count = count +1
    
    ############################# End of Ethernet Mode Configuration ###########################################################
    
    
    
    ############################# Start of IP Configuration ####################################################################
                
           
            """ @ setting the first octet of the IP
    
            sending command to set the first octet of the ip
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """    
            #setting command as ip1 and writing to coreui
            ip1 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 17  -v 10" + "\r\n"
            ui2conn.write(ip1.encode('ascii'))
            count = 0
            for line in ui2conn:
                #writing to gui if coreui not ready
                #self.configuretext2.setText('Unit not ready, try again')
                #self.configurebutton2.setStyleSheet('background-color: yellow')
                #writing to gui if config failed
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('IP Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    IPconfigure_check1 = False
                    print("ip1 hash")
                    break
                else:
                    #writing to gui if config successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('IP Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        IPconfigure_check1 = True
                        print("ip1 diff")
                        break
                    else:
                        #writing to gui if config successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('IP Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            IPconfigure_check1 = True
                            print("ip1 equal")
                            break
                        else:
                            #writing to gui if config failed
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                IPconfigure_check1 = False
                                print("ip1 not found")
                                break
                            else:
                                #writing to gui if config failed
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       IPconfigure_check1 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the second octet of the IP
    
            sending command to set the second octet of the ip
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #setting command as ip2 and writing to coreui
            ip2 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 18  -v 0" + "\r\n"
            ui2conn.write(ip2.encode('ascii'))
            count = 0
            for line in ui2conn:
                #writing to gui if config failed
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('IP Octet 2 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    IPconfigure_check2 = False
                    print("ip2 hash")
                    break
                else:
                    #writing to gui if config successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('IP Octet 2 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        IPconfigure_check2 = True
                        print("ip2 diff")
                        break
                    else:
                        #writing to gui if config successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('IP Octet 2 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            IPconfigure_check2 = True
                            print("ip2 equal")
                            break
                        else:
                            #writing to gui if config failed
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                IPconfigure_check2 = False
                                print("ip2 not found")
                                break
                            else:
                                #writing to gui if config failed
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       IPconfigure_check2 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the third octet of the IP
    
            sending command to set the third octet of the ip
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #setting command as ip3 and writing to coreui
            ip3 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 19  -v 0" + "\r\n"
            ui2conn.write(ip3.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('IP Octet 3 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    IPconfigure_check3 = False
                    print("ip3 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('IP Octet 3 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        IPconfigure_check3 = True
                        print("ip3 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('IP Octet 3 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            IPconfigure_check3 = True
                            print("ip3 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                IPconfigure_check3 = False
                                print("ip3 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       IPconfigure_check3 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the fourth octet of the IP
    
            sending command to set the fourth octet of the ip
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            ip4 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 20  -v 7" + "\r\n"
            ui2conn.write(ip4.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('IP Octet 4 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    IPconfigure_check4 = False
                    print("ip4 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('IP Octet 4 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        IPconfigure_check4 = True
                        print("ip4 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('IP Octet 4 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            IPconfigure_check4 = True
                            print("ip4 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                IPconfigure_check4 = False
                                print("ip4 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       IPconfigure_check4 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ determining if all IP octets were set successfully
    
            setting the overall IP configure check true if all octet checks are true
            setting overall IP configure check false if any octet checks are false
    
            """
            #determining if all IP octets were successfully configured
            if (IPconfigure_check1 == True and IPconfigure_check2 == True and IPconfigure_check3 == True and IPconfigure_check4 == True):
               IP_configure_check = True 
            else:
               IP_configure_check = False
                                        
    ############################################### End of IP configuration ############################################################## 
    
     
              
    ############################################### Start of Netmask Configuration #######################################################           
            
            """ @ setting the first octet of the netmask
    
            sending command to set the first octet of the netmask
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            net1 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 21  -v 255" + "\r\n"
            ui2conn.write(net1.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Netmask Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Netconfigure_check1 = False
                    print("net1 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Netmask Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Netconfigure_check1 = True
                        print("net1 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Netmask Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Netconfigure_check1 = True
                            print("net1 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Netconfigure_check1 = False
                                print("net1 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Netconfigure_check1 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the second octet of the netmask
    
            sending command to set the second octet of the netmask
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            net2 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 22  -v 255" + "\r\n"
            ui2conn.write(net2.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Netmask Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Netconfigure_check2 = False
                    print("net2 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Netmask Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Netconfigure_check2 = True
                        print("net2 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Netmask Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Netconfigure_check2 = True
                            print("net2 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Netconfigure_check2 = False
                                print("net2 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Netconfigure_check2 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the third octet of the netmask
    
            sending command to set the third octet of the netmask
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            net3 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 23  -v 255" + "\r\n"
            ui2conn.write(net3.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Netmask Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Netconfigure_check3 = False
                    print("net3 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Netmask Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Netconfigure_check3 = True
                        print("net3 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Netmask Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Netconfigure_check3 = True
                            print("net3 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Netconfigure_check3 = False
                                print("net3 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Netconfigure_check3 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the fourth octet of the netmask
    
            sending command to set the fourth octet of the netmask
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing commands to coreui
            net4 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 24  -v 0" + "\r\n"
            ui2conn.write(net4.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Netmask Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Netconfigure_check4 = False
                    print("net4 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Netmask Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Netconfigure_check4 = True
                        print("net4 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Netmask Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Netconfigure_check4 = True
                            print("net4 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Netconfigure_check4 = False
                                print("net4 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Netconfigure_check4 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ determining if all netmask octets were set successfully
    
            setting the overall netmask configure check true if all octet checks are true
            setting overall netmask configure check false if any octet checks are false
    
            """
            #checking if all netmask octets configured successfully
            if (Netconfigure_check1 == True and Netconfigure_check2 == True and Netconfigure_check3 == True and Netconfigure_check4 == True):
               Net_configure_check = True 
            else:
               Net_configure_check = False
    
    ############################################### End of Netmask Configuration #############################################################
                
                
                
    ############################################### Start of Gateway Configuration ###########################################################
    
    
            """ @ setting the first octet of the gateway
    
            sending command to set the first octet of the gateway
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            gate1 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 29  -v 10" + "\r\n"
            ui2conn.write(gate1.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Gateway Octet 1 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Gateconfigure_check1 = False
                    print("gate1 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Gateway Octet 1 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Gateconfigure_check1 = True
                        print("gate1 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Gateway Octet 1 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Gateconfigure_check1 = True
                            print("gate1 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Gateconfigure_check1 = False
                                print("gate1 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Gateconfigure_check1 = True
                                       break
                #print(line.decode())
                count = count + 1
    
            
            """ @ setting the second octet of the gateway
    
            sending command to set the second octet of the gateway
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            gate2 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 30  -v 0" + "\r\n"
            ui2conn.write(gate2.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Gateway Octet 2 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Gateconfigure_check2 = False
                    print("gate2 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Gateway Octet 2 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Gateconfigure_check2 = True
                        print("gate2 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Gateway Octet 2 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Gateconfigure_check2 = True
                            print("gate2 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Gateconfigure_check2 = False
                                print("gate2 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Gateconfigure_check2 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the third octet of the gateway
    
            sending command to set the third octet of the gateway
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            gate3 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 31  -v 0" + "\r\n"
            ui2conn.write(gate3.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Gateway Octet 3 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Gateconfigure_check3 = False
                    print("gate3 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Gateway Octet 3 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Gateconfigure_check3 = True
                        print("gate3 diff")
                        break                    
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Gateway Octet 3 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Gateconfigure_check3 = True
                            print("gate3 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Gateconfigure_check3 = False
                                print("gate3 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Gateconfigure_check3 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            """ @ setting the fourth octet of the gateway
    
            sending command to set the fourth octet of the gateway
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to coreui
            gate4 = "secure-db -u 5 -p 5555 -c writeparam - n db -i 32  -v 1" + "\r\n"
            ui2conn.write(gate4.encode('ascii'))
            count = 0
            for line in ui2conn:
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Gateway Octet 4 Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    Gateconfigure_check4 = False
                    print("gate4 hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Gateway Octet 4 Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        Gateconfigure_check4 = True
                        print("gate4 diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Gateway Octet 4 Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            Gateconfigure_check4 = True
                            print("gate4 equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
                                #self.configuretext2.setText('Unit not ready, try again')
                                #self.configurebutton2.setStyleSheet('background-color: yellow')
                                Gateconfigure_check4 = False
                                print("gate4 not found")
                                break
                            else:
                                #determining if command was failed or was successful
                                if(count > 30):
                                       #self.configuretext2.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton2.setStyleSheet('background-color: yellow')
                                       Gateconfigure_check4 = True
                                       break
                #print(line.decode())
                count = count + 1
            
            
            
            """ @ determining if all gateway octets were set successfully
    
            setting the overall gateway configure check true if all octet checks are true
            setting overall gateway configure check false if any octet checks are false
    
            """
            #determining if all gateway octets are configured correctly 
            if (Gateconfigure_check1 == True and Gateconfigure_check2 == True and Gateconfigure_check3 == True and Gateconfigure_check4 == True):
               Gate_configure_check = True 
            else:
               Gate_configure_check = False
            
    ################################## End of Gateway Configuration ##############################################################################  
    
    
    ################################## Start of URL Configuration ################################################################################
            
            """ @ setting the url for the HMI to connect to
    
            sending command to set connection url for the HMI to connect to
            checking if command is successful
            determining success of commands based on console response of HMI
            setting checks based on console responses
        
            """
            #writing command to set primary url
            #URL = "secure-db -u 5 -p 5555 -c writeparam - n db -i 9  -v http://10.0.0.1/bay=B/?secret=HMI" + "\r\n"
            ui2conn.write(URL.encode('ascii'))
            count = 0
            for line in ui2conn:
                #t1 = time.perf_counter()
                #print("in url loop")
                #determining if command was failed or was successful
                if ("fail_hash" in line.decode()):
                    #self.configuretext2.setText('Primary URL Configuration Failed')
                    #self.configurebutton2.setStyleSheet('background-color: red')
                    URLconfigure_check = False
                    print("url hash")
                    break
                else:
                    #determining if command was failed or was successful
                    if ("fail_diff" in line.decode()):
                        #self.configuretext2.setText('Primary URL Already Configured')
                        #self.configurebutton2.setStyleSheet('background-color: green')
                        URLconfigure_check = True
                        print("url diff")
                        break
                    else:
                        #determining if command was failed or was successful
                        if ("IS equal" in line.decode()):
                            #self.configuretext2.setText('Primary URL Configuration Successful')
                            #self.configurebutton2.setStyleSheet('background-color: green')
                            URLconfigure_check = True
                            print("url equal")
                            break
                        else:
                            #determining if command was failed or was successful
                            if ("not found" in line.decode()):
# =============================================================================
#                                 self.configuretext2.setText('Unit not ready, try again')
#                                 self.configurebutton2.setStyleSheet('background-color: yellow')
# =============================================================================
                                URLconfigure_check = False
                                print("url not found")
                                break
                            else:
                                if(count > 30):
                                       #self.configuretext.setText('Configure Timeout (Please try again)')
                                       #self.configurebutton.setStyleSheet('background-color: yellow')
                                       URLconfigure_check = True
                                       print("url timeout")
                                       break
                #print(line.decode())
                #t2 = time.perf_counter()
                #t = t + (t2 - t1)
                count = count + 1
    
    ################################## End of URL Configuration ##################################################################################
    
               
               
    ################################## Providing the user with feedback ##########################################################################
            #print(Ethmode_check)
            #print(IP_configure_check)
            #print(Net_configure_check)
            #print(Gate_configure_check)
            #print(URLconfigure_check)
            
            
            """ @ determining if all parameters were set successfully
    
            checking if each overall parameter check is true
            setting text/color in GUI based on the status of each check
            
            """
            #checking to see if all settings were properly configured and providing user feedback in the gui
            if (Ethmode_check == True and IP_configure_check == True and Net_configure_check == True and Gate_configure_check == True and URLconfigure_check == True):
                self.configuretext2.setText('Configuration Complete')
                self.configuretext2.setStyleSheet('background-color: green')
                #closing the serial connection
                #ui2conn.close()
                # !\closing serial connection
                ui2conn.close()  
                # !\settting button to red
                self.connectionstatus2.setStyleSheet('background-color: red')
                # !\setting status text
                self.connectionstatus2.setText('Connection Closed')
                # !\setting flag to false
                flag = False
                self.ConnectButton2.setEnabled(True)
                self.disconnectButton2.setEnabled(False)
                self.comtext2.setText('')
                #self.configuretext2.setText('')
                #self.configuretext2.setStyleSheet('background-color: white')
            else:
                self.configuretext2.setText('Configuration Failed, Try Again')
                self.configuretext2.setStyleSheet('background-color: red')       
   
    
    ###################################################################################################################################



""" @calling functions for GUI

showing the GUI window

"""
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
