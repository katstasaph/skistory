# Main ==================================================================

import win32com.client
import ctypes, sys
import novelvars

from skievents import NktSpyMgrEvents
from skifunctions import *

if sys.version_info.major < 3:
    warnings.warn("Need Python 3.0 for this program to run", RuntimeWarning)
    sys.exit(0)

win32com.client.pythoncom.CoInitialize()
spyManager = win32com.client.DispatchWithEvents("DeviareCOM.NktSpyMgr", NktSpyMgrEvents)
result = spyManager.Initialize()

if not result == 0:
    print("ERROR: Could not initialize the SpyManager. Error code: %d" % (result))
    sys.exit(0)

skifree = runAndHookSkiFree(spyManager)

MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox(None, "Placeholder, this will ideally exit when we have 50,000.", "SkiHook", 0)

novelvars.skinovel.close()
novelvars.flavor_text.close()
skifree.Terminate(0)

