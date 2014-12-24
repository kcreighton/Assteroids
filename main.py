import pygame, sys, math
from pygame.locals import *

# COLOR = (RRR, GGG, BBB)
BLACK   = (000, 000, 000)
CLEAR   = (000, 000, 000, 000)

CENTER = (400, 300)

ObjectDrawQueue = []

def inertia(Objects):
    for Object in Objects:
        Object.position[0] += Object.velocity[0]
        Object.position[1] += Object.velocity[1]
    # takes the velocity of all objects and moves them over time

class Player:
    def __init__(self, spawn = CENTER):
        self.image = pygame.image.load('test.png') # the source image
        self.sprite = pygame.image.load('test.png') # where the rotated image will be stored
        self.health = 100
        self.position = [spawn[0], spawn[1]]
        self.velocity = [0, 0]
        self.thrust = 1
        ObjectDrawQueue.append(self)

    def accelerate(self, direction):
        self.velocity[0] += self.thrust * math.cos(direction)
        self.velocity[1] += self.thrust * math.sin(direction)
        
    def brakes(self): # notworking properly
        self.velocity[0] -= self.thrust * math.cos(self.direction)
        if self.velocity[0] < 0:
            self.velocity[0] = 0
        self.velocity[1] -= self.thrust * math.sin(self.direction)
        if self.velocity[1] < 0:
            self.velocity[1] = 0
            
    def damage(self):
        pass

class Gun:
    def __init__(self):
        pass
    

def main():
    pygame.init()

    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    # set up the window
    BACKGROUND = pygame.display.set_mode((800, 600), 0, 32)
    STAGE = BACKGROUND.convert_alpha()
    PHYSICS = BACKGROUND.convert_alpha()
    pygame.display.set_caption('Assteroids')

    One = Player()

    while True: # the main game loop 
        
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)
        inertia(ObjectDrawQueue)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_RIGHT, K_d):
                    One.accelerate(0)
                elif event.key in (K_DOWN, K_s):
                    One.accelerate(math.pi/2)
                elif event.key in (K_LEFT, K_a):
                    One.accelerate(math.pi)
                elif event.key in (K_UP, K_w):
                    One.accelerate(3*math.pi/2)
            # more events go here
        
        for Object in ObjectDrawQueue:
            STAGE.blit(Object.sprite, Object.position)
        BACKGROUND.blit(STAGE, (0, 0))
        
        pygame.display.update()
        fpsClock.tick(FPS)

main()
