import pygame

# COLORS  = (RRR, GGG, BBB, AAA)
BLACK     = (000, 000, 000)
WHITE     = (255, 255, 255)
LASER_RED = (255, 000, 000, 100)
CLEAR     = (000, 000, 000, 000)

WINDOWWIDTH = 1340
WINDOWHEIGHT = 700
CENTER = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

BUTTASSPATH = ".\images\ButtAssSmall.png"
DONKEYASSPATH = ".\images\ButtDonkeySmall.png"

# set up the stage
BACKGROUND = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
STAGE = BACKGROUND.convert_alpha()
pygame.display.set_caption('Assteroids')
ObjectDrawQueue = [] # placment list
BadAssList = []
GoodAssList = []
CollisionList = [None, None]
