import json
from PreferencesUI import PreferencesUI
from Config import Config

class PreferencesUIController:

    def __init__(self):

        self.preferencesUI = PreferencesUI()
        self.pref = Config.getConfig()
        self.__initValues()
        self.__initSignals()

        self.preferencesUI.exec_()

    def __initValues(self):
        self.preferencesUI.widthLine.setText(str(self.pref["dimensions"]["width"]))
        self.preferencesUI.heightLine.setText(str(self.pref["dimensions"]["height"]))

        if self.pref["mode"] == "mobile":
            self.preferencesUI.mobileRadioButton.setChecked(True)
            self.mode = self.pref["mode"]
        else:
            self.preferencesUI.desktopRadioButton.setChecked(True)
            self.mode = "desktop" #fail safe in case the json file has been modified

    def __initSignals(self):
        self.preferencesUI.saveButton.clicked.connect(self.saveButtonClicked)
        self.preferencesUI.cancelButton.clicked.connect(self.preferencesUI.close)
        self.preferencesUI.mobileRadioButton.toggled.connect(lambda: self.modeToggled(self.preferencesUI.mobileRadioButton))
        self.preferencesUI.desktopRadioButton.toggled.connect(lambda: self.modeToggled(self.preferencesUI.desktopRadioButton))

    def saveButtonClicked(self):
        newPref = {}
        newPref["dimensions"] = {}

        newPref["dimensions"]["width"] = int(self.preferencesUI.widthLine.text())
        newPref["dimensions"]["height"] = int(self.preferencesUI.heightLine.text())

        newPref["mode"] = self.mode

        Config.createPreferencesConfig(newPref)
        self.preferencesUI.close()


    def modeToggled(self, button):

        if button == self.preferencesUI.mobileRadioButton:
            if button.isChecked():
                self.mode = "mobile"
        else:
            self.mode = "desktop"
