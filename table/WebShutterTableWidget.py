from PyQt5.QtWidgets import QTableWidget, QHeaderView, QCheckBox
from table.TableWidgetRowInput import TableWidgetRowInput
from PyQt5.QtCore import Qt

class WebShutterTableWidget(QTableWidget):

    def __init__(self):
        self.super = super(WebShutterTableWidget, self)
        self.super.__init__()
        self.__setGui()

        self.__rowItems = [] # TableWidgetRowItem
        self.__checkedItems = [] # Reference to the checked items
        #self.__rowItems = {}
        #self.__checkedItems = {}
        self.__numCheck = 0

        self.rowInput = None
        self.isInputInitialized = False

        self.__addInput()
        
        self.__checkboxAll.clicked.connect(self.__checkboxAllStateChanged)

    def __setGui(self):
        self.__checkboxAll = QCheckBox()

        self.__setInitialRowAndColumn()
        self.__setHeaderTitles()


    def __setInitialRowAndColumn(self):
        self.super.setRowCount(1)
        self.super.setColumnCount(3)

    def __setHeaderTitles(self):
        titleHeader = self.super.horizontalHeader()
        numberHeader = self.super.verticalHeader()

        header = self.horizontalHeader()
        self.__checkboxAll.setParent(header)
        self.__checkboxAll.setGeometry(14, 3, 17, 17) # Position the checkbox

        titleHeader.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        titleHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        titleHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        headerTitles = ["", "Link", "Status"]
        self.super.setHorizontalHeaderLabels(headerTitles)

    def addRowItem(self, rowItem):
        rowIndex = self.super.rowCount() - 1
        self.super.insertRow(rowIndex)

        rowItem.setRow(rowIndex)
        self.super.setCellWidget(rowIndex, 0, rowItem.checkBox)
        self.super.setItem(rowIndex, 1, rowItem.linkInput)
        self.super.setItem(rowIndex, 2, rowItem.statusInput)

        self.__rowItems.append(rowItem)
        #self.__rowItems[str(rowItem.getItem().dbId)] = rowItem
        #self.__checkedItems[str(rowItem.getItem().dbId)] = rowItem
        self.__numCheck += 1
        rowItem.setToggleCallback(self.__toggleCheckbox)
        
        self.__checkboxAll.setCheckState(Qt.Checked) if  self.__numCheck == len(self.__rowItems) else self.__checkboxAll.setCheckState(Qt.Unchecked)


        #self.__rowItems.append(rowItem)
        #self.__checkedItems.append(rowItem) # Add reference to the checked items

    def deleteCheckedItems(self):
        items = self.__rowItems

        removeCount = 0
        remainingItems = []
        deletedItems = []
        for item in items:
            if item.isSelected():
                id = item.getItem().dbId
                self.super.removeRow(item.getRow() - removeCount)
                removeCount = removeCount + 1
                deletedItems.append(item)
                
            else:
                item.setRow(item.getRow() - removeCount) #move the row, record the new index
                remainingItems.append(item)
            
        
        items[:] = remainingItems
        return deletedItems
    
    def checkAllItems(self, isChecked):
        for item in self.__rowItems:
            print(item.getItem().link)
            item.setChecked(isChecked)
    
    def clearTable(self):
        while self.super.rowCount() > 1:
            self.super.removeRow(0)
        

    #getters

    def getRowItems(self):
        return self.__rowItems

    def getCheckedRowItems(self):
        # implement basic searchLine
        checkedRowItems = []
        for item in self.__rowItems:
            if item.checkBox.checkState() == Qt.Checked:
                checkedRowItems.append(item)

        return checkedRowItems
        #return self.__checkedItems

    def __toggleCheckbox(self, status):
        if status:
            self.__numCheck += 1
        else:
            self.__numCheck -= 1

        
        self.__checkboxAll.setCheckState(Qt.Checked) if  self.__numCheck == len(self.__rowItems) else self.__checkboxAll.setCheckState(Qt.Unchecked)
        #item = rowItem.getItem()
        #if(not item.isChecked):
        #    del self.__checkedItems[str(item.dbId)]
        #else:
        #    self.__checkedItems[str(item.dbId)] = rowItem



    def __addInput(self): # only call this once on table init
        if self.isInputInitialized == True:
            return

        self.rowInput = TableWidgetRowInput()

        self.super.setCellWidget(0, 1, self.rowInput.linkInput)
        self.super.setCellWidget(0, 2, self.rowInput.addButton)
        self.super.setSpan(0, 0, 1, 2)
        self.isInputInitialized = True

    def __checkboxAllStateChanged(self):
        
        value = True if self.__checkboxAll.checkState() == Qt.Checked else False
        self.checkAllItems(value)
        #print(value)    
        
