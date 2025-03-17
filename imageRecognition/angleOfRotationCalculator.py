import numpy as np
import math

def calculateAngleOfRotation(forwardsPoint, backwardsPoint, goalPoint):
    middlePoint = ((forwardsPoint[0] + backwardsPoint[0]) / 2, (forwardsPoint[1] + backwardsPoint[1]) / 2)
    angleOfRotation = math.atan2(goalPoint[1]-middlePoint[1], goalPoint[0]-middlePoint[0]) - math.atan2(forwardsPoint[1]-middlePoint[1], forwardsPoint[0] - middlePoint[0])

    return angleOfRotation

