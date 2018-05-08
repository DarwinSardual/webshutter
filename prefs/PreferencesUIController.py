import json
from PreferencesUI import PreferencesUI
from Config import Config

class PreferencesUIController:
    
    def __init__(self):
        self.preferencesUI = PreferencesUI()
        #fl = open("preferences", "r")
        
        try:
            self.prefFile = open("preferences.json", "r+")
        except FileNotFoundError:
            self.prefFile = open("preferences.json", "w")
            self.prefFile.close()
            
            self.prefFile = open("preferences.json", "r+")
            self.prefFile.write(json.dumps(Config.PREF_DEFAULT))
            
        
