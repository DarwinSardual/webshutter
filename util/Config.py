import os, json
from json import JSONDecodeError
from pathlib import Path

class Config:

    CURRENT_DIR = os.getcwd()
    PYTHON_PATH = "";
    PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts\\phantomjs\\bin\\phantomjs.exe")
    CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts\\casperjs\\bin\\casperjs")
    #SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts\\capture.js")
    
    PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts/phantomjs/bin/")
    CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts/casperjs/bin/casperjs")
    SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts/capture.js")
    
    IMAGE_EXT =".png"
    OUTPUT_ROOT_DIR = os.path.join(CURRENT_DIR, "save")
    MAX_THREADS = 5

    ENV = PHANTOMJS_EXECUTABLE
    
    PREF_DEFAULT = {"mode": "desktop", "dimensions":{"width": 1024, "height": 960}}

    
    @staticmethod
    def checkPreferencesConfig():
        dirname = os.path.dirname(os.path.abspath(__file__))
        prefPath = os.path.join(dirname, "../prefs/preferences.json")
        
        return os.path.isfile(prefPath)
    
    @staticmethod
    def createPreferencesConfig(pref = False):
        dirname = os.path.dirname(os.path.abspath(__file__))
        prefPath = os.path.join(dirname, "../prefs/preferences.json")
        
        if not pref:
            pref = Config.PREF_DEFAULT
        
        prefFile = open(prefPath, "w")
        prefFile.write(json.dumps(pref))
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
                    return False
                #else everything is correct
            else:
                return False
        except (JSONDecodeError, ValueError, KeyError):
            return False
        
        return True
            
    @staticmethod
    def getConfig():
        dirname = os.path.dirname(os.path.abspath(__file__))
        prefPath = os.path.join(dirname, "../prefs/preferences.json")
            
        prefFile = open(prefPath, "r")
        pref = json.loads(prefFile.read())
            
        prefFile.close()
        return pref
        
    
