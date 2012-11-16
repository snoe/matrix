import wx
import sys
import random

import visuals

try:
    from wx import glcanvas
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

    
# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
class VizCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.visualizers = [visuals.field_lines, visuals.flock]
        self.visindex = 0
        self.vis = self.get_vis().GLMethods()
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
	self.Bind(wx.EVT_IDLE, self.OnIdle)

    def get_vis(self):
        return self.visualizers[self.visindex]

    def set_next_vis(self):
        self.visindex = (self.visindex+1) % len(self.visualizers)
        self.vis = self.get_vis().GLMethods(self.Size[0],self.Size[1])
        self.init = False

    
    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnIdle(self, evt):
        self.Refresh(False)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            size = self.size = self.GetClientSize()
            self.vis.InitGL(size.width, size.height)
            self.init = True
        self.OnDraw()

    def OnSize(self, event):
        size = self.size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
            self.vis.ReSizeGLScene()
        event.Skip()

    def OnDraw(self):
        self.vis.Draw()
	#  since this is double buffered, swap the buffers to display what just got drawn. 
	self.SwapBuffers()
