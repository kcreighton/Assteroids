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
DONKEYASSPATH = ".\images\ButtDonkeySmall.png"

# tables of precalculated values of sin(x / (180 / pi)) and cos(x / (180 / pi))
SINTABLE = (
    0.00000, 0.01745, 0.03490, 0.05234, 0.06976, 0.08716, 0.10453,
    0.12187, 0.13917, 0.15643, 0.17365, 0.19081, 0.20791, 0.22495, 0.24192,
    0.25882, 0.27564, 0.29237, 0.30902, 0.32557, 0.34202, 0.35837, 0.37461,
    0.39073, 0.40674, 0.42262, 0.43837, 0.45399, 0.46947, 0.48481, 0.50000,
    0.51504, 0.52992, 0.54464, 0.55919, 0.57358, 0.58779, 0.60182, 0.61566,
    0.62932, 0.64279, 0.65606, 0.66913, 0.68200, 0.69466, 0.70711, 0.71934,
    0.73135, 0.74314, 0.75471, 0.76604, 0.77715, 0.78801, 0.79864, 0.80902,
    0.81915, 0.82904, 0.83867, 0.84805, 0.85717, 0.86603, 0.87462, 0.88295,
    0.89101, 0.89879, 0.90631, 0.91355, 0.92050, 0.92718, 0.93358, 0.93969,
    0.94552, 0.95106, 0.95630, 0.96126, 0.96593, 0.97030, 0.97437, 0.97815,
    0.98163, 0.98481, 0.98769, 0.99027, 0.99255, 0.99452, 0.99619, 0.99756,
    0.99863, 0.99939, 0.99985, 1.00000, 0.99985, 0.99939, 0.99863, 0.99756,
    0.99619, 0.99452, 0.99255, 0.99027, 0.98769, 0.98481, 0.98163, 0.97815,
    0.97437, 0.97030, 0.96593, 0.96126, 0.95630, 0.95106, 0.94552, 0.93969,
    0.93358, 0.92718, 0.92050, 0.91355, 0.90631, 0.89879, 0.89101, 0.88295,
    0.87462, 0.86603, 0.85717, 0.84805, 0.83867, 0.82904, 0.81915, 0.80902,
    0.79864, 0.78801, 0.77715, 0.76604, 0.75471, 0.74314, 0.73135, 0.71934,
    0.70711, 0.69466, 0.68200, 0.66913, 0.65606, 0.64279, 0.62932, 0.61566,
    0.60182, 0.58779, 0.57358, 0.55919, 0.54464, 0.52992, 0.51504, 0.50000,
    0.48481, 0.46947, 0.45399, 0.43837, 0.42262, 0.40674, 0.39073, 0.37461,
    0.35837, 0.34202, 0.32557, 0.30902, 0.29237, 0.27564, 0.25882, 0.24192,
    0.22495, 0.20791, 0.19081, 0.17365, 0.15643, 0.13917, 0.12187, 0.10453,
    0.08716, 0.06976, 0.05234, 0.03490, 0.01745, 0.00000, -0.01745, -0.03490,
    -0.05234, -0.06976, -0.08716, -0.10453, -0.12187, -0.13917, -0.15643,
    -0.17365, -0.19081, -0.20791, -0.22495, -0.24192, -0.25882, -0.27564,
    -0.29237, -0.30902, -0.32557, -0.34202, -0.35837, -0.37461, -0.39073,
    -0.40674, -0.42262, -0.43837, -0.45399, -0.46947, -0.48481, -0.50000,
    -0.51504, -0.52992, -0.54464, -0.55919, -0.57358, -0.58779, -0.60182,
    -0.61566, -0.62932, -0.64279, -0.65606, -0.66913, -0.68200, -0.69466,
    -0.70711, -0.71934, -0.73135, -0.74314, -0.75471, -0.76604, -0.77715,
    -0.78801, -0.79864, -0.80902, -0.81915, -0.82904, -0.83867, -0.84805,
    -0.85717, -0.86603, -0.87462, -0.88295, -0.89101, -0.89879, -0.90631,
    -0.91355, -0.92050, -0.92718, -0.93358, -0.93969, -0.94552, -0.95106,
    -0.95630, -0.96126, -0.96593, -0.97030, -0.97437, -0.97815, -0.98163,
    -0.98481, -0.98769, -0.99027, -0.99255, -0.99452, -0.99619, -0.99756,
    -0.99863, -0.99939, -0.99985, -1.00000, -0.99985, -0.99939, -0.99863,
    -0.99756, -0.99619, -0.99452, -0.99255, -0.99027, -0.98769, -0.98481,
    -0.98163, -0.97815, -0.97437, -0.97030, -0.96593, -0.96126, -0.95630,
    -0.95106, -0.94552, -0.93969, -0.93358, -0.92718, -0.92050, -0.91355,
    -0.90631, -0.89879, -0.89101, -0.88295, -0.87462, -0.86603, -0.85717,
    -0.84805, -0.83867, -0.82904, -0.81915, -0.80902, -0.79864, -0.78801,
    -0.77715, -0.76604, -0.75471, -0.74314, -0.73135, -0.71934, -0.70711,
    -0.69466, -0.68200, -0.66913, -0.65606, -0.64279, -0.62932, -0.61566,
    -0.60182, -0.58779, -0.57358, -0.55919, -0.54464, -0.52992, -0.51504,
    -0.50000, -0.48481, -0.46947, -0.45399, -0.43837, -0.42262, -0.40674,
    -0.39073, -0.37461, -0.35837, -0.34202, -0.32557, -0.30902, -0.29237,
    -0.27564, -0.25882, -0.24192, -0.22495, -0.20791, -0.19081, -0.17365,
    -0.15643, -0.13917, -0.12187, -0.10453, -0.08716, -0.06976, -0.05234,
    -0.03490, -0.01745, -0.00000)

