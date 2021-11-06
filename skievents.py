# Event Handlers ======================================================================

import win32com.client
import novel

class NktSpyMgrEvents:

    def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):
        nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
        paramsEnum = nktHookCallInfo.Params().GetAt(3)
        new_text = str(paramsEnum)
        if (novel.used_text != new_text):
            novel.skinovel.write("And then: %s \n" %(new_text))
        novel.used_text = str(new_text)
        novel.words += 1000


