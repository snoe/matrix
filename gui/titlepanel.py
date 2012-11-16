import wx
from lib.path import path

from gradientpanel import GradientPanel
import pluginutils as utils

from api import API
from datetime import datetime

class TitlePanel(GradientPanel):
    def __init__(self, frame):
        GradientPanel.__init__(self, frame, percent=0.35)

        self.frame = frame

        theme = path('images/themes') / API.config.theme_name

        self.statebmps = {}
        self.statebmps[API.media.STATE_PLAYING] = utils.get_bitmap(theme / "play.png")
        self.statebmps[API.media.STATE_STOPPED] = utils.get_bitmap(theme / "stop.png")
        self.statebmps[API.media.STATE_PAUSED] = utils.get_bitmap(theme / "pause.png")

        self.shufflebmps = {}
        self.shufflebmps[API.media.SHUFFLE_TRACK] = utils.get_bitmap(theme / "random_track.png")
        self.shufflebmps[API.media.SHUFFLE_ALBUM] = utils.get_bitmap(theme / "random_album.png")
        self.shufflebmps[API.media.SHUFFLE_NONE] = utils.get_bitmap(theme / "random_no.png")

        self.volumebmps = {}
        self.volumebmps["volume_mute"] = utils.get_bitmap(theme / "volume_mute.png")
        self.volumebmps["volume_low"] = utils.get_bitmap(theme / "volume_low.png")
        self.volumebmps["volume_medium"] = utils.get_bitmap(theme / "volume_medium.png")
        self.volumebmps["volume_high"] = utils.get_bitmap(theme / "volume_high.png")

        c1  = wx.Colour(34, 55, 84, wx.ALPHA_OPAQUE)
        c2  = wx.Colour(83, 120, 234, wx.ALPHA_OPAQUE)
        self.stripe = GradientPanel(self, c1, c1)
        self.stripe.SetBackgroundColour(c1)

        self.titles = [None, None, None]
        self.titles[0] = wx.StaticText(self.stripe, style=wx.ALIGN_RIGHT)
        self.titles[1] = wx.StaticText(self.stripe, style=wx.ALIGN_RIGHT)
        self.titles[2] = wx.StaticText(self.stripe, style=wx.ALIGN_RIGHT)

        self.wifi = wx.StaticText(self, -1, '--', style=wx.ALIGN_LEFT)

        font = self.titles[0].GetFont()
        font.SetPointSize(24)
        self.titles[0].SetFont(font)
        font.SetPointSize(18)
        self.titles[1].SetFont(font)
        font.SetPointSize(12)
        self.titles[2].SetFont(font)

        asizer = wx.BoxSizer(wx.HORIZONTAL)
        asizer.AddStretchSpacer()
        asizer.Add(self.titles[2], flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM)
        asizer.AddSpacer(20)
        asizer.Add(self.titles[1], flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM)
        asizer.AddSpacer(20)
        asizer.Add(self.titles[0], flag=wx.ALIGN_RIGHT|wx.EXPAND)
        asizer.AddSpacer(20)
        self.stripe.SetSizer(asizer)

        self.statebmp = wx.StaticBitmap(self)
        self.shufflebmp = wx.StaticBitmap(self)
        self.volumebmp = wx.StaticBitmap(self)
        self.quit = wx.StaticBitmap(self)
        bmp = utils.get_bitmap(theme / "quit.png")
        self.quit.SetBitmap(bmp)
        self.quit.SetSize(bmp.Size)
        self.nowplayingline1 = wx.StaticText(self, -1, 'artist', style=wx.ALIGN_RIGHT)
        self.nowplayingline2 = wx.StaticText(self, -1, 'song', style=wx.ALIGN_RIGHT)
        self.clock = wx.StaticText(self, -1, datetime.now().strftime('%H:%M'))
        font = self.clock.GetFont()
        font.SetPointSize(24)
        self.clock.SetFont(font)

        nsizer = wx.BoxSizer(wx.VERTICAL)
        nsizer.Add(self.nowplayingline1, flag=wx.ALIGN_CENTER|wx.EXPAND)        
        nsizer.Add(self.nowplayingline2, flag=wx.ALIGN_CENTER|wx.EXPAND)        
        
        ssizer = wx.BoxSizer(wx.HORIZONTAL)
        ssizer.Add(nsizer, flag=wx.ALIGN_CENTER)
        ssizer.AddSpacer(10)
        ssizer.Add(self.statebmp, flag=wx.ALIGN_CENTER)
        ssizer.AddSpacer(10)
        ssizer.Add(self.shufflebmp, flag=wx.ALIGN_CENTER)
        ssizer.AddSpacer(10)
        ssizer.Add(self.volumebmp, flag=wx.ALIGN_CENTER)        
        ssizer.AddSpacer(10)
        ssizer.Add(self.quit, flag=wx.ALIGN_CENTER)        
        self.ssizer = ssizer
        
        xsizer = wx.GridBagSizer(2, 3)
        xsizer.Add(self.wifi, (0,0), flag=wx.ALIGN_CENTER|wx.EXPAND)
        xsizer.Add(self.ssizer, (0,1), flag=wx.ALIGN_CENTER|wx.EXPAND)
        xsizer.Add(self.clock, (0,2), flag=wx.ALIGN_CENTER)
        xsizer.Add(self.stripe, (1,0), (1,3), flag=wx.ALIGN_RIGHT|wx.EXPAND|wx.ALIGN_CENTER)
        xsizer.AddGrowableCol(1)
        xsizer.AddGrowableCol(0)
        self.SetSizerAndFit(xsizer)

        utils.setColours(self)
        utils.setColours(self.stripe)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update)
        self.timer.Start(1000)

        self.stripe.stripe_timer = wx.Timer(self.stripe)
        self.stripe.Bind(wx.EVT_TIMER, self.on_stripe_update)
        self.stripe.stripe_timer.Start(100)

        self.quit.Bind(wx.EVT_LEFT_UP, self.on_quit)
        self.volumebmp.Bind(wx.EVT_LEFT_UP, API.media.toggle_mute)
        self.statebmp.Bind(wx.EVT_LEFT_UP, API.media.play_pause)
        self.shufflebmp.Bind(wx.EVT_LEFT_UP, API.media.change_shuffle)

        # os x text tends to erase background, so we no op
        self.titles[0].Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.titles[1].Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.titles[2].Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.nowplayingline1.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.nowplayingline2.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.wifi.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.clock.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)

        API.media.attach('current', self.check_current)
        API.media.attach('state', self.check_state)
        API.media.attach('shuffle', self.check_shuffle)
        API.media.attach('volume', self.check_volume)

    def check_current(self, current):
        if current:
            if self.nowplayingline1.Label != current['artist']:
                self.nowplayingline1.Label = current['artist']
            if self.nowplayingline2.Label != current['name']:
                self.nowplayingline2.Label = current['name']                
                self.Sizer.Layout()

    def check_state(self, state):
        if state in self.statebmps:
            tmpbmp = self.statebmps[state]
            if tmpbmp != self.statebmp.GetBitmap():
                self.statebmp.SetBitmap(tmpbmp)
                self.statebmp.SetSize(tmpbmp.Size)
                self.Sizer.Layout()

    def check_shuffle(self, shuffle):        
        if shuffle in self.shufflebmps:
            tmpbmp = self.shufflebmps[shuffle]
            if tmpbmp != self.shufflebmp.GetBitmap():
                self.shufflebmp.SetBitmap(tmpbmp)
                self.shufflebmp.SetSize(tmpbmp.Size)                
                self.Sizer.Layout()

    def check_volume(self, volume):
        vol = ''
        if volume == 0:
            vol = 'volume_mute' 
        elif volume < 0.5:
            vol = 'volume_low'
        elif volume < 1.0:
            vol = 'volume_medium'
        else:
            vol = 'volume_high'
                
        tmpbmp = self.volumebmps[vol]
        if tmpbmp != self.volumebmp.GetBitmap():
            self.volumebmp.SetBitmap(tmpbmp)
            self.volumebmp.SetSize(tmpbmp.Size)            
            self.Sizer.Layout()

    def on_quit(self, e):
        self.frame.Close()
        
    def set_titles(self):
        # only use the first three labels
        new_labels = self.frame.get_plugin_titles()[:3]

        update = False
        for new_label, old_title in zip(new_labels, self.titles):
            if old_title.Label != new_label:
                old_title.SetLabel(new_label)
                update = True
            
        self.stripe.Sizer.Layout()
        self.Sizer.Layout()

    def on_stripe_update(self, evt):
        self.set_titles()
        if self.clock.Label != datetime.now().strftime('%H:%M'):
            self.clock.SetLabel(datetime.now().strftime('%H:%M'))
        
    def on_update(self, evt):

        API.wifi.update()
        self.wifi.Label = API.wifi.get_ssid()
        
