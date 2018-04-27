import sys
from PyQt5.QtWidgets import QApplication
from main.WebShutterUIController import WebShutterUIController

class Main:
    def run(self):
        webShutterUIController = WebShutterUIController()
        return webShutterUIController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    webShutterMain = ui.run()
    sys.exit(app.exec_())
