import numpy as np

def getTurnSpeed(angleToTarget: float):
    turn = max(-100, min(100, angleToTarget**5*2+angleToTarget*30)) # x^(3)*40+x*50
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
            turnStrength = getTurnSpeed(angleToTarget)
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
        kp_speed = 0.15

        goalDistanceFromBall = 10
        engineSpeeds = max(40, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnStrength = getTurnSpeed(angleToTarget) 

    elif state == "TO_GOAL":
        kp_speed = 0.15

        goalDistanceFromBall = 100
        engineSpeeds = max(0, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)))
        turnStrength = getTurnSpeed(angleToTarget) 
    
    elif state == "TO_EXACT_ROTATION":
        forwardSpeed = getTurnSpeed(angleToTarget)/8
        forwardSpeed += 3 if forwardSpeed>0 else -3
        turnSpeed = -100 if angleToTarget > 0 else 100
    

    return (turnStrength, engineSpeeds)
    
