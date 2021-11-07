# Event Handlers ======================================================================

import win32com.client
import novel

class NktSpyMgrEvents:

    def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):
        nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
        skiString = nktHookCallInfo.Params().GetAt(3)
        new_text = str(skiString)
        if (novel.used_text != new_text):
            text_to_write = novel.parse_text(new_text)
            novel.skinovel.write("%s \n" %(text_to_write))
        novel.used_text = str(new_text)
        novel.words += 1000