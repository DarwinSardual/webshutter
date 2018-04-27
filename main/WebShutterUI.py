from PyQt5 import uic
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLineEdit, QDesktopWidget, QTableWidget,
        QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton)
from table.TableWidgetRowItem import TableWidgetRowItem
from table.WebShutterTableWidget import WebShutterTableWidget
import os

class WebShutterUI(QMainWindow):

    def __init__(self):
        super(WebShutterUI, self).__init__()

        self.uiRef = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),'WebShutterUI.ui'), self) # first load the ui file
        self.dw = QDesktopWidget(); # for desktop size
        self.appMaxSize = self.__setAppMaxSize(0.30, 0.5) # set using percent
        width, height = self.appMaxSize
        self.setGeometry(50, 50, width, height)
        self.setWindowTitle("Web Shutter")

        self.__initWidgets()
        self.__setupTable()
        self.show()

    def __initWidgets(self):
        self.filterCombo = self.uiRef.findChild(QComboBox, "filterCombo")
        self.filterCombo.setStyleSheet("padding: 0")
        self.searchLine = self.uiRef.findChild(QLineEdit, "searchLine")
        self.searchButton = self.uiRef.findChild(QPushButton, "searchButton")
        self.deleteButton = self.uiRef.findChild(QPushButton, "deleteButton")
        self.startStopButton = self.uiRef.findChild(QPushButton, "startStopButton")

    def __setupTable(self):
        verticalLayout = self.uiRef.findChild(QVBoxLayout, "verticalLayout")
        self.tableWidget = WebShutterTableWidget()
        verticalLayout.addWidget(self.tableWidget)

    def __setAppMaxSize(self, widthPercent, heightPercent):

        self.desktopWidth = self.dw.width()
        self.desktopHeight = self.dw.height()
        width = self.desktopWidth * widthPercent
        height = self.desktopHeight * heightPercent
        self.setMaximumSize(width, height)

        return (width, height)
