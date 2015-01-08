import math
from setup import *
from random import randint
from rigidBody import *
from utility import *

# called constantly # takes the velocity of all RigidBodies and moves them over time
def physics(RigidBodyList):
    for Body in RigidBodyList:
        Body.position[0] += Body.velocity[0]
        Body.position[1] += Body.velocity[1]
        Body.center[0] += Body.velocity[0]
        Body.center[1] += Body.velocity[1]
        Body.lastCenter = [ (Body.center[0] - Body.velocity[0]*2), (Body.center[1] - Body.velocity[1]*2) ]
        CollisionList[0] = Body
        for Body2 in RigidBodyList:
            CollisionList[1] = Body2
            # collision detection
        
