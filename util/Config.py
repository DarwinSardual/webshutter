import os, json
from json import JSONDecodeError
from pathlib import Path

class Config:

    CURRENT_DIR = os.getcwd()
    PYTHON_PATH = "";
    PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts\\phantomjs\\bin\\phantomjs.exe")
    #CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts\\casperjs\\bin\\casperjs")
    #SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts\\capture.js")
    
    #PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts/phantomjs/bin/")
    CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts/casperjs/bin/casperjs")
    SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts/capture.js")
    
    IMAGE_EXT =".png"
    OUTPUT_ROOT_DIR = os.path.join(CURRENT_DIR, "save")
    MAX_THREADS = 5

    ENV = PHANTOMJS_EXECUTABLE
    
    PREF_DEFAULT = {"dimensions":{"width": 1024, "height": 960}, "mode": "desktop"}

    
    @staticmethod
    def checkPreferencesConfig():
        dirname = os.path.dirname(os.path.abspath(__file__))
        prefPath = os.path.join(dirname, "../prefs/preferences.json")
        
        return os.path.isfile(prefPath)
    
    @staticmethod
    def createPreferencesConfig():
        dirname = os.path.dirname(os.path.abspath(__file__))
        prefPath = os.path.join(dirname, "../prefs/preferences.json")
        
        prefFile = open(prefPath, "w")
        prefFile.write(json.dumps(Config.PREF_DEFAULT))
        prefFile.close()
    
    @staticmethod
    def checkPreferencesConfigFormat():
        dirname = os.path.dirname(os.path.abspath(__file__))
        prefPath = os.path.join(dirname, "../prefs/preferences.json")
        prefFile = open(prefPath, "r")

        try:
            pref = json.loads(prefFile.read())
                
            # Check the keys first
            pref["dimensions"]
            pref["dimensions"]["width"]
            pref["dimensions"]["height"]
            pref["mode"]
                
            # Then check the type of the values
                
            int(pref["dimensions"]["width"])
            int(pref["dimensions"]["height"])
                
            if isinstance(pref["mode"], str):
                if not (pref["mode"] == "desktop" or pref["mode"] == "mobile"):
                    Config.createPreferencesConfig()
                #else everything is correct
            else:
                Config.createPreferencesConfig()
        except (JSONDecodeError, ValueError, KeyError):
            Config.createPreferencesConfig()
