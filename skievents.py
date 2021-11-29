# Event Handlers ======================================================================

import win32com.client
import novel
import novelvars

class NktSpyMgrEvents:

    def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):
        nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
        skiString = nktHookCallInfo.Params().GetAt(3) # get param #4 of TextOutA: lpString
        if novelvars.sentences > 8: # no flavor text before we get the intro in
            novel.print_flavor_text()
        new_text = str(skiString)
        if (novelvars.used_text != new_text):
            text_to_write = novel.parse_text(new_text)
            novel.write_text(text_to_write)
        if novelvars.post_ski:
            novel.print_yeti_text()
        novelvars.used_text = str(new_text)
        print("Words: %s" %(str(novelvars.words)))