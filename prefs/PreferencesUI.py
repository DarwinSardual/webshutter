from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QRadioButton, QLineEdit, QPushButton
import os
from UI_Preferences import UI_Preferences

class PreferencesUI(QDialog):
    
    def __init__(self):
        super(PreferencesUI, self).__init__()
        self.dw = QDesktopWidget();
        self.prefUIRef = UI_Preferences()
        self.prefUIRef.setupUi(self)
        
        self.dialogMaxSize = self.__setDialogMaxSize(0.20, 0.10) # set using percent
        width, height = self.dialogMaxSize
        self.setGeometry(50, 50, width, height)
        
        self.__initWidgets()
        
        self.setWindowModality(Qt.ApplicationModal)
        
    def __initWidgets(self):
        self.mobileRadioButton = self.prefUIRef.mobileRadioButton
        self.desktopRadioButton = self.prefUIRef.desktopRadioButton
        
        self.widthLine = self.prefUIRef.widthLine
        self.heightLine = self.prefUIRef.heightLine
        
        self.cancelButton = self.prefUIRef.cancelButton
        self.saveButton = self.prefUIRef.saveButton
        
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
