from main.WebShutterUI import WebShutterUI
from table.TableWidgetRowItem import TableWidgetRowItem
from PyQt5.QtCore import Qt
import re, time
from util.Status import Status
from util.Item import Item
from util.SqliteCon import SqliteCon
from util.Config import Config
from collections import deque
from util.WebShutterThread import WebShutterThread
from queue import Queue
from threading import Thread

class WebShutterUIController:

    def __init__(self):
        self.webShutterUI = WebShutterUI()
        self.__initSignals()
        self.__databaseConnection = SqliteCon()
        self.__toRun = False
        self.__numThreads = 0
        self.__threads = deque()
        self.results = Queue()
        self.resultToProcess = 0

    def __initSignals(self):
        self.webShutterUI.tableWidget.rowInput.addButton.clicked.connect(self.addButtonClicked)
        self.webShutterUI.searchButton.clicked.connect(self.searchButtonClicked)
        self.webShutterUI.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.webShutterUI.searchButton.clicked.connect(self.searchButtonClicked)
        self.webShutterUI.startStopButton.clicked.connect(self.startStopButtonClicked)


    def searchButtonClicked(self):
        #comboBox = self.webShutterUI.filterCombo;
        #searchText = self.webShutterUI.searchLine.text()
        #filterBy = comboBox.currentText()
        # implement search

        #self.webShutterUI.tableWidget.getCheckedRowItems()
        print("darwin")

    def checkboxAllClicked(self):
        return 0


    def deleteButtonClicked(self):
        items = self.webShutterUI.tableWidget.getRowItems()

        removeCount = 0
        for item in items:
            if item.isSelected():
                id = item.getItem().dbId
                self.__deleteItemFromDatabase(id)
                self.webShutterUI.tableWidget.removeRow(item.getRow() - removeCount)
                removeCount = removeCount + 1
            else:
                item.setRow(item.getRow() - removeCount) #move the row, record the new index

    def addButtonClicked(self):

        links = self.webShutterUI.tableWidget.rowInput.linkInput.toPlainText()
        linkList = re.split("\s+", links)

        for link in linkList:
            item = Item(-1, link, Status.PENDING, True)
            id = self.__addItemToDatabase(item)
            if id > 0:
                item.dbId = id
            tableRowItem = TableWidgetRowItem(item)
            self.webShutterUI.tableWidget.addRowItem(tableRowItem)

        self.webShutterUI.tableWidget.rowInput.linkInput.setText("")

    def startStopButtonClicked(self):
        checkedRowItems = self.webShutterUI.tableWidget.getCheckedRowItems()
        args = self.getGeneralArgs()

        for item in checkedRowItems:
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
            thread.toProcessCallback.connect(self.updateRowStatus)

            self.__threads.append(thread)

        #spawn a new thread to start the threads
        startThread = Thread(target=self.__startThreads)
        startThread.start()


    #START - callback methods for the thread

    def updateRowStatus(self, rowItem, status):
        rowItem.setStatus(status)

    def finishThreading(self, rowItem, status):
        self.updateRowStatus(rowItem, status)
        self.__numThreads -= 1

        #
        #update database
        self.__updateItemToDatabase(rowItem.getItem())

    #END - callback methods for the thread

    def darwin(self):
        return 0

    def getGeneralArgs(self):

        #get the settings here
        size = { "width": 1024, "height" : 960} # define on the settings
        path = "D:\\DarwinFiles\\Work\\Projects\\webshutter\\test\\save"
        #path = "/home/darwin/Projects/Python/webshutter/test/save"

        sizeArgs = "--size=" + str(size['width']) + "x" + str(size['height'])
        deviceArgs = "--desktop"
        pathArgs = "--output" + path

        args = { "size": sizeArgs, "device": deviceArgs, "path": pathArgs,
            "casperJS": Config.CASPERJS_PATH, "screenshotScript": Config.SCREENSHOT_SCRIPT_PATH
        }

        return args

    def __startThreads(self):
        #start threading
        self.__toRun = True

        while len(self.__threads) > 0 and self.__toRun:
            if self.__numThreads < Config.MAX_THREADS:
                self.__numThreads += 1
                thread = self.__threads.popleft()
                thread.start()
            time.sleep(1)

    def __addItemToDatabase(self,item):
        sql = "INSERT INTO urls(url, status, status_label, is_checked) VALUES(?, ?, ?, ?)"
        params = (item.link, item.status, Status.State[item.status], item.isChecked)
        return self.__databaseConnection.insert(sql, params)

    def __deleteItemFromDatabase(self, id):
        sql = "DELETE FROM urls WHERE id = ?"
        params = (id,)
        self.__databaseConnection.delete(sql, params)

    def __updateItemToDatabase(self, item):
        sql = "UPDATE urls SET status = ?, status_label = ? where id = ?"
        params = (item.status, Status.State[item.status], item.dbId)
        self.__databaseConnection.update(sql, params)
