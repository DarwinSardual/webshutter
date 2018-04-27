import sys, os
from cx_Freeze import setup, Executable

cur_dir = os.getcwd()
sys.path.append(os.path.join(cur_dir, "app/util"))
sys.path.append(os.path.join(cur_dir, "app/data"))
sys.path.append(os.path.join(cur_dir, "app/action"))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "include_files": ["scripts"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "webshutter",
        version = "0.1",
        description = "Web Shutter",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])