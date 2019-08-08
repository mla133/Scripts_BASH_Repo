# This GUI skeleton file built using tutorial found at:
# https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

# This requires PyQt5 and Python3 to be installed

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

# "layout.ui" created by Qt Designer (run "designer" in console)
Ui_MainWindow, QtBaseClass = uic.loadUiType("layout.ui")

class MyApp(QMainWindow):
    # Initialize the window to plug in functionality to each button/textbox/etc
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Add functionality for each control or output window in GUI
        self.ui.submit_ip_connect.clicked.connect(self.ConnectIP)

    # Implement the function ConnectIP when self.ConnectIP defined above is clicked
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

# Run the actual app to display the window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
