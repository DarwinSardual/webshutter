import sys, os
from PySide import QtCore, QtGui
from app.ui.app_controller import AppController

from app.action.shutter import Shutter
from app.data.config import Config
from app.data.urls import Url, Status
from app.util.db import SqliteCon
from enum import Enum

def clickedfunc():
	print "clicked"

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    main = AppController(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())