import pygame, sys, math
from pygame.locals import *
from random import randint

# COLOR   = (RRR, GGG, BBB, AAA)
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

ObjectDrawQueue = []

def main():
    pygame.init()

    FPS = 60 # frames per second setting
    fpsClock = pygame.time.Clock()

    # set up the window
    BACKGROUND = pygame.display.set_mode((WINDOWWIDTH,  WINDOWHEIGHT), 0, 32)
    STAGE = BACKGROUND.convert_alpha()
    PHYSICS = BACKGROUND.convert_alpha()
    pygame.display.set_caption('Assteroids')


    One = Actor(pygame.image.load('test.png'))
    Blaster = Laser(One)

    BadAssList = []
    count = 0

    while True: # the main game loop 
        
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)

        inertia(ObjectDrawQueue)
        One.Aim()
        # quick random gen
        count += 1
        if count == 60:
            BadAssList.append(Ass(pygame.image.load('ship.png'), randomLocation(), randomVelocity())
            count = 0
        
        pressedList = pygame.key.get_pressed()
       
       # <Movment>
        
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
            
        # </Movement>
            
        if pressedList[K_SPACE] ==  True:
            One.brakes()
        if pressedList[K_r] ==  True:
            One.respawn()
        if pressedList[K_t] ==  True:
            One.respawn(preserveVelocity = True)
        
        if One.Gun.held ==  True:
           One.Gun.hold(STAGE)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                One.Gun.down()
            if event.type == MOUSEBUTTONUP:
                One.Gun.up()
            # more events go here
            
        for Object in ObjectDrawQueue:
            STAGE.blit(Object.sprite, Object.position)
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

def randomVelocity():
    x = 0
    y = 0
    while ( x == 0 and y == 0):
        x = randint(-5,5)
        y = randint(-5,5)
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

class Actor(RigidBody):
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.position = [spawn[0], spawn[1]]
        self.velocity = [velocity[0], velocity[1]]
        self.center = [spawn[0] + 16, spawn[1] + 16]
        self.Items= []
        self.health = 100
        self.thrust = 0.25
        self.aim = pygame.mouse.get_pos()
        ObjectDrawQueue.append(self)

    def Aim(self):
        self.aim = pygame.mouse.get_pos()
        self.Gun.aim = pygame.mouse.get_pos()
        self.Gun.position = self.center

    def accelerate(self, direction, thrust = None):
        thrust = self.thrust
        self.velocity[0] += thrust * math.cos(direction)
        self.velocity[1] += thrust * math.sin(direction)

    def respawn(self, spawn = CENTER, preserveVelocity = False):
        self.position = [spawn[0], spawn[1]]
        self.center = [spawn[0] + 16, spawn[1] + 16]
        if preserveVelocity == False:
            self.velocity = [0, 0]
            
    def damage(self):
        pass
    
class Ass(RigidBody):
    def __init__(self, Sprite, spawn = CENTER, velocity = [0, 0]):
        self.sprite = Sprite
        self.position = [spawn[0], spawn[1]]
        self.velocity = [velocity[0], velocity[1]]
        self.center = [self.position[0] + BUTTASSWIDTH/2, self.position[1] + BUTTASSHEIGHT/2]
        self.Items= []
        ObjectDrawQueue.append(self)

class Gun:
    def __init__(self, Owner = None):
        self.aim = Owner.aim
        self.position = Owner.center
        self.held = False
        Owner.Gun = self
    
    def down(self, SURFACE = None):
        self.held = True
        
    def up(self, SURFACE = None):
        self.held = False
    
    def hold(self, SURFACE = None):
        pass

class Laser(Gun):
    def hold(self, SURFACE = None):
        pygame.draw.line(SURFACE, LASER_RED, self.position, self.aim, 3)

class Rifle(Gun):
    def down(self, SURFACE = None):
        self.held = True
main()
