import random
import math
import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

def rsRandf(x):
    return x * random.random()

class Ion:    
    def __init__(self):

        if random.randint(0,2) == 1:
            self.charge = -1.0
        else:
            self.charge = 1.0

        self.xyz = [(random.random()*2.0*x) - x for x in [high,deep,wide]] 
        self.vel = [(random.random()*4.0*dSpeed) - dSpeed*2 for x in range(3)]

        self.angle = 0.0
        self.anglevel = 0.0005 * dSpeed + 0.0005 * random.random()*dSpeed

    def update(self):

        self.xyz = [self.xyz[i] + (self.vel[i] * frameTime) for i in range(3)]
	
        if(self.xyz[0] > wide):
            self.vel[0] -= 0.1 * dSpeed

        if(self.xyz[0] < -wide):
	    self.vel[0] += 0.1 * dSpeed

        if(self.xyz[1] > high):
            self.vel[1] -= 0.1 * dSpeed

        if(self.xyz[1] < -high):
            self.vel[1] += 0.1 * dSpeed

        if(self.xyz[2] > deep):
            self.vel[2] -= 0.1 * dSpeed

        if(self.xyz[2] < -deep):
            self.vel[2] += 0.1 * dSpeed

        self.angle += self.anglevel

        if(self.angle > PIx2):
            self.angle -= PIx2

	
def drawfieldline(source, x, y, z):
	brightness = 10000.0

	charge = ions[source].charge
	lastxyz = ions[source].xyz[:]
        direction = [x,y,z]

	# Do the first segment
	r = float(abs(direction[2])) * brightness
	g = float(abs(direction[0])) * brightness
	b = float(abs(direction[1])) * brightness
	if(r > 1.0):
		r = 1.0
	if(g > 1.0):
		g = 1.0
	if(b > 1.0):
		b = 1.0
	lastr = r
	lastg = g
	lastb = b
	glColor3f(r, g, b)
	xyz = [lastxyz[i] + direction[i] for i in range(3)]	
	end = [0.0,0.0,0.0]
        
	if(dElectric):
		xyz[0] += rsRandf(float(dStepSize) * 0.2) - (float(dStepSize) * 0.1)
		xyz[1] += rsRandf(float(dStepSize) * 0.2) - (float(dStepSize) * 0.1)
		xyz[2] += rsRandf(float(dStepSize) * 0.2) - (float(dStepSize) * 0.1)
	
	#if(not dConstwidth):
	#	glLineWidth((xyz[2] + 300.0) * 0.000333 * float(dWidth))

	glBegin(GL_LINE_STRIP)
	glColor3f(lastr, lastg, lastb)
	glVertex3fv(lastxyz)
	glColor3f(r, g, b)
	glVertex3fv(xyz)

	#if(not dConstwidth):
        #    glEnd()

	for i in range(dMaxSteps):
		direction[0] = 0.0
		direction[1] = 0.0
		direction[2] = 0.0
		for j in range(dIons):
			repulsion = charge * ions[j].charge
                        tempvec = [xyz[k] - ions[j].xyz[k] for k in range(3)]
			distsquared = tempvec[0] * tempvec[0] + tempvec[1] * tempvec[1] + tempvec[2] * tempvec[2]
			dist = float(math.sqrt(distsquared))
			if(dist < float(dStepSize) and i > 2):
				end[0] = ions[j].xyz[0]
				end[1] = ions[j].xyz[1]
				end[2] = ions[j].xyz[2]
				i = 10000

			tempvec[0] /= dist
			tempvec[1] /= dist
			tempvec[2] /= dist
			if(distsquared < 1.0):
				distsquared = 1.0
			direction[0] += tempvec[0] * repulsion / distsquared
			direction[1] += tempvec[1] * repulsion / distsquared
			direction[2] += tempvec[2] * repulsion / distsquared
		lastr = r
		lastg = g
		lastb = b
		r = float(abs(direction[2])) * brightness
		g = float(abs(direction[0])) * brightness
		b = float(abs(direction[1])) * brightness
		if(dElectric):
			r *= 10.0
			g *= 10.0
			b *= 10.0
			if(r > b * 0.5):
				r = b * 0.5
			if(g > b * 0.3):
				g = b * 0.3
		if(r > 1.0):
			r = 1.0
		if(g > 1.0):
			g = 1.0
		if(b > 1.0):
			b = 1.0
		distsquared = direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2]
		distrec = float(dStepSize) / float(math.sqrt(distsquared))
		direction[0] *= distrec
		direction[1] *= distrec
		direction[2] *= distrec
		if(dElectric):
			direction[0] += rsRandf(float(dStepSize)) - (float(dStepSize) * 0.5)
			direction[1] += rsRandf(float(dStepSize)) - (float(dStepSize) * 0.5)
			direction[2] += rsRandf(float(dStepSize)) - (float(dStepSize) * 0.5)
		lastxyz[0] = xyz[0]
		lastxyz[1] = xyz[1]
		lastxyz[2] = xyz[2]
		xyz[0] += direction[0]
		xyz[1] += direction[1]
		xyz[2] += direction[2]
		#if not dConstwidth:
		#	glLineWidth((xyz[2] + 300.0) * 0.000333 * float(dWidth))
		#	glBegin(GL_LINE_STRIP)
                print lastr, lastg, lastb, lastxyz,i,r,g,b,xyz,end
		glColor3f(lastr, lastg, lastb)
		glVertex3fv(lastxyz)
		if(i != 10000):
			if(i == (int(dMaxSteps) - 1)):
				glColor3f(0.0, 0.0, 0.0)
			else:
				glColor3f(r, g, b)
			glVertex3fv(xyz)
			#if(i == (int(dMaxSteps) - 1)):
			#	glEnd()
	if(i == 10001):
		glColor3f(r, g, b)
		glVertex3fv(end)

        glEnd()

