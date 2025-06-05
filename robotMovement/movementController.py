import numpy as np

def getTurnSpeed(angleToTarget: float):
    return max(-100, min(100, angleToTarget**3*40+angleToTarget*50)) # x^(3)*40+x*50

# PID controller
def calculateSpeedAndRotation(distanceFromTarget, angleToTarget, state):
    if distanceFromTarget == None or angleToTarget == None:
        return (0, 0)
    # Robot should drive differently depending on state.
    if state == "SEARCH_BALLS":
        # Proportionality constants. Tune to change how fast speed changes
        kp_speed = 0.2

        goalDistanceFromBall = 20
        # Assuming that we use MoveSteering().on(steering, speed), the values range from -100 to 100, adjust below values accordingly
        forwardSpeed = max(5, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = getTurnSpeed(angleToTarget) 

    elif state == "TO_INTERMEDIARY":
        kp_speed = 0.2

        goalDistanceFromBall = 10
        forwardSpeed = max(40, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = getTurnSpeed(angleToTarget)

    elif state == "TO_GOAL":
        kp_speed = 0.2

        goalDistanceFromBall = 100
        forwardSpeed = max(0, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = getTurnSpeed(angleToTarget) 
    
    elif state == "TO_EXACT_ROTATION":
        forwardSpeed = getTurnSpeed(angleToTarget)
        turnSpeed = 100 if angleToTarget > 0 else -100
    

    return (turnSpeed, forwardSpeed)
    
