import numpy as np
import math

def calculateAngleOfRotation(forwardsPoint, backwardsPoint, goalPoint):
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