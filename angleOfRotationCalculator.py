import numpy as np
import math

def rotatePointsAroundMidPoint(p1, p2):
    middlePoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    # Translate both points to be around origo by subtracting mid point from them
    translatedp1 = (p1[0] - middlePoint[0], p1[1] - middlePoint[1])
    translatedp2 = (p2[0] - middlePoint[0], p2[1] - middlePoint[1])

    rotatedp1 = (-translatedp1[1], translatedp1[0])
    rotatedp2 = (-translatedp2[1], translatedp2[0])

    reTranslatedp1 = (rotatedp1[0] + middlePoint[0], rotatedp1[1] + middlePoint[1])
    reTranslatedp2 = (rotatedp2[0] + middlePoint[0], rotatedp2[1] + middlePoint[1])

    return reTranslatedp1, reTranslatedp2



def calculateAngleOfRotation(forwardsPoint, backwardsPoint, goalPoint):
    # Rotate points 90 degrees so they properly point forwards and backwards (This is to the color paper being sideways into account)
    forwardsPoint, backwardsPoint = rotatePointsAroundMidPoint(forwardsPoint, backwardsPoint)
    
    middlePoint = ((forwardsPoint[0] + backwardsPoint[0]) / 2, (forwardsPoint[1] + backwardsPoint[1]) / 2)    
    angleOfRotation = math.atan2(goalPoint[1]-middlePoint[1], goalPoint[0]-middlePoint[0]) - math.atan2(forwardsPoint[1]-middlePoint[1], forwardsPoint[0] - middlePoint[0])

    # New attempt at calculation
    # middlePoint = ((forwardsPoint[0] + backwardsPoint[0]) / 2, (forwardsPoint[1] + backwardsPoint[1]) / 2)
    # MGVector = (goalPoint[0] - middlePoint[0], goalPoint[1] - middlePoint[1])
    # backToFrontVector = (forwardsPoint[0] - backwardsPoint[0], forwardsPoint[0] - backwardsPoint[0])

    # angleOfRotation = math.atan2(MGVector[1], MGVector[0]) - math.atan2(backToFrontVector[1], backToFrontVector[0])

    # Normalize angle to the range (-π, π]
    if angleOfRotation > math.pi:
        angleOfRotation -= 2 * math.pi
    elif angleOfRotation <= -math.pi:
        angleOfRotation += 2 * math.pi

    return angleOfRotation

point2 = (2,2)
point1 = (1,1)
goalPoint = (1, 3)

angle = calculateAngleOfRotation(point1, point2, goalPoint)
print(angle)