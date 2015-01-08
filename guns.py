import pygame
from rigidBody import *
from setup import *

class Gun: # projectile creator
    def __init__(self, Owner = None):
        self.reticule = [] # point relative to gun (updated costantly)
        self.reticule.append(Owner.aim[0] - Owner.position[0])
        self.reticule.append(Owner.aim[1] - Owner.position[1])
        self.position = Owner.lastCenter
        self.velocity = Owner.velocity
        self.propulsion = 1
        self.held = False
        self.accuracy = 0 # use to create variance in reticule from Owner's aim
        self.Owner = Owner
        Owner.Gun = self

# called constantly # updates targeting of gun # called by Owner's adjustAim()
    def updateAim(self, aim):
        self.position = self.Owner.center
        self.velocity = self.Owner.velocity
        self.reticule[0] = (aim[0] - self.Owner.center[0])
        self.reticule[1] = (aim[1] - self.Owner.center[1])

# down triger action
    def down(self):
        self.held = True
        
# up triger action
    def up(self):
        self.held = False

# hold triger action
    def hold(self):
        pass

class Laser(Gun):
    def hold(self):
        pygame.draw.line(STAGE, LASER_RED, self.center, self.Owner.aim, 2)

class Kinetic(Gun):
    def down(self):
        self.held = True
        Bullet = Projectile(self)
        Bullet.fire()

    def up(self):
        self.held = False

    def hold(self):
        pass
