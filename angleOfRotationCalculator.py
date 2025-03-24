import numpy as np
import math

def calculateAngleOfRotation(forwardsPoint, backwardsPoint, goalPoint):
    middlePoint = ((forwardsPoint[0] + backwardsPoint[0]) / 2, (forwardsPoint[1] + backwardsPoint[1]) / 2)
    angleOfRotation = math.atan2(goalPoint[1]-middlePoint[1], goalPoint[0]-middlePoint[0]) - math.atan2(forwardsPoint[1]-middlePoint[1], forwardsPoint[0] - middlePoint[0])

    return angleOfRotation

point1 = (2,2)
point2 = (1,1)
goalPoint = (1, 1.1)

angle = calculateAngleOfRotation(point1, point2, goalPoint)
print(angle)