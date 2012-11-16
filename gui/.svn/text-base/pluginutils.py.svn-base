import wx
import wx.lib.mixins.listctrl as listmix
import wx.media
import os
import Image
from gradientpanel import GradientPanel


# Utility classes to write plugins
def setColours(obj, foreground=wx.WHITE, background=wx.BLACK):
    olist = [obj] + obj.GetChildren()
    for o in olist:
        o.SetBackgroundColour(background)
        o.SetForegroundColour(foreground)

def get_bitmap( filename, newsize=None ):
    if newsize:
        source = Image.open( filename )
        w = source.size[0]
        h = source.size[1]

        ratio = 1        
        if w>=h and w > newsize[0]:
            ratio = newsize[0]/(w*1.0)
        elif h>w and h > newsize[1]:
            ratio = newsize[1]/(h*1.0)
        if ratio != 1:
            source = source.resize(map(int,(w*ratio,h*ratio)))
        image = apply( wx.EmptyImage, source.size )
        image.SetData( source.convert( "RGB").tostring() )
        image.SetAlphaData(source.convert("RGBA").tostring()[3::4])
        bmp = image.ConvertToBitmap()
    else:
        bmp = wx.Image( filename, wx.BITMAP_TYPE_ANY ).ConvertToBitmap()
    return bmp
