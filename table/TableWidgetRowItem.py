from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QWidget
from util.Status import Status

class TableWidgetRowItem:

    CHECKBOX = 0
    LINK = 1
    STATUS = 2

    def __init__(self, item):
        self.__item = item

        self.checkBox = QCheckBox()
        self.checkBox.setStyleSheet("margin-left: 14px")
        self.setSelected(item.isChecked)

        self.linkInput = QTableWidgetItem(item.link)
        self.statusInput = QTableWidgetItem(Status.State[item.status])
        self.table = None
        self.__toggleCallback

        self.__setAlignment()
        self.__setFlags()
        self.__initSignals()

    def __setAlignment(self):
        self.linkInput.setTextAlignment(Qt.AlignCenter)
        self.statusInput.setTextAlignment(Qt.AlignCenter)


    def __setFlags(self):
        #self.rowNumber.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.statusInput.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

    def __initSignals(self):
        self.checkBox.stateChanged.connect(self.__stateChanged)

    #SETTERS

    def setSelected(self, isSelected):
        if isSelected == True:
            self.checkBox.setCheckState(Qt.Checked)
        else:
            self.checkBox.setCheckState(Qt.Unchecked)

        self.__item.isChecked = isSelected #a little bit of redundant at initialization

    def setLink(self, link):
        self.__item.link = link
        self.linkInput.setText(link)

    def setStatus(self, status):
        self.__item.status = status
        self.statusInput.setText(Status.State[status])
        #

    def setRow(self, row):
        self.__row = row

    def isSelected(self):
        return self.__item.isChecked

    #GETTERS
    # write getters here

    def getRow(self):
        return self.__row

    def getItem(self):
        return self.__item

    #def setTable(self, table): #backup method in case we need reference to the table
        #self.table = table

    # Callbacks

    def setToggleCallback(self, callback):
        return 0

    #Signals

    def __stateChanged(self, state):
        if(state == Qt.Checked):
            self.setSelected(True)
        else:
            self.setSelected(False)

    self.__toggleCallback && self.__toggleCallback()
