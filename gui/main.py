import wx
import NotebookCtrl as nbc
import gui.titlepanel
import gui.mediaplayer
import loader
from api import API

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(640, 480), style=wx.NO_BORDER)
        self.PLUGINS = ["audio", "video", "visualizer", "gps_plugin"]
        
        if API.config.fullscreen:
            self.ShowFullScreen(True)
            self.SetPosition((0, 0))
            self.SetInitialSize(wx.DisplaySize())
        else:
            self.SetPosition((50, 50))

        self.title = gui.titlepanel.TitlePanel(self)
        self.plugintitles = {}

        self.panel = nbc.NotebookCtrl(self,-1)
        self.panel.SetBackgroundColour(wx.BLACK)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.title, 15,  wx.EXPAND)
        self.sizer.Add(self.panel, 85,  wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sizer.Layout()

        self.mediaplayer = gui.mediaplayer.MediaPlayer(self.panel)
        self.panel.AddPage(self.mediaplayer, "")
        
        for i, plugin in enumerate(self.PLUGINS):
            self.panel.AddPage(loader.getPlugin(plugin, self.panel), "")
        self.PLUGINS.insert(0, self.mediaplayer)
            
        self.panel.ShowTabs(False)

        # Attach a hotkey to a menu event
        # This makes it global
        def make_event(accel, key):
            wxid = wx.NewId()
            wx.EVT_MENU(self, wxid, self.on_hot_key)
            event = (accel, key, wxid)
            self.idKeyMap[wxid] = (accel, key)
            return event

        # maps menu event ids to key strokes
        self.idKeyMap = {}

        # Hot Key Events
        events = []        
        events.append(make_event(wx.ACCEL_SHIFT, wx.WXK_LEFT))
        events.append(make_event(wx.ACCEL_SHIFT, wx.WXK_RIGHT))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_LEFT))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_RIGHT))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_RETURN))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_ESCAPE))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_UP))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_DOWN))
        events.append(make_event(wx.ACCEL_NORMAL, wx.WXK_SPACE))

        self.SetAcceleratorTable(wx.AcceleratorTable(events))
        
        self.Show(True)
        self.set_plugin(0)
                
        self.get_plugin().SetFocusIgnoringChildren()        

        API.media.attach('current', self.mediaplayer.check_current)
        API.media.attach('state', self.mediaplayer.check_state)        

    def on_hot_key(self, evt):
        wxid = evt.Id
        accel, key = self.idKeyMap[wxid]
        try:
            self.get_plugin().handle_key(accel, key)
        except NotImplementedError:
            self.handle_key(accel, key)
        evt.Skip()

    def handle_key(self, accel, key):
        norm = wx.ACCEL_NORMAL
        shift = wx.ACCEL_SHIFT
        
        if (accel, key) == (shift, wx.WXK_LEFT):
            self.next_plugin()
        elif (accel, key) == (shift, wx.WXK_RIGHT):
            API.media.next()
        elif (accel, key) == (norm, wx.WXK_RETURN):
            API.media.play_pause()
        elif (accel, key) == (norm, wx.WXK_LEFT):
            API.media.change_volume(-0.05)
        elif (accel, key) == (norm, wx.WXK_RIGHT):
            API.media.change_volume(0.05)
            
    def next_plugin(self):
        num = self.panel.GetSelection()
        num = (num+1)%(len(self.PLUGINS))
            
        self.set_plugin(num)

    def get_plugin(self):
        i = self.panel.GetSelection()
        return self.panel.GetPage(i)

    def show_titlebar(self):
        if not self.title.IsShown():
            self.title.Show()
            self.Layout()
            self.title.Layout()

    def hide_titlebar(self):
        if self.title.IsShown():
            self.title.Hide()
            self.Layout()

    def set_plugin(self, num):
        self.show_titlebar()
        self.panel.GetPage(num).Show()
        old = self.panel.SetSelection(num)
        if old != None:
            self.panel.GetPage(old).Hide()
            
        if self.get_plugin() == self.mediaplayer:
            if API.media.media_type == API.media.TYPE_AUDIO:
                API.log.debug('Playing audio, skipping media page')
                self.next_plugin()

        self.get_plugin().SetFocusIgnoringChildren()

    def take_focus(self):
        API.log.debug('focus before: %s', wx.Window.FindFocus())
        self.get_plugin().SetFocusIgnoringChildren()
        API.log.debug('focus after: %s', wx.Window.FindFocus())

    def get_plugin_titles(self):
        # get the stand-alone title
        default_title = "i need a title"

        # get defined or default title
        single_title = getattr(self.get_plugin(), 'title', default_title)

        # get multiple titles or single title
        multi_titles = getattr(self.get_plugin(), 'titles', [single_title,"",""])

        return multi_titles
        
    def Close(self):
        API.log.debug("closing")
        API.gps.close()
        wx.Frame.Close(self)

def run():
    wx.SystemOptions.SetOptionInt("mac.listctrl.always_use_generic", 1)
    app = wx.PySimpleApp()
    wx.ToolTip.Enable(False)
    MainWindow(None, 'Matrix')
    app.MainLoop()    
        
if __name__ == "__main__":
    run()
