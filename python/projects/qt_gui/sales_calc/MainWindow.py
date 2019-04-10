# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 10, 258, 516))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.price = QtWidgets.QLabel(self.widget)
        self.price.setObjectName("price")
        self.verticalLayout.addWidget(self.price)
        self.price_box = QtWidgets.QTextEdit(self.widget)
        self.price_box.setObjectName("price_box")
        self.verticalLayout.addWidget(self.price_box)
        self.tax_rate = QtWidgets.QSpinBox(self.widget)
        self.tax_rate.setProperty("value", 20)
        self.tax_rate.setObjectName("tax_rate")
        self.verticalLayout.addWidget(self.tax_rate)
        self.calc_tax_button = QtWidgets.QPushButton(self.widget)
        self.calc_tax_button.setObjectName("calc_tax_button")
        self.verticalLayout.addWidget(self.calc_tax_button)
        self.results_window = QtWidgets.QTextEdit(self.widget)
        self.results_window.setObjectName("results_window")
        self.verticalLayout.addWidget(self.results_window)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Sales Tax Calculator"))
        self.price.setText(_translate("MainWindow", "Price"))
        self.calc_tax_button.setText(_translate("MainWindow", "Calculate"))


