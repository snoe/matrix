from core import library
from core import config
from core import media
from core import wifi
from core import gps_logger

import logging

class API(object):
    log = logging.getLogger()
    config = config.Config()
    library = library.Library(config.mp3path)
    media = media.Media(library)
    wifi = wifi.WiFi()
    gps = gps_logger.GPS(config.gpsfile)

    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance
