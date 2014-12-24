import pygame, sys, math
from pygame.locals import *

# COLOR = (RRR, GGG, BBB)
BLACK   = (000, 000, 000)


CENTER = (200, 150)

def movement(Object):
    pass
    # takes the velocity of all active objects and moves them over time

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
    DISPLAYSURF = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption('Assteroids')
    ActiveObjects = None

    # set up the colors
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE = (  0,   0, 255)
    



    while True: # the main game loop 
         
        # draw on the surface object
        DISPLAYSURF.fill(WHITE)
        pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
        pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
        pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
        pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)
        pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)
        pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)
        pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

        pixObj = pygame.PixelArray(DISPLAYSURF)
        pixObj[480][380] = BLACK
        pixObj[482][382] = BLACK
        pixObj[484][384] = BLACK
        pixObj[486][386] = BLACK
        pixObj[488][388] = BLACK
        del pixObj
        
        movement(ActiveObjects)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
             # more events go here

        pygame.display.update()
        fpsClock.tick(FPS)

main()
