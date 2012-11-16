import wx
import gui.pluginutils as utils
from gui.itemlist import ItemList

class BasePlugin(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.frame = wx.GetApp().GetTopWindow()

    def handle_key(self, accel, key):
        raise NotImplementedError

    def attach_gestures(self, obj, mg):
        # handle this object with mouse handler
        obj.Bind(wx.EVT_MOUSE_EVENTS, mg.OnMouseEvent)
        obj.Bind(wx.EVT_MOTION, mg.OnMotion)

        # recurse through children
        for child in obj.Children:
            self.attach_gestures(child, mg)

class ContentPlugin(BasePlugin):
    def __init__(self, parent):
        BasePlugin.__init__(self, parent)

        gradient_percent = 0.35

        # one main area called content
        self.content = utils.GradientPanel(self, percent=gradient_percent)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.content, 100, flag=wx.EXPAND)
        self.SetSizer(hsizer)
        utils.setColours(self)

class ListboxPlugin(BasePlugin):
    def __init__(self, parent):
        BasePlugin.__init__(self, parent)

        # choices panel simply holds listbox
        self.listbox = ItemList(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.listbox, 100, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Layout()
