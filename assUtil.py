import pygame, sys, math
from pygame.locals import *
from random import randint
import assConstants

def randomLocation():
    x = randint(0, assConstants.WINDOWWIDTH)
    y = randint(0, assConstants.WINDOWHEIGHT)
    return [x, y]

def randomVelocity(rangeX = 5, rangeY = 5):
    x = randint(-rangeX, rangeX)
    y = randint(-rangeY, rangeY)
    return [x, y]
