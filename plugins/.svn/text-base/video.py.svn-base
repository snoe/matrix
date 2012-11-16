import wx
from gui.plugintypes import ListboxPlugin
from lib.path import path
from api import API

# must be named panel
class Panel(ListboxPlugin):
    def __init__(self, parent):
        ListboxPlugin.__init__(self, parent)
        self.titles = ["Video"]

        root = path('/Users/snoe/media/video')
        self.current = root
        self.items = self.get_items(root)
        self.listbox.Bind(wx.EVT_LEFT_UP, self.on_click)
        self.listbox.set_items(self.items)

    def get_items(self, folder):
        items = []
        for f in folder.listdir():
            if f.name.startswith('.'):
                continue
            label = f.name
            data = f
            items.append((label, data, None))
        return items

    def on_click(self, event):
        self.on_enter(self.listbox.GetFirstSelected())
        event.Skip()

    def on_enter(self, i):
        label, data, artfile = self.items[i]
        if data.isdir():
            self.titles.insert(0, label)
            self.current = data
            self.items = self.get_items(data)
            self.listbox.set_items(self.items)
        else:
            API.media.load_track_and_playlist(i,self.listbox.items,API.media.TYPE_VIDEO)
            self.frame.set_plugin(0)

    def on_back(self):
        self.titles = self.titles[1:]
        self.current = self.current.parent
        self.items = self.get_items(self.current)
        self.listbox.set_items(self.items)
            
    def handle_key(self, accel, key):
        norm = wx.ACCEL_NORMAL
        shift = wx.ACCEL_SHIFT
        
        if (accel, key) == (norm, wx.WXK_ESCAPE):
            self.on_back()
            
        elif (accel, key) == (norm, wx.WXK_RETURN):
            self.on_enter(self.listbox.GetFirstSelected())

        elif (accel, key) == (norm, wx.WXK_RIGHT):
            self.listbox.move(1)
            
        elif (accel, key) == (norm, wx.WXK_LEFT):
            self.listbox.move(-1)
            
        else:
            raise NotImplementedError

