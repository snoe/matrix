import wx
from api import API
from lib.path import path
from gui.plugintypes import ContentPlugin

class MediaPlayer(ContentPlugin):
    def __init__(self, parent):
        ContentPlugin.__init__(self, parent)

        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self.content, style=wx.ALIGN_CENTER)
            self.mc.ShowPlayerControls(wx.media.MEDIACTRLPLAYERCONTROLS_NONE)
        except NotImplementedError:
            self.Destroy()
            raise

        self.slider = wx.Slider(self.content, minValue=1, maxValue=100)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.mc, flag=wx.ALIGN_CENTER)
        sizer.AddSpacer(10)
        sizer.Add(self.slider, flag=wx.ALIGN_CENTER|wx.EXPAND)
        sizer.AddStretchSpacer()
        self.content.SetSizer(sizer)
        #self.content.Sizer.Layout()

        self.content.Bind(wx.EVT_LEFT_DOWN, lambda e: None)
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.on_mc_loaded)
        self.Bind(wx.media.EVT_MEDIA_FINISHED, API.media.next)
        self.mc.Bind(wx.EVT_CHILD_FOCUS, self.on_focus)
        self.slider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.on_scroll)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(100)

        self.timer10 = wx.Timer(self.slider)
        self.slider.Bind(wx.EVT_TIMER, self.on_tell)
        self.timer10.Start(1000)

        self.track = None
        self.current = None

    def on_scroll(self, e):
        API.log.debug(e.GetPosition())
        self.mc.Seek(e.GetPosition())

    def check_current(self, current):
        mc_volume = self.mc.GetVolume()
        self.current = current

    def check_state(self, api_state):
        mc_state = self.mc.GetState()
        state_map = { API.media.STATE_PLAYING : wx.media.MEDIASTATE_PLAYING,
                      API.media.STATE_STOPPED : wx.media.MEDIASTATE_STOPPED,
                      API.media.STATE_PAUSED : wx.media.MEDIASTATE_PAUSED }

        if state_map[api_state] != mc_state:
            if api_state == API.media.STATE_PLAYING:
                self._play()
            if api_state == API.media.STATE_STOPPED:
                self._stop()
            if api_state == API.media.STATE_PAUSED:
                self._pause()

    def on_tell(self, e):
        self.slider.Value = self.mc.Tell()

    def on_timer(self, e):
        mc_volume = self.mc.GetVolume()

        if API.media.volume < mc_volume:
            self.mc.SetVolume(API.media.volume)
        elif abs(mc_volume - API.media.volume) > 0.01:
            if mc_volume > API.media.volume:
                self.mc.SetVolume(mc_volume - .01)
            else:
                self.mc.SetVolume(mc_volume + .01)

        if self.track != self.current and not API.media.loading:
            if API.media.media_type == API.media.TYPE_AUDIO or self.IsShown():
                API.log.debug("timer loading")
                self._load(self.current)
                self.mc.SetVolume(mc_volume)

    def on_media_state_changed(self, evt):
        API.log.debug("received event %s", evt)
        
    def on_focus(self, e):
        self.frame.take_focus()
            
    def on_mc_loaded(self, evt):
        API.log.debug("loaded %s", self.track['location'])
        API.media.loading = False
        API.media.play()
        self.slider.SetRange(0, self.mc.Length())
        self.slider.SetValue(0)
        
    def _play(self):
        if self.track:
            API.log.debug("playing %s", self.track['location'])
            if not self.mc.Play():
                API.log.error("unable to play %s, unsupported format?", self.track['location'])
            else:
                self.mc.SetInitialSize()
                self.content.Sizer.Layout()

    def _pause(self):
        API.log.debug("playing %s", self.track['location'])
        self.mc.Pause()

    def _load(self, track):
        API.log.debug("loading %s", track['location'])
        
        if not self.mc.Load(track['location']):
            API.log.error("Could not load: %s", track['name'])
            self.current = None
            self.track = None
            self.title = "Cannot Load " + track['name']
        else:
            API.media.loading = True
            self.track = track
            self.title = track['name']

    def handle_key(self, accel, key):
        norm = wx.ACCEL_NORMAL
        shift = wx.ACCEL_SHIFT
        
        if (accel, key) == (norm, wx.WXK_ESCAPE):
            self.fullscreen()
        else:
            raise NotImplementedError

    def fullscreen(self):
        if self.frame.title.IsShown():
            self.frame.hide_titlebar()
            maxx, maxy = self.frame.Size
            orgx, orgy = self.mc.BestSize
            newx, newy = 0, 0
            ratio = float(orgx)/orgy
            if maxx > maxy:
                newx = maxx
                newy = maxx / ratio
            else:
                newy = maxy
                newx = maxy*ratio
            
            self.mc.MinSize = (newx,newy)
            self.content.Size = self.frame.Size
            self.content.Layout()
            #self.content.Fit()
        else:
            self.frame.show_titlebar()
            self.mc.MinSize = self.mc.BestSize
            self.Refresh()
            self.content.Layout()
        API.log.debug("%s %s, ratio= %s should be %s",
                      self.mc.Size[0], self.mc.Size[1], float(self.mc.Size[0]) / self.mc.Size[1], 640.0/360)
