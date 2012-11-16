import ConfigParser
import os
from lib.path import path

class Config(object):
    try:
        import OpenGL
        opengl = True
    except ImportError:
        opengl = False

    home = path(os.environ['HOME'])
    _fname = open(home / ".matrix-config")
    _config = ConfigParser.ConfigParser()
    _config.readfp(_fname)
    raw = dict(_config.items("config"))
    config = raw
    
    fullscreen = bool(int(raw['fullscreen']))
    fontsize = int(raw['fontsize_small'])
    if fullscreen:
        fontsize = int(raw['fontsize_full'])

    theme_name = raw['theme_name']
    gpsfile = raw['gpsfile']
    
    mp3path = raw['mp3path']

    slidepath = raw['slidepath']
    
                 
