import threading, time, os, subprocess
from util.Config import Config
from util.Status import Status
from PyQt5 import QtCore

class WebShutterThread(QtCore.QThread):

    finishCallback = QtCore.pyqtSignal(object, object)
    toProcessCallback = QtCore.pyqtSignal(object, object, object)

    def __init__(self, command, rowItem):
        self.super = super(WebShutterThread, self)
        self.super.__init__()
        self.command = command
        self.rowItem = rowItem


    def run(self):
        self.toProcessCallback.emit(self.rowItem, Status.IN_PROCESS, False)
        os.environ["PHANTOMJS_EXECUTABLE"] = str(Config.ENV)
        #os.environ["PATH"] += os.pathsep + str(Config.ENV)
        p = subprocess.Popen(self.command, env=os.environ, stdout=subprocess.PIPE, shell=True)

        while True:
            line = p.stdout.readline()
            if not line:
                break
            else:
                print(line)
                
        self.finishCallback.emit(self.rowItem, Status.COMPLETED)
