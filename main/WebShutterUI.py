from PyQt5 import uic
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLineEdit, QDesktopWidget, QTableWidget,
        QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QAction, QLabel, QTextEdit)
from table.TableWidgetRowItem import TableWidgetRowItem
from table.WebShutterTableWidget import WebShutterTableWidget
from PyQt5.QtGui import QIcon, QPixmap
import os
from UI_WebShutter import UI_WebShutter
from Config import Config
from WebShutterTextEdit import WebShutterTextEdit

class WebShutterUI(QMainWindow):

    def __init__(self):
        super(WebShutterUI, self).__init__()

        self.uiRef = UI_WebShutter()
        self.uiRef.setupUi(self)
        self.dw = QDesktopWidget(); # for desktop size
        self.appMaxSize = self.__setAppMaxSize(0.30, 0.5) # set using percent
        width, height = self.appMaxSize
        self.setGeometry(50, 50, width, height)
        self.setWindowTitle("Web Shutter")

        shutterIconPath = "images/shutter.svg"
        shutterIcon = QIcon(shutterIconPath)

        self.setWindowIcon(shutterIcon)

        self.__initWidgets()
        self.__setupTable()
        self.__setIcons()
        self.__setupTextEdit()
        self.show()

    def __setIcons(self):

        searchIconPath = "images/search.svg"
        deleteIconPath = "images/delete.svg"
        startIconPath = "images/play.svg"
        filterIconPath = "images/filter.svg"
        #addIconPath = "images/add.svg"

        searchButtonIcon = QIcon(searchIconPath)
        self.searchButton.setIcon(searchButtonIcon)

        deleteButtonIcon = QIcon(deleteIconPath)
        self.deleteButton.setIcon(deleteButtonIcon)

        startButtonIcon = QIcon(startIconPath)
        self.startStopButton.setIcon(startButtonIcon)

        #addButtonIcon = QIcon(addIconPath)
        #self.addButton.setIcon(addButtonIcon)

    def __initWidgets(self):

        self.verticalLayout = self.uiRef.verticalLayout
        self.gridLayout = self.uiRef.gridLayout

        self.filterCombo = self.uiRef.filterCombo
        self.filterCombo.setStyleSheet("padding: 0")

        self.searchLine = self.uiRef.searchLine
        self.searchButton = self.uiRef.searchButton
        self.deleteButton = self.uiRef.deleteButton
        self.startStopButton = self.uiRef.startStopButton

        #self.addButton = self.uiRef.addButton
        self.mobileRadioButton = self.uiRef.mobileRadioButton
        self.desktopRadioButton = self.uiRef.desktopRadioButton
        self.dimensionsCombo = self.uiRef.dimensionsCombo

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
