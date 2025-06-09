import numpy as np

def getTurnSpeed(angleToTarget: float):
    # return max(-100, min(100, angleToTarget**3*40+angleToTarget*50)) # x^(3)*40+x*50
    
    # Try tuning constant.
    kpTurn = 20
    turnStrength = kpTurn * angleToTarget

    return turnStrength

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
        
        # Try limiting engineSpeeds as it determines the speed at which we turn. Maybe especially limit it at large angles? And no limit or lower limit when angle is small enough? 
        # Try not moving forward until angle is satisfyingly small? Probably slow, but probably effective.
        
        # If distance is large, turn before moving
        if distanceFromTarget > 100:

            turnStrength = getTurnSpeed(angleToTarget) 
            if angleToTarget < -0.0872665:
                engineSpeeds = 2
                if angleToTarget < -0.785:
                    engineSpeeds = 10
                turnStrength = -100
            elif angleToTarget >= 0.0872665:
                engineSpeeds = 2
                if angleToTarget > 0.785:
                    engineSpeeds = 10
                turnStrength = 100
            else: 
                turnStrength = 0
                engineSpeeds = 20

        # Adjust forward speed depending on angle. Only drive forwards if angle is small enough
        # engineSpeeds = max(5, min(5, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        

    elif state == "TO_INTERMEDIARY":
        kp_speed = 0.2

        goalDistanceFromBall = 10
        engineSpeeds = max(40, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnStrength = getTurnSpeed(angleToTarget) 

    elif state == "TO_GOAL":
        kp_speed = 0.2

        goalDistanceFromBall = 100
        engineSpeeds = max(0, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnStrength = getTurnSpeed(angleToTarget) 
    

    return (turnStrength, engineSpeeds)
    
