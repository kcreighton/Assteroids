import pygame, sys, math
from pygame.locals import *
from random import randint

# COLORS  = (RRR, GGG, BBB, AAA)
BLACK     = (000, 000, 000)
WHITE     = (255, 255, 255)
LASER_RED = (255, 000, 000, 200)
CLEAR     = (000, 000, 000, 000)

WINDOWWIDTH = 1340
WINDOWHEIGHT = 700
CENTER = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

BUTTASSPATH = ".\images\ButtAssSmall.png"
BUTTASSWIDTH = 73
BUTTASSHEIGHT = 100

DONKEYASSPATH = ".\images\ButtDonkeySmall.png"
DONKEYASSWIDTH = 98
DONKEYASSHEIGHT = 138

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
    Blaster = Rifle(One)
    Blaster.propulsion = 25
    BadAssList = []
    
    # quick random gen (implement better later)
    count = 0

# the main game loop
    while True:
    # clear stage
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)
        
    # constant events
        inertia(ObjectDrawQueue)
        One.adjustAim(pygame.mouse.get_pos())
        
        # quick random gen (implement better later)
        count += 1
        if count == 60:
            BadAssList.append(BadAss(pygame.image.load('ship.png'), randomLocation(), randomVelocity()))
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
            STAGE.blit(Object.sprite, Object.position)
            
    # take picture
        BACKGROUND.blit(STAGE, (0, 0))
        pygame.display.update()
        fpsClock.tick(FPS)

def inertia(RigidBodyList): # takes the velocity of all RigidBodies and moves them over time
    for Body in RigidBodyList:
        Body.position[0] += Body.velocity[0]
        Body.position[1] += Body.velocity[1]
        Body.center[0] += Body.velocity[0]
        Body.center[1] += Body.velocity[1]

def randomLocation():
    x = 0
    y = 0
    while ( x == 0 and y == 0):
        x = randint(0,WINDOWWIDTH)
        y = randint(0,WINDOWHEIGHT)
    return (x, y)

def randomVelocity(rangeX = 5, rangeY = 5):
    x = 0
    y = 0
    while ( x == 0 and y == 0):
        x = randint(-rangeX, rangeX)
        y = randint(-rangeY, rangeY)
    return (x, y)

class RigidBody:
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.position = [spawn[0], spawn[1]]
        self.velocity = [velocity[0], velocity[1]]
        self.Items= []
        ObjectDrawQueue.append(self)
        
    def accelerate(self, direction, thrust):
        self.velocity[0] += thrust * math.cos(direction)
        self.velocity[1] += thrust * math.sin(direction)

    def hit(self):
        pass
    
class Actor(RigidBody):
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.position = [spawn[0] - 16, spawn[1] - 16]
        self.velocity = [velocity[0], velocity[1]]
        self.center = [spawn[0], spawn[1]]
        self.Items= []
        self.health = 100
        self.thrust = 0.25
        self.aim = [0, 0] # point relative to screen (updated costantly)
        self.Gun = None
        ObjectDrawQueue.append(self)

# called constantly
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
    
class BadAss(RigidBody):
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.position = [spawn[0], spawn[1]]
        self.velocity = [velocity[0], velocity[1]]
        self.center = [self.position[0] + BUTTASSWIDTH/2, self.position[1] + BUTTASSHEIGHT/2]
        self.Items= []
        ObjectDrawQueue.append(self)
        
    def hit(self):
        pass
    
class GoodAss(RigidBody):
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.position = [spawn[0], spawn[1]]
        self.velocity = [velocity[0], velocity[1]]
        self.center = [self.position[0] + BUTTASSWIDTH/2, self.position[1] + BUTTASSHEIGHT/2]
        self.Items= []
        ObjectDrawQueue.append(self)
        
    def hit(self):
        pass
    
class Projectile(RigidBody):
    def __init__(self, Sprite, Owner):
        self.sprite = Sprite
        self.position = []
        self.position.append(Owner.position[0] - 16)
        self.position.append(Owner.position[1] - 16)
        self.velocity = []
        self.velocity.append(Owner.velocity[0])
        self.velocity.append(Owner.velocity[1])
        self.center = []
        self.center.append(Owner.position[0])
        self.center.append(Owner.position[1])
        self.Items = []
        self.Owner = Owner
        ObjectDrawQueue.append(self)

    def fire(self):
        if self.Owner.reticule[0] < 0:
            self.direction = math.atan(self.Owner.reticule[1]/self.Owner.reticule[0]) + math.pi
            self.velocity[0] += self.Owner.propulsion * math.cos(self.direction)
            self.velocity[1] += self.Owner.propulsion * math.sin(self.direction)
        elif self.Owner.reticule[0] > 0:
            self.direction = math.atan(self.Owner.reticule[1]/self.Owner.reticule[0])
            self.velocity[0] += self.Owner.propulsion * math.cos(self.direction)
            self.velocity[1] += self.Owner.propulsion * math.sin(self.direction)
        elif self.Owner.reticule[0] == 0 and self.Owner.reticule[1] < 0:
            self.velocity[1] -= self.Owner.propulsion
        elif self.Owner.reticule[0] == 0 and self.Owner.reticule[1] > 0:
            self.velocity[1] += self.Owner.propulsion

    def hit(self):
        pass
    
class Gun:
    def __init__(self, Owner = None):
        self.reticule = [] # point relative to gun (updated costantly)
        self.reticule.append(Owner.aim[0] - Owner.position[0])
        self.reticule.append(Owner.aim[1] - Owner.position[1])
        self.position = Owner.center
        self.velocity = Owner.velocity
        self.propulsion = 1
        self.held = False
        self.accuracy = 0
        self.Owner = Owner
        Owner.Gun = self

# called constantly
    def updateAim(self, aim):
        self.position = self.Owner.center
        self.velocity = self.Owner.velocity
        self.reticule[0] = (aim[0] - self.Owner.position[0])
        self.reticule[1] = (aim[1] - self.Owner.position[1])

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
        pygame.draw.line(STAGE, LASER_RED, self.position, self.aim, 3)

class Rifle(Gun):
    def down(self):
        self.held = True
        Bullet = Projectile(pygame.image.load('test.png'), self)
        Bullet.fire()
main()
