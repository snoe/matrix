#!/usr/bin/env python

import unittest
from test import testmain, testcontrol

def suite():
    suites = (unittest.makeSuite(testmain.TestMain, 'test'),
              unittest.makeSuite(testapi.TestApi, 'test'))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
