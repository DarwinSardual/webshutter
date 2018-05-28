import re, time
import os, sys
from queue import Queue
from collections import deque
from threading import Thread
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from WebShutterUI import WebShutterUI
from TableWidgetRowItem import TableWidgetRowItem
from Status import Status
from Item import Item
from SqliteCon import SqliteCon
from Config import Config
from WebShutterThread import WebShutterThread
from PreferencesUIController import PreferencesUIController
from Dimension import Dimension

class WebShutterUIController:

    def __init__(self):
        self.webShutterUI = WebShutterUI()
        self.__databaseConnection = SqliteCon()
        self.__toRun = False
        self.__numThreads = 0
        self.__threads = deque()
        self.results = Queue()
        self.resultToProcess = 0

        #self.dirname = os.path.dirname(os.path.abspath(__file__))
        if not Config.checkPreferencesConfig() or not Config.checkPreferencesConfigFormat():
            Config.createPreferencesConfig()

        Config.createSaveDirectory()
        self.__setupTable()

        self.mode = None

        self.pref = Config.getConfig()
        self.__initPreferences()
        self.__initSignals()

    def __initPreferences(self):
        #self.preferencesUI.widthLine.setText(str(self.pref["dimensions"]["width"]))
        #self.preferencesUI.heightLine.setText(str(self.pref["dimensions"]["height"]))

        if self.pref["mode"] == "mobile":
            self.webShutterUI.mobileRadioButton.setChecked(True)
            self.mode = self.pref["mode"]
        else:
            self.webShutterUI.desktopRadioButton.setChecked(True)
            self.mode = "desktop" #fail safe in case the json file has been modified

        self.webShutterUI.mobileRadioButton.toggled.connect(lambda: self.__modeToggled(self.webShutterUI.mobileRadioButton))
        self.webShutterUI.desktopRadioButton.toggled.connect(lambda: self.__modeToggled(self.webShutterUI.desktopRadioButton))

        # Set Dimensions
        index = 0
        #isDimensionSet = False
        for dimension in Dimension.Value:
            self.webShutterUI.dimensionsCombo.addItem(str(dimension["width"]) + " x " + str(dimension["height"]))
            if self.pref["dimensions"]["width"] == dimension["width"] and self.pref["dimensions"]["height"] == dimension["height"]:
                self.webShutterUI.dimensionsCombo.setCurrentIndex(index)
            #    isDimensionSet = True
            else:
                index += 1

        #if not isDimensionSet:
        #    Config.createPreferencesConfig()


    def __initSignals(self):
        #self.webShutterUI.tableWidget.rowInput.addButton.clicked.connect(self.addButtonClicked)
        #self.webShutterUI.addButton.clicked.connect(self.addButtonClicked)
        self.webShutterUI.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.webShutterUI.searchButton.clicked.connect(self.searchButtonClicked)
        self.webShutterUI.startStopButton.clicked.connect(self.startStopButtonClicked)
        self.webShutterUI.inputTextEdit.setCallback(self.addAndStart)
        self.webShutterUI.dimensionsCombo.currentIndexChanged.connect(self.__dimensionChanged)
        #self.webShutterUI.preferencesAction.triggered.connect(self.preferencesActionTriggered)
        #self.webShutterUI.exitAction.triggered.connect(self.webShutterUI.close)

    def __setupTable(self):
         data = self.__fetchAllDataFromDatabase()
         self.fillTable(data)


    def searchButtonClicked(self):
        comboBox = self.webShutterUI.filterCombo;
        searchText = self.webShutterUI.searchLine.text().strip()
        filterBy = comboBox.currentText().lower()
        # implement search

        res = self.__searchFromDatabase(searchText, filterBy)
        self.webShutterUI.tableWidget.clearTable()
        self.fillTable(res)

    def fillTable(self, items):
        for dbId, url, status, statusText, isChecked in items:
            item = Item(dbId, url, status, isChecked)
            rowItem = TableWidgetRowItem(item)
            rowItem.setToggleCallback(self.__toggleCheckbox)
            self.webShutterUI.tableWidget.addRowItem(rowItem)

    def deleteButtonClicked(self):
        items = self.webShutterUI.tableWidget.deleteCheckedItems()
        for item in items:
            self.__deleteItemFromDatabase(item.getItem().dbId)

    def addButtonClicked(self):

        links = self.webShutterUI.inputTextEdit.toPlainText()
        links = links.strip()

        if links == "":
            return # empty string

        linkList = re.split("\s+", links)

        items = []
        for link in linkList:
            item = Item(-1, link, Status.PENDING, True)
            id = self.__addItemToDatabase(item)
            if id > 0:
                item.dbId = id
            rowItem = TableWidgetRowItem(item)
            self.webShutterUI.tableWidget.addRowItem(rowItem)
            rowItem.setToggleCallback(self.__toggleCheckbox)
            items.append(rowItem)

        self.webShutterUI.inputTextEdit.setText("")
        return items

    def startStopButtonClicked(self):

        if self.__toRun:
            self.__toRun = False
            return

        checkedRowItems = self.webShutterUI.tableWidget.getCheckedRowItems()
        self.spawnThread(checkedRowItems)

        #spawn a new thread to start the threads
        startThread = Thread(target=self.__startThreads)
        startThread.start()

    def spawnThread(self, rowItems):
        args = self.getGeneralArgs()

        for item in rowItems:
            link = item.getItem().link
            filename =  link + "_" + time.strftime('%Y%M%d%H%M%S%Ms') + Config.IMAGE_EXT
            filenameArgs = "--filename" + filename

            command = [args["casperJS"], args["screenshotScript"],
                link, args["size"], args["device"], args["path"], filenameArgs
            ]
            commandStr = " ".join(command)
            commandStr += " --ignore-ssl-errors=true"

            thread = WebShutterThread(commandStr, item)
            thread.finishCallback.connect(self.finishThreading)
            thread.toProcessCallback.connect(self.updateRowItem)


            self.__threads.append(thread)

    def addAndStart(self):
        rowItems = self.addButtonClicked()
        if self.__toRun:
            self.spawnThread(rowItems)
        else:
            self.startStopButtonClicked()

    #def preferencesActionTriggered(self):

    #    if not Config.checkPreferencesConfig() or not Config.checkPreferencesConfigFormat():
    #        Config.createPreferencesConfig()

    #    self.pref = PreferencesUIController()

    #START - callback methods for the thread

    def updateRowItem(self, rowItem, status, isChecked = None):
        rowItem.setStatus(status)
        if not isChecked == None:
            rowItem.setChecked(isChecked)

    def finishThreading(self, rowItem, status):
        self.updateRowItem(rowItem, status)
        self.__numThreads -= 1

        #
        #update database
        self.__updateItemToDatabase(rowItem.getItem())

    #END - callback methods for the thread

    def getGeneralArgs(self):

        if not Config.checkPreferencesConfig() and not Config.checkPreferencesConfigFormat():
            Config.createPreferencesConfig()

        pref = Config.getConfig()

        #get the settings here
        path = "D:\\DarwinFiles\\Work\\Projects\\webshutter\\test\\save"
        #path = "/home/darwin/Projects/Python/webshutter/test/save"
        sizeArgs = "--size=" + str(pref["dimensions"]["width"]) + "x" + str(pref["dimensions"]["height"])
        deviceArgs = "--" + pref["mode"]
        pathArgs = "--output" + path

        args = { "size": sizeArgs, "device": str(deviceArgs), "path": pathArgs,
            "casperJS": Config.CASPERJS_PATH, "screenshotScript": Config.SCREENSHOT_SCRIPT_PATH
        }

        return args

    def __dimensionChanged(self, index):
        dimension = Dimension.Value[index]
        self.pref["dimensions"]["width"] = dimension["width"]
        self.pref["dimensions"]["height"] = dimension["height"]

        Config.createPreferencesConfig(self.pref)

    def __modeToggled(self, button):

        if button.isChecked():
            if button == self.webShutterUI.mobileRadioButton:
                self.pref["mode"] = "mobile"
                Config.createPreferencesConfig(self.pref)
            elif button == self.webShutterUI.desktopRadioButton:
                self.pref["mode"] = "desktop"
                Config.createPreferencesConfig(self.pref)

    def __toggleCheckbox(self, item):

        checkbox = self.webShutterUI.tableWidget.getCheckboxAll()

        if item.isChecked:
            self.webShutterUI.tableWidget.setNumCheck(self.webShutterUI.tableWidget.getNumCheck() + 1)
        else:
            self.webShutterUI.tableWidget.setNumCheck(self.webShutterUI.tableWidget.getNumCheck() - 1)

        checkbox.setCheckState(Qt.Checked) if  self.webShutterUI.tableWidget.getNumCheck() == len(self.webShutterUI.tableWidget.getRowItems()) else checkbox.setCheckState(Qt.Unchecked)
        self.__updateItemToDatabase(item)


    def __startThreads(self):
        #start threading
        self.__toRun = True
        stopIconPath = "images/stop.svg"
        stopIcon = QIcon(stopIconPath)
        self.webShutterUI.startStopButton.setIcon(stopIcon)
        self.webShutterUI.startStopButton.setText("Stop")
        self.webShutterUI.deleteButton.setEnabled(False)

        while len(self.__threads) > 0 and self.__toRun:
            if self.__numThreads < Config.MAX_THREADS:
                self.__numThreads += 1
                thread = self.__threads.popleft()
                thread.start()
            time.sleep(1)

        self.__toRun = False
        playIconPath = "images/play.svg"
        playIcon = QIcon(playIconPath)
        self.webShutterUI.startStopButton.setIcon(playIcon)
        self.webShutterUI.startStopButton.setText("Start")
        self.webShutterUI.deleteButton.setEnabled(True)

        self.__threads = deque() # always clear the threads before after running

    def __fetchAllDataFromDatabase(self):
        sql = "select * from urls"
        data = self.__databaseConnection.fetchall(sql)
        return data

    def __searchFromDatabase(self, searchText, filterBy):
        sql = "SELECT * from urls "
        params = ()

        if filterBy == "url":
            sql += "Where url like ?"
            params = (searchText + "%", )
        elif filterBy == "status":
            sql += "Where status_label like ?"
            params = (searchText + "%", )
        else:
            sql += "WHERE url LIKE ? or status_label LIKE ?"
            params = (searchText + "%", searchText + "%")

        return self.__databaseConnection.fetchall(sql, params)

    def __addItemToDatabase(self,item):
        sql = "INSERT INTO urls(url, status, status_label, is_checked) VALUES(?, ?, ?, ?)"
        params = (item.link, item.status, Status.State[item.status], item.isChecked)
        return self.__databaseConnection.insert(sql, params)

    def __deleteItemFromDatabase(self, id):
        sql = "DELETE FROM urls WHERE id = ?"
        params = (id,)
        self.__databaseConnection.delete(sql, params)

    def __updateItemToDatabase(self, item):
        sql = "UPDATE urls SET status = ?, status_label = ?, is_checked = ? where id = ?"
        params = (item.status, Status.State[item.status], item.isChecked, item.dbId)
        self.__databaseConnection.update(sql, params)
