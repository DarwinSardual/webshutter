# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreferencesUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class UI_Preferences(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.mobileRadioButton = QtWidgets.QRadioButton(self.widget_3)
        self.mobileRadioButton.setObjectName("mobileRadioButton")
        self.horizontalLayout_4.addWidget(self.mobileRadioButton)
        self.desktopRadioButton = QtWidgets.QRadioButton(self.widget_3)
        self.desktopRadioButton.setObjectName("desktopRadioButton")
        self.horizontalLayout_4.addWidget(self.desktopRadioButton)
        self.horizontalLayout_3.addWidget(self.widget_3)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_4 = QtWidgets.QWidget(self.groupBox)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widthLine = QtWidgets.QLineEdit(self.widget_4)
        self.widthLine.setObjectName("widthLine")
        self.horizontalLayout_5.addWidget(self.widthLine)
        self.label = QtWidgets.QLabel(self.widget_4)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.heightLine = QtWidgets.QLineEdit(self.widget_4)
        self.heightLine.setObjectName("heightLine")
        self.horizontalLayout_5.addWidget(self.heightLine)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget_5 = QtWidgets.QWidget(Dialog)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout.setObjectName("gridLayout")
        self.cancelButton = QtWidgets.QPushButton(self.widget_5)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self.widget_5)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.widget_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Preferences"))
        self.groupBox_2.setTitle(_translate("Dialog", "Mode"))
        self.mobileRadioButton.setText(_translate("Dialog", "Mobi&le"))
        self.desktopRadioButton.setText(_translate("Dialog", "&Desktop"))
        self.groupBox.setTitle(_translate("Dialog", "Dimensions"))
        self.widthLine.setPlaceholderText(_translate("Dialog", "Width"))
        self.label.setText(_translate("Dialog", "x"))
        self.heightLine.setPlaceholderText(_translate("Dialog", "Height"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.saveButton.setText(_translate("Dialog", "Save"))

