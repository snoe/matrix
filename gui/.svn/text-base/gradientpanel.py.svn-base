import wx

class GradientPanel(wx.Panel):
    def __init__(self, parent, c1=None, c2=None, percent=1, direction=wx.WEST):
        wx.Panel.__init__(self, parent, -1)

        self.percent = percent
        self.direction = direction

        self.c1 = c1
        self.c2 = c2

        if not c1:
            self.c1 = wx.BLACK
        if not c2:
            self.c2 = wx.Colour(46, 46, 46, wx.ALPHA_OPAQUE)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, evt):
        pdc = wx.PaintDC(self)
        try:
            dc = wx.GCDC(pdc)
        except:
            dc = pdc

        r = self.GetClientRect()
        r.SetSize((r.Size[0]*self.percent,r.Size[1]))
        dc.GradientFillLinear(r,self.c1,self.c2,self.direction)
