import pygame, sys, math
from pygame.locals import *

# COLOR = (RRR, GGG, BBB)
BLACK   = (000, 000, 000)


CENTER = (200, 150)

ObjectDrawQueue = []

def inertia(Objects):
    for Object in Objects:
        Object.position[0] += Object.velocity[0]
        Object.position[1] += Object.velocity[1]
    # takes the velocity of all objects and moves them over time

class Player:
    def __init__(self, spawn = CENTER):
        self.sprite = pygame.image.load('test.png')
        self.hitBox = pygame.image.load('test.png')
        self.health = 100
        self.position = [spawn[0], spawn[1]]
        self.direction = 3 * math.pi / 2
        self.velocity = [0, 0]
        self.thrust = 1
        self.torque = 1
        ObjectDrawQueue.append(self)

    def turn(self, turn):
        if turn == left:
            pass
            # rotate direction clockwise
        if turn == right:
            pass
            # rotate direction counterclockwise
                
    def accelerate(self):
        self.velocity[0] += self.thrust * math.cos(self.direction)
        self.velocity[1] += self.thrust * math.sin(self.direction)
        
    def breaks(self):
        self.velocity[speed] -= self.thrust

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
    DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
    pygame.display.set_caption('Assteroids')

    One = Player()

    while True: # the main game loop 
        
        DISPLAYSURF.fill(BLACK)

        inertia(ObjectDrawQueue)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    One.turn(left)
                elif event.key in (K_SPACE, K_d):
                    One.breaks()
                elif event.key in (K_UP, K_w):
                    One.accelerate()
                elif event.key in (K_DOWN, K_s):
                    One.turn(right)
            # more events go here
        
        for Object in ObjectDrawQueue:
            DISPLAYSURF.blit(Object.sprite, Object.position)
        
        pygame.display.update()
        fpsClock.tick(FPS)

main()