def Draw():
    try:
	    s = float(math.sqrt(float(dStepSize) * float(dStepSize) * 0.333))

	    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	    for i in range(dIons):
		    ions[i].update()

	    for i in range(dIons):
		    drawfieldline(i, s, s, s)
		    drawfieldline(i, s, s, -s)
		    drawfieldline(i, s, -s, s)
		    drawfieldline(i, s, -s, -s)
		    drawfieldline(i, -s, s, s)
		    drawfieldline(i, -s, s, -s)
		    drawfieldline(i, -s, -s, s)
		    drawfieldline(i, -s, -s, -s)


    except KeyboardInterrupt:
	    sys.exit()
	    
def ReSizeGLScene(Width, Height):
	global wide
	global deep
	global high
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation

	if Width > Height:
		high = deep = 160.0
		wide = high * Width / Height
	else:
		wide = deep = 160.0
		high = wide * Height / Width

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	aspectRatio = float(Width / Height)
	gluPerspective(60.0, aspectRatio, 1.0, deep * 10)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glTranslatef(0.0, 0.0, -2.0 * deep)

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    global ions
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glEnable(GL_LINE_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    ReSizeGLScene(Width, Height)
    ions = [Ion() for i in range(dIons)]

def _draw():
    Draw()
    glutSwapBuffers()

def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")
    glutDisplayFunc(draw)
    #glutFullScreen()
    glutIdleFunc(draw)
    glutReshapeFunc(ReSizeGLScene)
    InitGL(640, 480)
    glutMainLoop()
    
dIons = 3
dStepSize = 5.0
dMaxSteps = 50
dWidth = 800
dSpeed = 20.0
dElectric = False
dConstwidth = False

dWidth = 800
wide = 160*800/600
high = 160
deep = 160
frameTime = 0.3
PIx2 = math.pi * 2

if __name__ == "__main__":
    main()
