from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDesktopWidget
import os

class PreferencesUI(QDialog):
    
    def __init__(self):
        super(PreferencesUI, self).__init__()
        self.dw = QDesktopWidget();
        self.prefUIRef = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),'PreferencesUI.ui'), self)
        
        self.dialogMaxSize = self.__setDialogMaxSize(0.15, 0.10) # set using percent
        width, height = self.dialogMaxSize
        self.setGeometry(50, 50, width, height)
        
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()
        
    def __setDialogMaxSize(self, widthPercent, heightPercent):
        
        self.desktopWidth = self.dw.width()
        self.desktopHeight = self.dw.height()
        width = self.desktopWidth * widthPercent
        height = self.desktopHeight * heightPercent
        self.setMaximumSize(width, height)

        return (width, height)
