import sys

def GetPIDByProcessName(aProcessName):
    for proc in psutil.process_iter():
        if proc.name == aProcessName:
            return proc.pid

def openSkiFree(spyManager):
    skiFreePath = "skifree.exe"
    skifree, continueEvent = spyManager.CreateProcess(skiFreePath, True)
    if skifree is None:
        print("Cannot launch SkiFree")
        sys.exit(0)
    return skifree, continueEvent


def HookFunctionForProcess(spyManager, functionModuleAndName, skifreePID):
    hook = spyManager.CreateHook(functionModuleAndName, 0)
    hook.Attach(skifreePID, True)
    hook.Hook(True)
    return hook


def runAndHookSkiFree(spyManager):
    skifree, continueEvent = openSkiFree(spyManager)
    hook = HookFunctionForProcess(spyManager, "Gdi32.dll!TextOutA", skifree.Id)
    spyManager.ResumeProcess(skifree, continueEvent)
    return skifree
