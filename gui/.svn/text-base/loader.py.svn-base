from api import API

def loadModule(modulename):
    import sys,imp
    
    module = imp.new_module(modulename)
    fd = open("plugins/%s.py" % modulename)

    exec fd in module.__dict__
    sys.modules[modulename] = module
        
    return module

def getPlugin(modulename, parent):
    API.log.debug('Loading Plugin: %s', modulename)
    m = loadModule(modulename)
    return m.Panel(parent)

                                                                        