COSTABLE = (
    1.00000, 0.99985, 0.99939, 0.99863, 0.99756, 0.99619, 0.99452,
    0.99255, 0.99027, 0.98769, 0.98481, 0.98163, 0.97815, 0.97437, 0.97030,
    0.96593, 0.96126, 0.95630, 0.95106, 0.94552, 0.93969, 0.93358, 0.92718,
    0.92050, 0.91355, 0.90631, 0.89879, 0.89101, 0.88295, 0.87462, 0.86603,
    0.85717, 0.84805, 0.83867, 0.82904, 0.81915, 0.80902, 0.79864, 0.78801,
    0.77715, 0.76604, 0.75471, 0.74314, 0.73135, 0.71934, 0.70711, 0.69466,
    0.68200, 0.66913, 0.65606, 0.64279, 0.62932, 0.61566, 0.60182, 0.58779,
    0.57358, 0.55919, 0.54464, 0.52992, 0.51504, 0.50000, 0.48481, 0.46947,
    0.45399, 0.43837, 0.42262, 0.40674, 0.39073, 0.37461, 0.35837, 0.34202,
    0.32557, 0.30902, 0.29237, 0.27564, 0.25882, 0.24192, 0.22495, 0.20791,
    0.19081, 0.17365, 0.15643, 0.13917, 0.12187, 0.10453, 0.08716, 0.06976,
    0.05234, 0.03490, 0.01745, 0.00000, -0.01745, -0.03490, -0.05234, -0.06976,
    -0.08716, -0.10453, -0.12187, -0.13917, -0.15643, -0.17365, -0.19081,
    -0.20791, -0.22495, -0.24192, -0.25882, -0.27564, -0.29237, -0.30902,
    -0.32557, -0.34202, -0.35837, -0.37461, -0.39073, -0.40674, -0.42262,
    -0.43837, -0.45399, -0.46947, -0.48481, -0.50000, -0.51504, -0.52992,
    -0.54464, -0.55919, -0.57358, -0.58779, -0.60182, -0.61566, -0.62932,
    -0.64279, -0.65606, -0.66913, -0.68200, -0.69466, -0.70711, -0.71934,
    -0.73135, -0.74314, -0.75471, -0.76604, -0.77715, -0.78801, -0.79864,
    -0.80902, -0.81915, -0.82904, -0.83867, -0.84805, -0.85717, -0.86603, 
    -0.87462, -0.88295, -0.89101, -0.89879, -0.90631, -0.91355, -0.92050,
    -0.92718, -0.93358, -0.93969, -0.94552, -0.95106, -0.95630, -0.96126,
    -0.96593, -0.97030, -0.97437, -0.97815, -0.98163, -0.98481, -0.98769,
    -0.99027, -0.99255, -0.99452, -0.99619, -0.99756, -0.99863, -0.99939,
    -0.99985, -1.00000, -0.99985, -0.99939, -0.99863, -0.99756, -0.99619,
    -0.99452, -0.99255, -0.99027, -0.98769, -0.98481, -0.98163, -0.97815,
    -0.97437, -0.97030, -0.96593, -0.96126, -0.95630, -0.95106, -0.94552,
    -0.93969, -0.93358, -0.92718, -0.92050, -0.91355, -0.90631, -0.89879,
    -0.89101, -0.88295, -0.87462, -0.86603, -0.85717, -0.84805, -0.83867,
    -0.82904, -0.81915, -0.80902, -0.79864, -0.78801, -0.77715, -0.76604,
    -0.75471, -0.74314, -0.73135, -0.71934, -0.70711, -0.69466, -0.68200,
    -0.66913, -0.65606, -0.64279, -0.62932, -0.61566, -0.60182, -0.58779,
    -0.57358, -0.55919, -0.54464, -0.52992, -0.51504, -0.50000, -0.48481,
    -0.46947, -0.45399, -0.43837, -0.42262, -0.40674, -0.39073, -0.37461,
    -0.35837, -0.34202, -0.32557, -0.30902, -0.29237, -0.27564, -0.25882,
    -0.24192, -0.22495, -0.20791, -0.19081, -0.17365, -0.15643, -0.13917,
    -0.12187, -0.10453, -0.08716, -0.06976, -0.05234, -0.03490, -0.01745,
    -0.00000, 0.01745, 0.03490, 0.05234, 0.06976, 0.08716, 0.10453, 0.12187,
    0.13917, 0.15643, 0.17365, 0.19081, 0.20791, 0.22495, 0.24192, 0.25882,
    0.27564, 0.29237, 0.30902, 0.32557, 0.34202, 0.35837, 0.37461, 0.39073,
    0.40674, 0.42262, 0.43837, 0.45399, 0.46947, 0.48481, 0.50000, 0.51504,
    0.52992, 0.54464, 0.55919, 0.57358, 0.58779, 0.60182, 0.61566, 0.62932,
    0.64279, 0.65606, 0.66913, 0.68200, 0.69466, 0.70711, 0.71934, 0.73135,
    0.74314, 0.75471, 0.76604, 0.77715, 0.78801, 0.79864, 0.80902, 0.81915,
    0.82904, 0.83867, 0.84805, 0.85717, 0.86603, 0.87462, 0.88295, 0.89101,
    0.89879, 0.90631, 0.91355, 0.92050, 0.92718, 0.93358, 0.93969, 0.94552,
    0.95106, 0.95630, 0.96126, 0.96593, 0.97030, 0.97437, 0.97815, 0.98163,
    0.98481, 0.98769, 0.99027, 0.99255, 0.99452, 0.99619, 0.99756, 0.99863,
    0.99939, 0.99985, 1.00000)

