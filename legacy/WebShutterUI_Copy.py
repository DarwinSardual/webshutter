from PyQt5 import uic
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLineEdit, QDesktopWidget, QTableWidget,
        QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QAction, QLabel, QTextEdit, QGridLayout, QRadioButton)
from table.TableWidgetRowItem import TableWidgetRowItem
from table.WebShutterTableWidget import WebShutterTableWidget
from PyQt5.QtGui import QIcon, QPixmap
import os
from Config_Copy import Config
from WebShutterTextEdit import WebShutterTextEdit

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
        shutterIconPath = os.path.join(self.dirname, "../images/shutter.svg")
        shutterIcon = QIcon(shutterIconPath)

        self.setWindowIcon(shutterIcon)
        self.__initWidgets()
        self.__setupTable()
        self.__setIcons()
        self.__setupTextEdit()
        self.show()

    def __setIcons(self):

        searchIconPath = os.path.join(self.dirname, "../images/search.svg")
        deleteIconPath = os.path.join(self.dirname, "../images/delete.svg")
        startIconPath = os.path.join(self.dirname, "../images/play.svg")
        addIconPath = os.path.join(self.dirname, "../images/add.svg")

        searchButtonIcon = QIcon(searchIconPath)
        self.searchButton.setIcon(searchButtonIcon)

        deleteButtonIcon = QIcon(deleteIconPath)
        self.deleteButton.setIcon(deleteButtonIcon)

        startButtonIcon = QIcon(startIconPath)
        self.startStopButton.setIcon(startButtonIcon)

        addButtonIcon = QIcon(addIconPath)
        self.addButton.setIcon(addButtonIcon)

    def __initWidgets(self):

        self.verticalLayout = self.uiRef.findChild(QVBoxLayout, "verticalLayout")
        self.gridLayout = self.uiRef.findChild(QGridLayout, "gridLayout")

        self.filterCombo = self.uiRef.findChild(QComboBox, "filterCombo")
        self.filterCombo.setStyleSheet("padding: 0")

        self.searchLine = self.uiRef.findChild(QLineEdit, "searchLine")
        self.searchButton = self.uiRef.findChild(QPushButton, "searchButton")
        self.deleteButton = self.uiRef.findChild(QPushButton, "deleteButton")
        self.startStopButton = self.uiRef.findChild(QPushButton, "startStopButton")
        self.addButton = self.uiRef.findChild(QPushButton, "addButton")

        self.mobileRadioButton = self.uiRef.findChild(QRadioButton, "mobileRadioButton")
        self.desktopRadioButton = self.uiRef.findChild(QRadioButton, "desktopRadioButton")
        self.dimensionsCombo = self.uiRef.findChild(QComboBox, "dimensionsCombo")


    def __setupTable(self):

        self.tableWidget = WebShutterTableWidget()
        self.verticalLayout.insertWidget(1, self.tableWidget)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 0)

    def __setupTextEdit(self):
        self.inputTextEdit = WebShutterTextEdit()
        self.inputTextEdit.setPlaceholderText("Enter the links here seperated by space or new line")
        self.gridLayout.addWidget(self.inputTextEdit, 1, 0, 1, 7)

    def __setAppMaxSize(self, widthPercent, heightPercent):

        self.desktopWidth = self.dw.width()
        self.desktopHeight = self.dw.height()
        width = self.desktopWidth * widthPercent
        height = self.desktopHeight * heightPercent
        self.setMaximumSize(width, height)

        return (width, height)
