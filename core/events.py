import wx
import wx.lib.newevent
from logger import log

class Events(object):    
    MediaStateChanged, EVT_MEDIA_STATE_CHANGED = wx.lib.newevent.NewCommandEvent()

    def post_event(self, event, target=None):
        if getattr(self, 'app', None):
            if not target:
                target = self.app.GetTopWindow().get_plugin()
            log.debug("posting event %s %s", event, target)
            wx.PostEvent(target, event)
