import os
from config import path

os.chdir(f"{path}")
system = 1
if system == 1:
    os.system("run.bat")
elif system == 2:
    os.system("run.bat")
else:
    raise Exception("Unknown system!")