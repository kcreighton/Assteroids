from random import randint
from rigidBody import *
from assUtil import *
import assConstants

class BadAss(RigidBody): # thinking of making Ass class with good/bad children?
    def __init__(self, Sprite, spawn = None, velocity = None):
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
        
    def hit(self):
        pass
    
class GoodAss(RigidBody):
    def __init__(self, Sprite, spawn = assConstants.CENTER, velocity = [0, 0]):
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
        
    def hit(self):
        pass
    
