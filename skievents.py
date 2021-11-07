# Event Handlers ======================================================================

import win32com.client
import novel
import novelvars

class NktSpyMgrEvents:

    def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):
        nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
        skiString = nktHookCallInfo.Params().GetAt(3)
        if novelvars.sentences > 4: # no flavor text before we get the intro in
            novel.print_flavor_text()
        new_text = str(skiString)
        if (novelvars.used_text != new_text):
            text_to_write = novel.parse_text(new_text)
            novel.write_text(text_to_write)
        novelvars.used_text = str(new_text)
        print("Sentences: %s; Words: %s" %(str(novelvars.sentences), str(novelvars.words)))