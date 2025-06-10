import numpy as np

def getTurnStrength(angleToTarget: float):
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

        goalDistanceFromBall = 0

        # Maybe change enginespeeds if ball is very close?
        
        # Choose one of the below movement styles. Comment out the other.
        # -----------------------------------------------------------------------------------------------
        # Normal movement but with turning first if angle is high (and significantly reduced speed)
        if angleToTarget < -0.52:
            turnStrength = -100
            engineSpeeds = 15
        elif angleToTarget >= 0.52:
            turnStrength = 100
            engineSpeeds = 15
        else:
            turnStrength = getTurnStrength(angleToTarget)
            engineSpeeds = max(5, min(30, kp_speed * (distanceFromTarget - goalDistanceFromBall)))

        # --------------------------------------------------------------------------------------------------
        # New approach to movement; Turn before moving
        # if angleToTarget < -0.0872665:
        #     turnStrength = -100
        #     engineSpeeds = 2
        #     if angleToTarget < -0.52:
        #         engineSpeeds = 15
        # elif angleToTarget >= 0.0872665:
        #     turnStrength = 100
        #     engineSpeeds = 2
        #     if angleToTarget > 0.52:
        #         engineSpeeds = 15
        # else: 
        #     turnStrength = 0
        #     engineSpeeds = 40

        # --------------------------------------------------------------------------------------------------

        

    elif state == "TO_INTERMEDIARY":
        kp_speed = 0.2

        goalDistanceFromBall = 10
        engineSpeeds = max(40, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnStrength = getTurnStrength(angleToTarget) 

    elif state == "TO_GOAL":
        kp_speed = 0.2

        goalDistanceFromBall = 100
        engineSpeeds = max(0, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnStrength = getTurnStrength(angleToTarget) 
    

    return (turnStrength, engineSpeeds)
    
