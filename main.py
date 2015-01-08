import pygame
from pygame.locals import *
from random import randint
from rigidBody import *
from utility import *
from setup import *
from actor import *
from guns import *
from physics import *

def main():
    pygame.init()

# frames per second setting
    FPS = 60
    fpsClock = pygame.time.Clock()

# create props
    One = Actor(pygame.image.load('test.png'))
    ObjectDrawQueue.append(One)
    Rifle = Kinetic(One)
    Rifle.propulsion = 60
    
    # quick random gen (implement better later)
    count = 0

# the main game loop
    while True:
    # clear stage
        BACKGROUND.fill(BLACK)
        STAGE.fill(CLEAR)
        
    # constant events (called every loop)
        physics(ObjectDrawQueue)
        #fov(One) NOT IMPLEMENTED
        One.adjustAim(pygame.mouse.get_pos()) # make AI controller for this
        
        # quick random gen (implement better later)
        count += 1
        if count == 60:
            newAss()
            count = 0
    # continuous events (toggled events)
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
            scanStart = Object.position
            if Object.trail == True:
                pygame.draw.line(STAGE, WHITE, Object.lastCenter, Object.center, 2)
            STAGE.blit(Object.sprite, Object.position)
            
    # take picture
        BACKGROUND.blit(STAGE, (0, 0))
        pygame.display.update()
        fpsClock.tick(FPS)
    
main()