# set up the stage
BACKGROUND = pygame.display.set_mode((WINDOWWIDTH,  WINDOWHEIGHT), 0, 32)
STAGE = BACKGROUND.convert_alpha()
PHYSICS = BACKGROUND.convert_alpha() # invisible layer for colision detection
SCREEN = BACKGROUND.convert_alpha() # invisible layer for FOV
pygame.display.set_caption('Assteroids')
ObjectDrawQueue = [] # placment list

def main():
    pygame.init()

# frames per second setting
    FPS = 30
    fpsClock = pygame.time.Clock()

# create props
    One = Actor(pygame.image.load('test.png'))
    Blaster = Rifle(One)
    Blaster.propulsion = 50
    BadAssList = []
    
    # quick random gen (implement better later)
    count = 0

# the main game loop
    while True:
    # clear stage
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)
        PHYSICS.fill(CLEAR)
        SCREEN.fill(BLACK)
        
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
            STAGE.blit(Object.sprite, Object.position)
            
    # take picture
        BACKGROUND.blit(STAGE, (0, 0))
        #BACKGROUND.blit(SCREEN, (0, 0)) NOT IMPLEMENTED
        pygame.display.update()
        fpsClock.tick(FPS)
        
# called constantly # takes the velocity of all RigidBodies and moves them over time
def physics(RigidBodyList):
    for Body in RigidBodyList:
        if Body.trail == True:
            oldPoint = Body.center
            newPoint = []
            newPoint.append(Body.center[0] + Body.velocity[0]*2)
            newPoint.append(Body.center[1] + Body.velocity[1]*2)
            pygame.draw.line(STAGE, WHITE, oldPoint, newPoint, 3)
            pygame.draw.line(PHYSICS, WHITE, oldPoint, newPoint, 3)
        Body.position[0] += Body.velocity[0]
        Body.position[1] += Body.velocity[1]
        Body.center[0] += Body.velocity[0]
        Body.center[1] += Body.velocity[1]
            
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
        self.position = Owner.center
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
        pygame.draw.line(STAGE, LASER_RED, self.position, self.Owner.aim, 3)

class Rifle(Gun):
    def up(self):
        self.held = False
        Bullet = Projectile(self)
        Bullet.fire()

main()
