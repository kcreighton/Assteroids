import pygame, sys, math
from pygame.locals import *

# COLOR = (RRR, GGG, BBB, AAA)
BLACK   = (000, 000, 000)
WHITE   = (255, 255, 255)
CLEAR   = (000, 000, 000, 000)

WINDOWWIDTH = 1800
WINDOWHEIGTH = 1000
CENTER = (WINDOWWIDTH/2, WINDOWHEIGTH/2)

ObjectDrawQueue = []

def main():
    pygame.init()

    FPS = 60 # frames per second setting
    fpsClock = pygame.time.Clock()

    # set up the window
    BACKGROUND = pygame.display.set_mode((WINDOWWIDTH,  WINDOWHEIGTH), 0, 32)
    STAGE = BACKGROUND.convert_alpha()
    PHYSICS = BACKGROUND.convert_alpha()
    pygame.display.set_caption('Assteroids')

    One = Player()
    mousePressed = False

    while True: # the main game loop 
        
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)

        inertia(ObjectDrawQueue)
        mousePosition = pygame.mouse.get_pos()
        pressedList = pygame.key.get_pressed()
        
        if pressedList[K_w] ==  True:
            if pressedList[K_d] ==  True:
                One.accelerate(7*math.pi/2)
            else:
                One.accelerate(3*math.pi/2)
        elif pressedList[K_d] ==  True:
            if pressedList[K_s] ==  True:
                One.accelerate(math.pi/4)
            else:
                One.accelerate(0)
        elif pressedList[K_s] ==  True:
            if pressedList[K_a] ==  True:
                One.accelerate(3*math.pi/4)
            else:
                One.accelerate(math.pi/2)
        elif pressedList[K_a] ==  True:
            if pressedList[K_w] ==  True:
                One.accelerate(5*math.pi/4)
            else:
                One.accelerate(math.pi)
        if pressedList[K_SPACE] ==  True:
            One.brakes()
        if pressedList[K_r] ==  True:
            One.respawn()
        if pressedList[K_t] ==  True:
            One.respawn(preserveVelocity = True)
        if mousePressed ==  True:
            pygame.draw.line(STAGE, WHITE, One.center, mousePosition, 4)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mousePressed = True
            if event.type == MOUSEBUTTONUP:
                mousePressed = False
            # more events go here
            
        for Object in ObjectDrawQueue:
            STAGE.blit(Object.sprite, Object.position)
        BACKGROUND.blit(STAGE, (0, 0))
        
        pygame.display.update()
        fpsClock.tick(FPS)

def inertia(Objects): # takes the velocity of all objects and moves them over time
    for Object in Objects:
        Object.position[0] += Object.velocity[0]
        Object.position[1] += Object.velocity[1]
        Object.center[0] += Object.velocity[0]
        Object.center[1] += Object.velocity[1]

class Player:
    def __init__(self, spawn = CENTER):
        self.sprite = pygame.image.load('test.png')
        self.health = 100
        self.position = [spawn[0], spawn[1]]
        self.center = [spawn[0] + 16, spawn[1] + 16]
        self.velocity = [0, 0]
        self.thrust = 1
        ObjectDrawQueue.append(self)

    def accelerate(self, direction):
        self.velocity[0] += self.thrust * math.cos(direction)
        self.velocity[1] += self.thrust * math.sin(direction)
        
    def brakes(self): # no tworking properly
        self.velocity[0] -= self.thrust * math.cos(self.direction)
        if self.velocity[0] < 0:
            self.velocity[0] = 0
        self.velocity[1] -= self.thrust * math.sin(self.direction)
        if self.velocity[1] < 0:
            self.velocity[1] = 0
            
    def respawn(self, spawn = CENTER, preserveVelocity = False):
        self.position = [spawn[0], spawn[1]]
        self.center = [spawn[0] + 16, spawn[1] + 16]
        if preserveVelocity == False:
            self.velocity = [0, 0]
            
    def damage(self):
        pass

class Gun:
    def __init__(self):
        pass
main()
