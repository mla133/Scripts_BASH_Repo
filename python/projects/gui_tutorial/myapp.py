from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My awesome App")
        
        label.QLabel("THIS IS AWESOME!!!")

        # The `Qt` namespace has a lot of attributes to customize
        # widgets.  See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the window.  Widget will expand
        # to take up all space in the window by default.
        self.setCentralWidget(label)
        



app = QApplication(sys.argv)

window = QMainWindow()
window.show()  # IMPORTANT: Windows are hidden by default.

# Start the event loop
app.exec()
