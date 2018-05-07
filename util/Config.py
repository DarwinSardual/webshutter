import os

class Config:

    CURRENT_DIR = os.getcwd()
    PYTHON_PATH = "";
    #PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts\\phantomjs\\bin\\phantomjs.exe")
    #CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts\\casperjs\\bin\\casperjs")
    #SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts\\capture.js")
    
    PHANTOMJS_EXECUTABLE = os.path.join(CURRENT_DIR, "scripts/phantomjs/bin/")
    CASPERJS_PATH = os.path.join(CURRENT_DIR, "scripts/casperjs/bin/casperjs")
    SCREENSHOT_SCRIPT_PATH = os.path.join(CURRENT_DIR, "scripts/capture.js")
    
    IMAGE_EXT =".png"
    OUTPUT_ROOT_DIR = os.path.join(CURRENT_DIR, "save")
    MAX_THREADS = 5

    ENV = PHANTOMJS_EXECUTABLE
