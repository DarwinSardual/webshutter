import sys, os
from cx_Freeze import setup, Executable

sys.path.append(os.path.join(os.getcwd(), "prefs"))
sys.path.append(os.path.join(os.getcwd(), "main"))
sys.path.append(os.path.join(os.getcwd(), "table"))
sys.path.append(os.path.join(os.getcwd(), "util"))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "include_files": ["scripts", "images"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "webshutter",
        version = "2.0",
        description = "Web Shutter",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
