import numpy as np

def getTurnSpeed(angleToTarget: float):
    # return max(-100, min(100, angleToTarget**3*40+angleToTarget*50)) # x^(3)*40+x*50
    
    # Try tuning constant.
    kpTurn = 20
    turnSpeed = kpTurn * angleToTarget

    # Try capping turn speed at eg. 50. Maybe not, as this would not allow for turning in place. Test?
    # return max(-50, min(50, turnSpeed))

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
        
        # Try limiting forwardSpeed as it determines the speed at which we turn. Maybe especially limit it at large angles? And no limit or lower limit when angle is small enough? 
        # Try not moving forward until angle is satisfyingly small? Probably slow, but probably effective.
        forwardSpeed = max(10, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
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
    

    return (turnSpeed, forwardSpeed)
    
