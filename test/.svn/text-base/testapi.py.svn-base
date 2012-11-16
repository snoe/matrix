import api
import unittest
from core.logger import log

class TestApi(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def testApi(self):
        a = api.API
        b = api.API
        assert(id(a.library) == id(b.library))
        assert(id(a.media) == id(b.media))
        assert(id(a.config) == id(b.config))

    def testLibrary(self):
        lib = api.API.library
        log.debug(lib.get_song_struct(0))
        
        
