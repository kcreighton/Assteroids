import pygame
from setup import *
from random import randint


def randomLocation():
    x = randint(0, WINDOWWIDTH)
    y = randint(0, WINDOWHEIGHT)
    return [x, y]

def randomVelocity(rangeX = 5, rangeY = 5):
    x = randint(-rangeX, rangeX)
    y = randint(-rangeY, rangeY)
    return [x, y]
