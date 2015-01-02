import pygame, sys, math
from pygame.locals import *
from random import randint
from rigidBody import *
from assUtil import *
from asses import *
from assConstants import *
from actor import *

# set up the stage
BACKGROUND = pygame.display.set_mode((assConstants.WINDOWWIDTH, assConstants.WINDOWHEIGHT), 0, 32)
STAGE = BACKGROUND.convert_alpha()
PHYSICS = BACKGROUND.convert_alpha() # invisible layer for colision detection
pygame.display.set_caption('Assteroids')
ObjectDrawQueue = [] # placment list
BadAssList = []

def main():
    pygame.init()

# frames per second setting
    FPS = 60
    fpsClock = pygame.time.Clock()

# create props
    One = Actor(pygame.image.load('test.png'))
    ObjectDrawQueue.append(One)
    Rifle = Kinetic(One)
    Rifle.propulsion = 30
    
    # quick random gen (implement better later)
    count = 0

# the main game loop
    while True:
    # clear stage
        BACKGROUND.fill(assConstants.BLACK)
        STAGE.fill(assConstants.CLEAR)
        PHYSICS.fill(assConstants.CLEAR)
        
    # constant events
        physics(ObjectDrawQueue)
        #fov(One) NOT IMPLEMENTED
        One.adjustAim(pygame.mouse.get_pos()) # make AI controller for this
        
        # quick random gen (implement better later)
        count += 1
        if count == 60:
            newDefaultBadass()
            count = 0
    # continuous events
        # movement
        pressedList = pygame.key.get_pressed()
        if pressedList[K_w] ==  True:
            if pressedList[K_d] ==  True:
                One.accelerate(7*math.pi/4)
            elif pressedList[K_a] ==  True:
                One.accelerate(5*math.pi/4)
            else:
                One.accelerate(3*math.pi/2)
        elif pressedList[K_s] ==  True:
            if pressedList[K_d] ==  True:
                One.accelerate(math.pi/4)
            elif pressedList[K_a] ==  True:
                One.accelerate(3*math.pi/4)
            else:
                One.accelerate(math.pi/2)
        elif pressedList[K_d] ==  True:
            One.accelerate(0)
        elif pressedList[K_a] ==  True:
            One.accelerate(math.pi)
            
        if pressedList[K_SPACE] ==  True:
            pass
        if pressedList[K_r] ==  True:
            One.respawn()
        if pressedList[K_t] ==  True:
            One.respawn(preserveVelocity = True)
        
        # shooting
        if One.Gun.held ==  True:
           One.Gun.hold()
    
    # instant events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            # shooting
            if event.type == MOUSEBUTTONDOWN:
                One.Gun.down()
            if event.type == MOUSEBUTTONUP:
                One.Gun.up()
                
            # more events go here
    
    # populate stage
        for Object in ObjectDrawQueue:
            if Object.trail == True:
                pygame.draw.line(STAGE, WHITE, Object.lastCenter, Object.center, 2)
                pygame.draw.line(PHYSICS, WHITE, Object.lastCenter, Object.center, 2)
            STAGE.blit(Object.sprite, Object.position)
            
    # take picture
        BACKGROUND.blit(STAGE, (0, 0))
        pygame.display.update()
        fpsClock.tick(FPS)

def newDefaultBadass():
    newAss = BadAss(pygame.image.load('ship.png'))
    BadAssList.append(newAss)
    ObjectDrawQueue.append(newAss)

def newCustomBadass(imagePath):
    newAss = BadAss(pygame.image.load(imagePath))
    BadAssList.append(newAss)
    ObjectDrawQueue.append(newAss)
    
# called constantly # takes the velocity of all RigidBodies and moves them over time
def physics(RigidBodyList):
    for Body in RigidBodyList:
        Body.position[0] += Body.velocity[0]
        Body.position[1] += Body.velocity[1]
        Body.center[0] += Body.velocity[0]
        Body.center[1] += Body.velocity[1]
        Body.lastCenter = [ (Body.center[0] - Body.velocity[0]*2), (Body.center[1] - Body.velocity[1]*2) ]

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

main()
