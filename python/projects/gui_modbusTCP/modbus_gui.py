import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

from pyModbusTCP.client import ModbusClient
import utils

Ui_MainWindow, QtBaseClass = uic.loadUiType("layout.ui")

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submit_ip_connect.clicked.connect(self.ConnectIP)
        self.ui.submit_mb_command.clicked.connect(self.SendModbus)
        self.ui.submit_clear_window.clicked.connect(self.ClearWindow)

    def ConnectIP(self):
        host = str(self.ui.ip_addr.toPlainText())
        port = 502

        if(host == ""):
            host="192.168.181.79"
        else:
            host = str(self.ui.ip_addr.toPlainText())
        
        self.c = ModbusClient(host, port, auto_open=True)

        # open or reconnect TCP to server
        if not self.c.is_open():
            if not self.c.open():
                self.ui.results.setText("NOT Connected")
                print("NOT Connected")
        if self.c.is_open():
            self.ui.results.setText("Connected to: "+ str(host))
            print("Connected to: " + str(host) + ":" + str(port))

    def SendModbus(self):
        mb_func = int(self.ui.mb_func.toPlainText())
        mb_reg = int(self.ui.mb_reg.toPlainText())
        mb_value = int(self.ui.mb_value.toPlainText())

        if (mb_func == 2):
            regs = self.c.read_discrete_inputs(mb_reg, mb_value)
            print("Func " + str(mb_func) + ": Reg: " + str(mb_reg) + " Number: " + str(mb_value) + " " + str(regs))
        elif (mb_func == 3):
            regs = self.c.read_holding_registers(mb_reg, mb_value)
            print("Func " + str(mb_func) + ": Reg: " + str(mb_reg) + " Number: " + str(mb_value) + " " + str(regs))
        else:   
            print("Not Func 02 or 03")
            regs = "[ERROR] Only Functions 02 & 03 are supported currently."

        self.ui.results.setText(str(regs))


    def ClearWindow(self):
        self.ui.results.setText("")
        print("Cleared Window")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
