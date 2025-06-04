import numpy as np

# PID controller
def calculateSpeedAndRotation(distanceFromTarget, angleToTarget, state):
    if distanceFromTarget == None or angleToTarget == None:
        return (0, 0)
    # Robot should drive differently depending on state.
    if state == "SEARCH_BALLS":
        # Proportionality constants. Tune to change how fast speed changes
        kp_speed = 0.2
        #kp_turn = 200

        goalDistanceFromBall = 20
        goalAngleToBall = 0
        # Assuming that we use MoveSteering().on(steering, speed), the values range from -100 to 100, adjust below values accordingly
        forwardSpeed = max(5, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = max(-100, min(100, angleToTarget**3*40+angleToTarget*50)) # x^(3)*40+x*50

    elif state == "TO_INTERMEDIARY":
        kp_speed = 0.2
        kp_turn = 200

        goalDistanceFromBall = 10
        goalAngleToBall = 0

        forwardSpeed = max(40, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = max(-100, min(100, kp_turn * (angleToTarget - goalAngleToBall))) 

    elif state == "TO_GOAL":
        kp_speed = 0.2
        kp_turn = 200

        goalDistanceFromBall = 100
        goalAngleToBall = 0

        forwardSpeed = max(0, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = max(-100, min(100, kp_turn * (angleToTarget - goalAngleToBall))) 
    
    



    return (turnSpeed, forwardSpeed)
    
