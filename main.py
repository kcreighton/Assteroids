import pygame, sys, math
from pygame.locals import *
from random import randint

# COLORS  = (RRR, GGG, BBB, AAA)
BLACK     = (000, 000, 000)
WHITE     = (255, 255, 255)
LASER_RED = (255, 000, 000, 100)
CLEAR     = (000, 000, 000, 000)

WINDOWWIDTH = 1340
WINDOWHEIGHT = 700
CENTER = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

BUTTASSPATH = ".\images\ButtAssSmall.png"
DONKEYASSPATH = ".\images\ButtDonkeySmall.png"

# set up the stage
BACKGROUND = pygame.display.set_mode((WINDOWWIDTH,  WINDOWHEIGHT), 0, 32)
STAGE = BACKGROUND.convert_alpha()
PHYSICS = BACKGROUND.convert_alpha() # invisible layer for colision detection
pygame.display.set_caption('Assteroids')
ObjectDrawQueue = [] # placment list

def main():
    pygame.init()

# frames per second setting
    FPS = 60
    fpsClock = pygame.time.Clock()

# create props
    One = Actor(pygame.image.load('test.png'))
    Rifle = Kinetic(One)
    Rifle.propulsion = 30
    BadAssList = []
    
    # quick random gen (implement better later)
    count = 0

# the main game loop
    while True:
    # clear stage
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)
        PHYSICS.fill(CLEAR)
        
    # constant events
        physics(ObjectDrawQueue)
        #fov(One) NOT IMPLEMENTED
        One.adjustAim(pygame.mouse.get_pos()) # make AI controller for this
        
        # quick random gen (implement better later)
        count += 1
        if count == 60:
            BadAssList.append(BadAss(pygame.image.load('ship.png')))
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
        
# called constantly # takes the velocity of all RigidBodies and moves them over time
def physics(RigidBodyList):
    for Body in RigidBodyList:
        Body.position[0] += Body.velocity[0]
        Body.position[1] += Body.velocity[1]
        Body.center[0] += Body.velocity[0]
        Body.center[1] += Body.velocity[1]
        Body.lastCenter = [ (Body.center[0] - Body.velocity[0]*2), (Body.center[1] - Body.velocity[1]*2) ]
            
def randomLocation():
    x = randint(0,WINDOWWIDTH)
    y = randint(0,WINDOWHEIGHT)
    return [x, y]

def randomVelocity(rangeX = 5, rangeY = 5):
    x = randint(-rangeX, rangeX)
    y = randint(-rangeY, rangeY)
    return [x, y]

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
    
class Actor(RigidBody): # intelegent bodies # need AI owners
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.size = Sprite.get_size()
        self.center = [spawn[0], spawn[1]]
        self.lastCenter = self.center
        self.position = [spawn[0] - (self.size[0]/2), spawn[1] - (self.size[1]/2)]
        self.velocity = [velocity[0], velocity[1]]
        self.Items= []
        self.health = 100
        self.thrust = 0.25
        self.aim = [0, 0] # relative to screen (updated costantly)
        self.Gun = None
        self.trail = False
        ObjectDrawQueue.append(self)

# called constantly # updates targeting for actor and their gun # called in main loop
    def adjustAim(self, target):
        self.aim = target
        if self.Gun != None:
            self.Gun.updateAim(target)

    def accelerate(self, direction, thrust = None):
        thrust = self.thrust
        self.velocity[0] += thrust * math.cos(direction)
        self.velocity[1] += thrust * math.sin(direction)

    def respawn(self, spawn = CENTER, preserveVelocity = False):
        self.position = [spawn[0], spawn[1]]
        self.center = [spawn[0] + 16, spawn[1] + 16]
        if preserveVelocity == False:
            self.velocity = [0, 0]
            self.Gun.velocity = [0, 0]
            
    def hit(self):
        pass
    
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
        ObjectDrawQueue.append(self)
        
    def hit(self):
        pass
    
class GoodAss(RigidBody):
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
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
        ObjectDrawQueue.append(self)
        
    def hit(self):
        pass
    
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
