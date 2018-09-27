# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WebShutterUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class UI_WebShutter(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(581, 590)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.filterCombo = QtWidgets.QComboBox(self.widget)
        self.filterCombo.setObjectName("filterCombo")
        self.filterCombo.addItem("")
        self.filterCombo.addItem("")
        self.filterCombo.addItem("")
        self.gridLayout.addWidget(self.filterCombo, 0, 0, 1, 1)
        self.searchLine = QtWidgets.QLineEdit(self.widget)
        self.searchLine.setObjectName("searchLine")
        self.gridLayout.addWidget(self.searchLine, 0, 1, 1, 1)
        self.dimensionsCombo = QtWidgets.QComboBox(self.widget)
        self.dimensionsCombo.setObjectName("dimensionsCombo")
        self.gridLayout.addWidget(self.dimensionsCombo, 0, 6, 1, 1)
        self.mobileRadioButton = QtWidgets.QRadioButton(self.widget)
        self.mobileRadioButton.setObjectName("mobileRadioButton")
        self.gridLayout.addWidget(self.mobileRadioButton, 0, 4, 1, 1)
        self.desktopRadioButton = QtWidgets.QRadioButton(self.widget)
        self.desktopRadioButton.setObjectName("desktopRadioButton")
        self.gridLayout.addWidget(self.desktopRadioButton, 0, 5, 1, 1)
        self.searchButton = QtWidgets.QPushButton(self.widget)
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.addButton = QtWidgets.QPushButton(self.widget_2)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QPushButton(self.widget_2)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.startStopButton = QtWidgets.QPushButton(self.widget_2)
        self.startStopButton.setObjectName("startStopButton")
        self.horizontalLayout.addWidget(self.startStopButton)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.filterCombo.setItemText(0, _translate("MainWindow", "All"))
        self.filterCombo.setItemText(1, _translate("MainWindow", "URL"))
        self.filterCombo.setItemText(2, _translate("MainWindow", "Status"))
        self.mobileRadioButton.setText(_translate("MainWindow", "Mobile"))
        self.desktopRadioButton.setText(_translate("MainWindow", "Desktop"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.deleteButton.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.startStopButton.setText(_translate("MainWindow", "Start"))
