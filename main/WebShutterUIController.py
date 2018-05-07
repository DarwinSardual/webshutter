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
        
        self.__setupTable()
        

    def __initSignals(self):
        self.webShutterUI.tableWidget.rowInput.addButton.clicked.connect(self.addButtonClicked)
        self.webShutterUI.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.webShutterUI.searchButton.clicked.connect(self.searchButtonClicked)
        self.webShutterUI.startStopButton.clicked.connect(self.startStopButtonClicked)
        
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

        links = self.webShutterUI.tableWidget.rowInput.linkInput.toPlainText()
        linkList = re.split("\s+", links)

        for link in linkList:
            item = Item(-1, link, Status.PENDING, True)
            id = self.__addItemToDatabase(item)
            if id > 0:
                item.dbId = id
            rowItem = TableWidgetRowItem(item)
            self.webShutterUI.tableWidget.addRowItem(rowItem)
            rowItem.setToggleCallback(self.__toggleCheckbox)

        self.webShutterUI.tableWidget.rowInput.linkInput.setText("")

    def startStopButtonClicked(self):
        checkedRowItems = self.webShutterUI.tableWidget.getCheckedRowItems()
        print(checkedRowItems)
        
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
            thread.toProcessCallback.connect(self.updateRowItem)

            self.__threads.append(thread)

        #spawn a new thread to start the threads
        startThread = Thread(target=self.__startThreads)
        startThread.start()
        

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

        while len(self.__threads) > 0 and self.__toRun:
            if self.__numThreads < Config.MAX_THREADS:
                self.__numThreads += 1
                thread = self.__threads.popleft()
                thread.start()
            time.sleep(1)
        

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
