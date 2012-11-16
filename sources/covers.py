import Image
from lib.path import path
import wx

def cache_covers(folder, size):
    p = path(folder)
    walked = p.walkfiles('cover.jpg')
    covers = {}
    
    for i, f in enumerate(walked):
        source = Image.open(f)
        source = source.resize(size)
        image = apply( wx.EmptyImage, source.size )
        image.SetData( source.convert( "RGB").tostring() )
        bmp = image.ConvertToBitmap()

        covers[f] = bmp

    return covers
