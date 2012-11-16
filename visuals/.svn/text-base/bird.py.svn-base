import math
import random
from utils import Point, Dimension

class Bird(object):
    size = Dimension(0,0)
    
    def __init__(self,x,y,theta,color,bird_id):
        self.bird_id = bird_id
        self.x = x
        self.y = y
        self.theta = theta
        self.color = color
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.alpha = 1
        self.speed = 2
        self.max_turn_theta = random.randint(5,45)

    def getLocation(self):
        return Point(self.x, self.y)

    def move(self, newHeading):
        # determine if it is better to turn left or right for the new heading
        left = (newHeading - self.theta + 360) % 360
        right = (self.theta - newHeading + 360) % 360
        
        # after deciding which way to turn, find out if we can turn that much
        thetaChange = 0
        if (left < right):
            # if left > than the max turn, then we can't fully adopt the new heading
            thetaChange = min(self.max_turn_theta, left)
        else:
            # right turns are negative degrees
            thetaChange = -1*min(self.max_turn_theta, right)
        
        # Make the turn
        self.theta = (self.theta + thetaChange + 360) % 360
        
        # Now move speed pixels in the direction the bird now faces.
        # Note: Because values are truncated, a speed of 1 will result in no
        # movement unless the bird is moving exactly vertically or horizontally.
        x = self.x + int(self.speed * math.cos(self.theta * math.pi/180))
        y = self.y - int(self.speed * math.sin(self.theta * math.pi/180))
        if y > self.size.height or x > self.size.width or x < 3 or y < 3:
            self.speed *= -1

        self.x = x
        self.y = y

    def getDistance(self, p):
        dX = p.x - self.x
        dY = p.y - self.y
        
        return int(math.sqrt( pow( dX, 2 ) + pow( dY, 2 )))

class Food(Bird):
    def __init__(self, x, y):
        Bird.__init__(self, x, y, 0, (1.0,1.0,0.0)) # yellow

    def move(self):
        return

class Predator(Bird):
    def __init__(self, x, y, theta):
        Bird.__init__(self, x, y, theta, (1.0,0.0,0.0)) # red
        self.hunger = 5
