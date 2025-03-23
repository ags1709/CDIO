import numpy as np


def calculateSpeedAndRotation(distanceFromBall, angleToBall):
    # Proportionality constants. Tune to change how fast speed changes
    kp_speed = 0.1
    kp_turn = 50

    targetDistanceFromBall = 20
    targetAngleToBall = 0

    # Assuming that we use MoveSteering().on(steering, speed), the values range from -100 to 100, adjust below values accordingly
    forwardSpeed = max(5, min(100, kp_speed * (distanceFromBall - targetDistanceFromBall)))
    turnSpeed = max(-50, min(50, kp_turn * (angleToBall - targetAngleToBall))) 

    return (turnSpeed, forwardSpeed)
    
