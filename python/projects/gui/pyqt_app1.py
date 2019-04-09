from PyQt5 import QtWidgets, QtGui, QtCore
class PyQtApp(QtWidgets.QWidget):
   
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("PyQt Application")
        self.setWindowIcon(QtGui.QIcon("Your/image/file.png"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myapp = PyQtApp()
    myapp.show()
    sys.exit(app.exec_())
