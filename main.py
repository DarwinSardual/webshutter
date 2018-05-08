import sys, os
from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.join(os.getcwd(), "prefs"))
sys.path.append(os.path.join(os.getcwd(), "main"))
sys.path.append(os.path.join(os.getcwd(), "table"))
sys.path.append(os.path.join(os.getcwd(), "util"))

from WebShutterUIController import WebShutterUIController

class Main:
    def run(self):
        webShutterUIController = WebShutterUIController()
        return webShutterUIController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    webShutterMain = ui.run()
    sys.exit(app.exec_())
