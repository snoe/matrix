#!/usr/bin/env python

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

class Runner(object):
    def __init__(self, vis, fullscreen):
        self.vis = vis
        self.fullscreen = fullscreen
        
    def _draw(self):
        try:
            self.vis.Draw()
            glutSwapBuffers()
        except KeyboardInterrupt:
            sys.exit()

    def run(self):
        glutInit([])
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(0, 0)
        window = glutCreateWindow(self.vis.__name__)
        glutDisplayFunc(self._draw)
        if self.fullscreen:
            glutFullScreen()
        glutIdleFunc(self._draw)
        glutReshapeFunc(self.vis.ReSizeGLScene)
        self.vis.InitGL(640, 480)
        glutMainLoop()

# Execute the simulation.
if __name__ == '__main__':
    import imp
    if len(sys.argv) >= 2:
        modname = sys.argv[1]

        fullscreen = False
        if len(sys.argv) == 3:
            fullscreen = sys.argv[2]
            
        # load visualizer module from parameters
        x = imp.load_module(modname,*imp.find_module(modname))
        Runner(x, fullscreen).run()
