#
# Copyright (C) 2010-2015 Nektra S.A., Buenos Aires, Argentina.
# All rights reserved. Contact: http://www.nektra.com
#
#
# This file is part of Deviare
#
#
# Commercial License Usage
# ------------------------
# Licensees holding valid commercial Deviare licenses may use this file
# in accordance with the commercial license agreement provided with the
# Software or, alternatively, in accordance with the terms contained in
# a written agreement between you and Nektra.  For licensing terms and
# conditions see http://www.nektra.com/licensing/. Use the contact form
# at http://www.nektra.com/contact/ for further information.
#
#
# GNU General Public License Usage
# --------------------------------
# Alternatively, this file may be used under the terms of the GNU General
# Public License version 3.0 as published by the Free Software Foundation
# and appearing in the file LICENSE.GPL included in the packaging of this
# file.  Please visit http://www.gnu.org/copyleft/gpl.html and review the
# information to ensure the GNU General Public License version 3.0
# requirements will be met.
#
#

# Auxiliar Functions =====================================================================

from subprocess import *
import os, sys


def GetPIDByProcessName(aProcessName):
    for proc in psutil.process_iter():
        if proc.name == aProcessName:
            return proc.pid

def openSkiFree(spyManager):
    print("Starting SkiFree...")
    skiFreePath = "skifree.exe"
    skifree, continueEvent = spyManager.CreateProcess(skiFreePath, True)
    if skifree is None:
        print("Cannot launch SkiFree")
        sys.exit(0)
    return skifree, continueEvent


def HookFunctionForProcess(spyManager, functionModuleAndName, skifreePID):
    print("Hooking function " + functionModuleAndName + " for SkiFree...")
    hook = spyManager.CreateHook(functionModuleAndName, 0)
    hook.Attach(skifreePID, True)
    hook.Hook(True)
    print("Notepad successfully hooked")
    return hook


def runAndHookSkiFree(spyManager):
    skifree, continueEvent = openSkiFree(spyManager)
    hook = HookFunctionForProcess(spyManager, "Gdi32.dll!TextOutA", skifree.Id)
    spyManager.ResumeProcess(skifree, continueEvent)
    return skifree
