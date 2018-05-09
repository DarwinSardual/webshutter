from PyQt5 import uic
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLineEdit, QDesktopWidget, QTableWidget,
        QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QAction, QLabel)
from table.TableWidgetRowItem import TableWidgetRowItem
from table.WebShutterTableWidget import WebShutterTableWidget
from PyQt5.QtGui import QIcon, QPixmap
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

        self.dirname = os.path.dirname(os.path.abspath(__file__))
        #shutterIconPath = os.path.join(dirname, "..\\images\\shutter.svg")
        shutterIconPath = os.path.join(self.dirname, "../images/shutter.svg")
        shutterIcon = QIcon(shutterIconPath)

        self.setWindowIcon(shutterIcon)

        self.__initWidgets()
        self.__setupTable()
        self.__setIcons()
        self.show()

    def __setIcons(self):
        #searchIconPath = os.path.join(dirname, "..\\images\\search.svg")
        #deleteIconPath = os.path.join(dirname, "..\\images\\delete.svg")
        #startIconPath = os.path.join(dirname, "..\\images\\play.svg")

        searchIconPath = os.path.join(self.dirname, "../images/search.svg")
        deleteIconPath = os.path.join(self.dirname, "../images/delete.svg")
        startIconPath = os.path.join(self.dirname, "../images/play.svg")
        filterIconPath = os.path.join(self.dirname, "../images/filter.svg")
        
        searchButtonIcon = QIcon(searchIconPath)
        self.searchButton.setIcon(searchButtonIcon)
        
        deleteButtonIcon = QIcon(deleteIconPath)
        self.deleteButton.setIcon(deleteButtonIcon)
        
        startButtonIcon = QIcon(startIconPath)
        self.startStopButton.setIcon(startButtonIcon)
        

    def __initWidgets(self):
        self.filterCombo = self.uiRef.findChild(QComboBox, "filterCombo")
        self.filterCombo.setStyleSheet("padding: 0")
        self.searchLine = self.uiRef.findChild(QLineEdit, "searchLine")
        self.searchButton = self.uiRef.findChild(QPushButton, "searchButton")
        self.deleteButton = self.uiRef.findChild(QPushButton, "deleteButton")
        self.startStopButton = self.uiRef.findChild(QPushButton, "startStopButton")
        self.preferencesAction = self.uiRef.findChild(QAction, "preferencesAction")
        self.exitAction = self.uiRef.findChild(QAction, "exitAction")
        

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
