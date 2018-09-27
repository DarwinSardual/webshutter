from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QRadioButton, QLineEdit, QPushButton
import os

class PreferencesUI(QDialog):
    
    def __init__(self):
        super(PreferencesUI, self).__init__()
        self.dw = QDesktopWidget();
        self.prefUIRef = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),'PreferencesUI.ui'), self)
        
        self.dialogMaxSize = self.__setDialogMaxSize(0.20, 0.10) # set using percent
        width, height = self.dialogMaxSize
        self.setGeometry(50, 50, width, height)
        
        self.__initWidgets()
        
        self.setWindowModality(Qt.ApplicationModal)
        
    def __initWidgets(self):
        self.mobileRadioButton = self.prefUIRef.findChild(QRadioButton, "mobileRadioButton")
        self.desktopRadioButton = self.prefUIRef.findChild(QRadioButton, "desktopRadioButton")
        
        self.widthLine = self.prefUIRef.findChild(QLineEdit, "widthLine")
        self.heightLine = self.prefUIRef.findChild(QLineEdit, "heightLine")
        
        self.cancelButton = self.prefUIRef.findChild(QPushButton, "cancelButton")
        self.saveButton = self.prefUIRef.findChild(QPushButton, "saveButton")
        
        validator = QIntValidator(5000, 5000)
        
        self.widthLine.setValidator(validator)
        self.heightLine.setValidator(validator)
        
    def __setDialogMaxSize(self, widthPercent, heightPercent):
        
        self.desktopWidth = self.dw.width()
        self.desktopHeight = self.dw.height()
        width = self.desktopWidth * widthPercent
        height = self.desktopHeight * heightPercent
        self.setMaximumSize(width, height)

        return (width, height)
