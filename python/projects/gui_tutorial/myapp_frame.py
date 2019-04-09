from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

    def onMyToolBarButtonClick(self, s):
        print("click", s)
        dlg = QDialog(self)
        dlg.setWindowTitle("HELLO!")
        dlg.exec_()

app = QApplication(sys.argv)

window = MainWindow()
window.show()  # IMPORTANT: Windows are hidden by default.

# Start the event loop
app.exec()
