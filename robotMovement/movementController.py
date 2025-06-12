import numpy as np

def getTurnSpeed(angleToTarget: float):
    turn = max(-100, min(100, angleToTarget**5*2+angleToTarget*40)) # x^(3)*40+x*50
    #turn += 2 if turn>0 else -2
    #turn = np.clip(turn, -100, 100)
    return turn

# PID controller
def calculateSpeedAndRotation(distanceFromTarget, angleToTarget, state):
    turnSpeed=0;forwardSpeed=0
    #if distanceFromTarget == None or angleToTarget == None:
    #    return (0, 0)
    # Robot should drive differently depending on state.
    if state == "SEARCH_BALLS":
        # Proportionality constants. Tune to change how fast speed changes
        kp_speed = 0.15

        goalDistanceFromBall = 10
        # Assuming that we use MoveSteering().on(steering, speed), the values range from -100 to 100, adjust below values accordingly
        # forwardSpeed = max(5, min(80, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        # turnSpeed = getTurnSpeed(angleToTarget) 

        # New approach to movement: Turn before moving
        if angleToTarget < -0.0872665:
            turnSpeed = -100
            forwardSpeed = 2
            if angleToTarget < -0.52:
                forwardSpeed = 15
        elif angleToTarget >= 0.0872665:
            turnSpeed = 100
            forwardSpeed = 2
            if angleToTarget > 0.52:
                forwardSpeed = 15
        else: 
            turnSpeed = 0
            forwardSpeed = 40


    elif state == "TO_INTERMEDIARY":
        kp_speed = 0.15

        goalDistanceFromBall = 10
        forwardSpeed = max(5, min(80, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = getTurnSpeed(angleToTarget)

    elif state == "TO_GOAL":
        kp_speed = 0.15

        goalDistanceFromBall = 100
        forwardSpeed = max(0, min(80, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnSpeed = getTurnSpeed(angleToTarget) 
    
    elif state == "TO_EXACT_ROTATION":
        forwardSpeed = getTurnSpeed(angleToTarget)/8
        forwardSpeed += 3 if forwardSpeed>0 else -3
        turnSpeed = -100 if angleToTarget > 0 else 100
    

    return (turnSpeed, forwardSpeed)
    
