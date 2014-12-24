import pygame, sys, math
from pygame.locals import *

# COLOR = (RRR, GGG, BBB)
BLACK   = (000, 000, 000)


CENTER = (200, 150)

def movement():
    pass
    # takes the velocity of all objects and moves them over time

class Player:
    def __init__(spawn = CENTER):
        self.health = 100
        self.position = [spawn[0], spawn[1]]
        self.direction = math.pi / 2
        self.velocity = [0, 0]
        self.thrust = 1
        self.torque = 1

    def turn(self, turn):
        if turn == left:
            pass
            # rotate direction clockwise
        if turn == right:
            pass
            # rotate direction counterclockwise
                
    def accelerate(self):
        self.velocity[0] += self.thrust * math.cos(direction)
        self.velocity[1] += self.thrust * math.sin(direction)
        
    def breaks(self):
        self.velocity[speed] -= self.thrust

    def damage(self):
        pass

class Gun:
    def __init__():
        pass
    

def main():

    pygame.init()

    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    # set up the window
    DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
    pygame.display.set_caption('Assteroids')

    while True: # the main game loop 
        
        DISPLAYSURF.fill(BLACK)

        movement(ActiveObjects)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
             # more events go here

        pygame.display.update()
        fpsClock.tick(FPS)

main()
