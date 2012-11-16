import unittest
import wx
from gui.main import MainWindow
from core.logger import log

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = MainWindow()
    
    def tearDown(self):
        pass
        
    def testMain(self):
        self.frame.top.on_
