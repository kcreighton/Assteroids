import math
from random import randint
from utility import *
from setup import * 

class RigidBody: # physics objects # need to add collision
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.size = Sprite.get_size()
        self.center = [spawn[0], spawn[1]]
        self.lastCenter = self.center
        self.position = [spawn[0] - (self.size[0]/2), spawn[1] - (self.size[1]/2)]
        self.velocity = [velocity[0], velocity[1]]
        self.Items= []
        self.trail = False
        ObjectDrawQueue.append(self)
        
    def accelerate(self, direction, thrust):
        self.velocity[0] += thrust * math.cos(direction)
        self.velocity[1] += thrust * math.sin(direction)

    def hit(self):
        pass
class Ass(RigidBody):
    def __init__(self, Sprite, spawn = None, velocity = None, bad = True):
        self.sprite = Sprite
        self.size = Sprite.get_size()
        if spawn == None:
            self.center = randomLocation()
            self.position = [self.center[0] - (self.size[0]/2), self.center[1] - (self.size[1]/2)]
        else:
            self.center = [spawn[0], spawn[1]]
            self.position = [spawn[0] - (self.size[0]/2), spawn[1] - (self.size[1]/2)]
        if velocity == None:
            self.velocity = randomVelocity()
        else:
            self.velocity = velocity
        self.lastCenter = self.center
        self.Items= []
        self.trail = False
        self.bad = None
        
    def hit(self):
        pass
    
def newAss(bad = True):
    if bad == True:
        newAss = Ass(pygame.image.load('ship.png'))
        BadAssList.append(newAss)
    else:
        newAss = Ass(pygame.image.load('goodShip.png'))
        GoodAssList.append(newAss)
    ObjectDrawQueue.append(newAss)

class Projectile(RigidBody):
    def __init__(self, Owner, Sprite = None):
        self.center = [Owner.position[0], Owner.position[1]]
        if Sprite == None:
            self.sprite = pygame.image.load('invisiPoint.png')
            self.size = [0, 0]
            self.position = self.center
            self.trail = True
        else:
            self.sprite = Sprite
            self.size = Sprite.get_size()
            self.position = [Owner.position[0] - (self.size[0]/2), Owner.position[1] - (self.size[1]/2)]
            self.trail = False
        self.velocity = [Owner.velocity[0], Owner.velocity[1]]
        self.lastCenter = self.center
        self.Items = []
        self.Owner = Owner
        ObjectDrawQueue.append(self)

    def fire(self):
        if self.Owner.reticule[0] < 0:
            self.direction = math.atan( (self.Owner.reticule[1])/(self.Owner.reticule[0]) ) + math.pi
            self.velocity[0] += self.Owner.propulsion * math.cos(self.direction)
            self.velocity[1] += self.Owner.propulsion * math.sin(self.direction)
        elif self.Owner.reticule[0] > 0:
            self.direction = math.atan( (self.Owner.reticule[1])/(self.Owner.reticule[0]) )
            self.velocity[0] += self.Owner.propulsion * math.cos(self.direction)
            self.velocity[1] += self.Owner.propulsion * math.sin(self.direction)
        elif self.Owner.reticule[0] == 0 and self.Owner.reticule[1] < 0:
            self.velocity[1] -= self.Owner.propulsion
        elif self.Owner.reticule[0] == 0 and self.Owner.reticule[1] > 0:
            self.velocity[1] += self.Owner.propulsion

    def hit(self):
        pass

