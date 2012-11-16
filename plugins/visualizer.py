import wx
from gui.plugintypes import ContentPlugin
import time
from api import API

# must be named panel
class Panel(ContentPlugin):
    def __init__(self, parent):
        ContentPlugin.__init__(self, parent)
        self.title = "Visualize"

        if API.config.opengl:
            import gui.opengl as opengl
            self.visualizer = opengl.VizCanvas(self.content)
        else:
            import gui.slideshow as slideshow
            self.visualizer = slideshow.SlideCanvas(self.content, self)
        
        # setup the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.visualizer, 1, flag=wx.EXPAND)
        self.content.SetSizer(sizer)
        self.content.Fit()

    def handle_key(self, accel, key):
        norm = wx.ACCEL_NORMAL
        shift = wx.ACCEL_SHIFT
        
        if (accel, key) == (norm, wx.WXK_ESCAPE):
            self.visualizer.set_next_vis()

        raise NotImplementedError
