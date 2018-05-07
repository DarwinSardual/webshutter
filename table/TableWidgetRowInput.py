from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QTextEdit, QWidget
from PyQt5.QtGui import QIcon
import os

class TableWidgetRowInput:
    def __init__(self):
        #self.layout = QHBoxLayout()
        #self.layout.setContentsMargins(0, 0, 0, 0)

        self.linkInput = QTextEdit()
        self.addButton = QPushButton()
        
        dirname = os.path.dirname(os.path.abspath(__file__))
        addIconPath = os.path.join(dirname, "../images/add.svg")
        addButtonIcon = QIcon(addIconPath)
        self.addButton.setIcon(addButtonIcon)
        
        #self.clear = QPushButton("Clear")

        #self.layout.addWidget(self.add)
        #self.layout.addWidget(self.clear)

        #self.actionsWidget = QWidget()
        #self.actionsWidget.setLayout(self.layout)
