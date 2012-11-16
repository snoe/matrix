import wx
from lib.path import path
import cStringIO
from api import API

class SlideCanvas(wx.Panel):
    def __init__(self, parent, plugin):
        wx.Panel.__init__(self, parent, -1)
        self.art = wx.StaticBitmap(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.art, flag=wx.ALIGN_CENTER_HORIZONTAL)
        sizer.AddStretchSpacer()
        self.SetSizer(sizer)

        self.plugin = plugin
        
        self.slidepath = API.config.slidepath
        self.images = path(self.slidepath).walkfiles("*.jpg")
        self.set_next_vis()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(10000)

    def get_next_image(self):
        try:
            next = self.images.next()
        except StopIteration:
            self.images = path(self.slidepath).walkfiles("*.jpg")
            next = self.images.next()
        return next

    def set_next_vis(self):
        
        try:
            data = open(self.get_next_image(), "rb").read()
            stream = cStringIO.StringIO(data)
        
            bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
            self.art.SetBitmap(bmp)
            self.art.SetSize(bmp.Size)
            self.Sizer.Layout()
        except StopIteration:
            pass
            
        self.Refresh()

    def OnTimer(self, e):
        if self.plugin.frame.get_plugin() == self.plugin:
            self.set_next_vis()
                                        
