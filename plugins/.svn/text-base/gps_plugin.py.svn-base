import wx
from gui.plugintypes import ContentPlugin

from datetime import datetime, date
from api import API

# must be named panel
class Panel(ContentPlugin):
    def __init__(self, parent):
        ContentPlugin.__init__(self, parent)
        self.title = "GPS"

        self.speed = wx.StaticText(self.content, label="No Fix")
        self.speed_average = wx.StaticText(self.content, label="No Fix")
        self.trip_time = wx.StaticText(self.content)
        self.total_distance = wx.StaticText(self.content)
        
        self.reset = wx.Button(self.content, -1, "reset")

        trip_time_label = wx.StaticText(self.content, -1, "Current Trip Duration: ")
        speed_label = wx.StaticText(self.content, -1, "Current Speed: ")
        speed_average_label = wx.StaticText(self.content, -1, "Average Speed: ")
        total_distance_label = wx.StaticText(self.content, -1, "Distance Travelled: ")
        self.set_font([self.speed, self.speed_average, self.trip_time, self.total_distance,
                       speed_label, speed_average_label, trip_time_label, total_distance_label])

        xsizer = wx.GridBagSizer(5, 2)
        xsizer.Add(trip_time_label, (0,0), flag=wx.ALIGN_RIGHT)
        xsizer.Add(speed_label, (1,0), flag=wx.ALIGN_RIGHT)
        xsizer.Add(speed_average_label, (2,0), flag=wx.ALIGN_RIGHT)
        xsizer.Add(total_distance_label, (3,0), flag=wx.ALIGN_RIGHT)
        xsizer.Add(self.reset, (4,0), flag=wx.ALIGN_CENTER)

        xsizer.Add(self.trip_time, (0,1), flag=wx.ALIGN_LEFT)
        xsizer.Add(self.speed, (1,1), flag=wx.ALIGN_LEFT)
        xsizer.Add(self.speed_average, (2,1), flag=wx.ALIGN_LEFT)
        xsizer.Add(self.total_distance, (3,1), flag=wx.ALIGN_LEFT)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(xsizer, flag=wx.ALIGN_CENTER)
        sizer.AddSpacer(20)

        self.content.SetSizerAndFit(sizer)
        self.content.SetAutoLayout(True)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(1000)

        self.reset.Bind(wx.EVT_BUTTON, API.gps.reset)


    def set_font(self, lst):
        for obj in lst:
            font = obj.GetFont()
            font.SetPointSize(32)
            obj.SetFont(font)
            obj.SetForegroundColour("white")
        
    def on_timer(self, evt):
        if self.frame.get_plugin() == self:
            speed = API.gps.get_speed()
            avg_speed = API.gps.get_avg_speed()
            trip_time = str(API.gps.get_trip_time())
            trip_time = trip_time[:trip_time.rfind('.')]
            dist = API.gps.get_total_distance()            
            
            if not speed:
                self.speed.SetLabel("No Fix")
            else:
                self.speed.SetLabel("%.2f km/h" % speed)

            self.speed_average.SetLabel("%.2f km/h" % avg_speed)
            self.trip_time.SetLabel(trip_time)
            self.total_distance.SetLabel("%.4f km" % dist)
                
if __name__ == "__main__":
    session = gps.gps(host="127.0.0.1", port="2947")
    session.set_raw_hook(raw_hook)
    session.query("o")
    while True:
        time.sleep(1)
        session.query("o")
       
