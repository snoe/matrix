import wx
import wx.lib.mixins.listctrl as listmix
import gui.pluginutils as utils
from api import API
from sources import covers

class ItemList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL):
        wx.ListCtrl.__init__(self, parent, ID, style=style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        font = self.GetFont()
        font.SetPointSize(API.config.fontsize)
        self.SetFont(font)
        self.InsertColumn(0, "First")
                
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("black")
        font.SetPointSize(API.config.fontsize)
        self.attr1.SetFont(font)
        
        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("black")
        font.SetPointSize(API.config.fontsize - 10)
        self.attr2.SetFont(font)

        # set up image list and default
        icon_size = [API.config.fontsize]*2
        self.lst = wx.ImageList(*icon_size)
        self.default_idx = self.lst.Add(wx.EmptyImage(*icon_size).ConvertToBitmap())

        # index our covers
        self.artcache = covers.cache_covers(API.config.mp3path, icon_size)
        self.idx_cache = {}
        for key, bmp in self.artcache.items():
            self.idx_cache[key] = self.lst.Add(bmp)

        self.SetImageList(self.lst, wx.IMAGE_LIST_SMALL)
        utils.setColours(self, foreground="white")

    def set_items(self, items, idx=0):
        self.items = items
        self.SetItemCount(len(items))
        self.Select(idx, True)
        self.Focus(idx)
        self.Refresh()

    def GetItemData(self, row, idx):
        return self.items[row][idx]
        
    def OnGetItemText(self, row, col):
        return self.items[row][0]

    def OnGetItemImage(self, row):
        if row != self.GetFirstSelected():
            return -1
        key = self.items[row][2]
        if key in self.idx_cache:
            return self.idx_cache[key]
        else:
            return -1
            
    def OnGetItemAttr(self, item):
       if item == self.GetFirstSelected():
           return self.attr1
       else:
           return self.attr2

    def move(self, amount):
        current = self.GetFirstSelected()
        i = self.GetFirstSelected() + int(amount)
        next = i % len(self.items)

        self.select(next)
        
    def select(self, i):
        self.Focus(i)
        self.Select(i)

        # hack because the refresh doesn't happen correctly when wrapping
        self.Focus(i)
        self.Select(i)
        self.Refresh()
