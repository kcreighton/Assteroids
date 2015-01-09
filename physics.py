import math
from setup import *
from random import randint
from rigidBody import *
from utility import *

# called constantly # takes the velocity of all RigidBodies and moves them over time
# also tried to add basic hit detection (not working)
def physics(RigidBodyList):
    for Body in RigidBodyList:
        Body.position[0] += Body.velocity[0]
        Body.position[1] += Body.velocity[1]
        Body.center[0] += Body.velocity[0]
        Body.center[1] += Body.velocity[1]
        Body.lastCenter = [ (Body.center[0] - Body.velocity[0]*2), (Body.center[1] - Body.velocity[1]*2) ]
        for Body2 in RigidBodyList:
            if Body == Body2:
                pass
            elif Body.Owner == Body2 or Body2.Owner == Body:
                pass
            else:
                relativePosition = [None, None]
                relativePosition[0] = Body.center[0] - Body2.center[0]
                relativePosition[1] = Body.center[1] - Body2.center[1]
                distance = relativePosition[0] * relativePosition[0] + relativePosition[1] * relativePosition[1]
                width1 = (Body.size[0] - Body.size[0]/2)
                width2 = (Body2.size[0] - Body2.size[0]/2)
                minimumDistance = width1 + width2
                if distance <= (minimumDistance * minimumDistance):
                    Body.hit(Body2)
                    Body2.hit(Body)
