import os, json
from json import JSONDecodeError
from pathlib import Path

from Dimension import Dimension

class Config:

    CURRENT_DIR = os.getcwd()
    PYTHON_PATH = "";
    PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts\\phantomjs\\bin\\phantomjs.exe")
    CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts\\casperjs\\bin\\casperjs")
    SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts\\capture.js")

    IMAGE_EXT =".png"
    OUTPUT_ROOT_DIR = os.path.join(CURRENT_DIR, "save")
    LOG_FILE = os.path.join(CURRENT_DIR, "log.txt")
    MAX_THREADS = 5

    ENV = PHANTOMJS_EXECUTABLE

    PREF_DEFAULT = {"mode": "desktop", "dimensions":{"width": 1280, "height": 720}}


    @staticmethod
    def createLogFile():
        if not os.path.isfile(Config.LOG_FILE):
            f = open("log.txt", "w")
            f.close()

    @staticmethod
    def createSaveDirectory():
        if not os.path.isdir(Config.OUTPUT_ROOT_DIR):
            os.makedirs(Config.OUTPUT_ROOT_DIR)

    @staticmethod
    def checkPreferencesConfig():
        prefPath = "preferences.json"

        return os.path.isfile(prefPath)

    @staticmethod
    def createPreferencesConfig(pref = False):
        prefPath = "preferences.json"

        if not pref:
            pref = Config.PREF_DEFAULT

        prefFile = open(prefPath, "w")
        prefFile.write(json.dumps(pref))
        prefFile.close()

    @staticmethod
    def checkPreferencesConfigFormat():
        prefPath = "preferences.json"
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

            isDimensionFound = False
            for dimension in Dimension.Value:
                if pref["dimensions"]["width"] == dimension["width"] and pref["dimensions"]["height"] == dimension["height"]:
                    isDimensionFound = True

            if not isDimensionFound:
                return False

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

        prefPath = "preferences.json"

        prefFile = open(prefPath, "r")
        pref = json.loads(prefFile.read())

        prefFile.close()
        return pref
