import numpy as np

def getTurnSpeed(angleToTarget, kpTurn=50, minTurn=-100, maxTurn=100):
    # kpTurn = 50
    # turn = max(-100, min(100, angleToTarget**5*2+angleToTarget*40)) # x^(3)*40+x*50
    #turn += 2 if turn>0 else -2
    #turn = np.clip(turn, -100, 100)
    turn = np.clip(angleToTarget * kpTurn, a_min=minTurn, a_max=maxTurn)
    return turn


def getForwardSpeed(distanceToTarget, kpForward=0.1, minSpeed=-100, maxSpeed=100):
    return np.clip(distanceToTarget * kpForward, a_min=minSpeed, a_max=maxSpeed)


def getRotationSign(angleToTarget):
    if angleToTarget >= 0:
        return 1
    else:
        return -1



def calculateSpeedAndRotation(distanceFromTarget, angleToTarget, state):
    turnSpeed=0;forwardSpeed=0
    
    if state == "SEARCH_BALLS":
        # Proportionality constants. Tune to change how fast speed changes
        kp_forward = 0.15
        
        # Assuming that we use MoveSteering().on(steering, speed), the values range from -100 to 100, adjust below values accordingly
        # forwardSpeed = max(5, min(80, kp_forward * (distanceFromTarget - goalDistanceFromBall)))
        # turnSpeed = getTurnSpeed(angleToTarget) 

        # New approach to movement: Turn before moving
        if angleToTarget < -0.0872665: # 5 degrees
            turnSpeed = -100
            forwardSpeed = 2
            if angleToTarget < -0.52: # 30 degrees
                forwardSpeed = 15
        elif angleToTarget >= 0.0872665:
            turnSpeed = 100
            forwardSpeed = 2
            if angleToTarget > 0.52:
                forwardSpeed = 15
        else: 
            # turnSpeed = 0
            turnSpeed = getTurnSpeed(angleToTarget)
            forwardSpeed = 40


    elif state == "TO_INTERMEDIARY":
        kp_forward = 0.15

        # Testing new faster movement. Tune constants
        if distanceFromTarget > 200:
            kp_forward = 0.25
            kp_turn = 30
            turnSpeed = getRotationSign(angleToTarget) * 100
            if abs(angleToTarget < 0.349):
                turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
                forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=80)
            elif abs(angleToTarget < 0.785):
                forwardSpeed = 30
            elif abs(angleToTarget < np.pi/2):
                forwardSpeed = 50
            else:
                forwardSpeed = 80
        else:
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
                # turnSpeed = 0
                turnSpeed = getTurnSpeed(angleToTarget)
                # forwardSpeed = 30
                forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=10, maxSpeed=80)

        # # New approach to movement
        # if angleToTarget < -0.0872665:
        #     turnSpeed = -100
        #     forwardSpeed = 2
        #     if angleToTarget < -0.52:
        #         forwardSpeed = 15
        # elif angleToTarget >= 0.0872665:
        #     turnSpeed = 100
        #     forwardSpeed = 2
        #     if angleToTarget > 0.52:
        #         forwardSpeed = 15
        # else: 
        #     # turnSpeed = 0
        #     turnSpeed = getTurnSpeed(angleToTarget)
        #     forwardSpeed = 30


    # Testing new faster movement. Tune constants
    elif state == "TO_OA_INTERMEDIARY":
        kp_forward = 0.25
        kp_turn = 30
        turnSpeed = getRotationSign(angleToTarget) * 100
        if abs(angleToTarget < 0.349):
            turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
            forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=80)
        elif abs(angleToTarget < 0.785):
            forwardSpeed = 30
        elif abs(angleToTarget < np.pi/2):
            forwardSpeed = 50
        else:
            forwardSpeed = 80
        

        # New approach to movement
        # if angleToTarget < -0.349: # 20 degrees
        #     turnSpeed = -100
        #     forwardSpeed = 2
        #     if angleToTarget < -0.52: # 30 degrees
        #         forwardSpeed = 15
        # elif angleToTarget >= 0.349:
        #     turnSpeed = 100
        #     forwardSpeed = 2
        #     if angleToTarget > 0.52:
        #         forwardSpeed = 15
        # else: 
        #     # turnSpeed = 0
        #     turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
        #     # forwardSpeed = 30
        #     forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, s_min=30, s_max=100)


    elif state == "TO_GOAL":
        kp_forward = 0.15
        
        # New to goal
        turnSpeed = getRotationSign(angleToTarget) * 100
        if abs(angleToTarget) < 0.0436: # 2.5 degrees
            # turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
            # forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=80)
            turnSpeed = 0
            forwardSpeed = 5
        elif abs(angleToTarget) < 0.0872: # 5 degrees
            forwardSpeed = 2
        elif abs(angleToTarget) < 0.174: # 10 degrees
            forwardSpeed = 3
        elif abs(angleToTarget) < np.pi/2:
            forwardSpeed = 5
        else:
            forwardSpeed = 10
        
        # New approach to movement
        # if angleToTarget < -0.0872665:
        #     turnSpeed = -100
        #     forwardSpeed = 2
        #     if angleToTarget < -0.52:
        #         forwardSpeed = 15
        # elif angleToTarget >= 0.0872665:
        #     turnSpeed = 100
        #     forwardSpeed = 2
        #     if angleToTarget > 0.52:
        #         forwardSpeed = 15
        # else: 
        #     turnSpeed = getTurnSpeed(angleToTarget*4)
        #     forwardSpeed = 25
        #     if distanceFromTarget < 110:
        #         forwardSpeed = 0
            # turnSpeed = 0
            # forwardSpeed = 10

        # forwardSpeed = max(0, min(80, kp_forward * (distanceFromTarget - goalDistanceFromBall)))
        # turnSpeed = getTurnSpeed(angleToTarget) 
        # forwardSpeed = 10
        if distanceFromTarget < 110:
            forwardSpeed = 0
    
    elif state == "TO_EXACT_ROTATION":
        forwardSpeed = np.abs(getTurnSpeed(angleToTarget)/8)
        np.clip(forwardSpeed + 2, a_min=0, a_max=100)
        turnSpeed = 100 if angleToTarget > 0 else -100
        
    elif state == "BACKOFF":
        forwardSpeed = -30
        turnSpeed = 0

    elif state == "COLLECT_BALL":
        kp_forward = 0.05

        # New approach to movement
        if angleToTarget < -0.0872665:
            turnSpeed = -100
            forwardSpeed = 2
            if angleToTarget < -0.52:
                forwardSpeed = 5
        elif angleToTarget >= 0.0872665:
            turnSpeed = 100
            forwardSpeed = 2
            if angleToTarget > 0.52:
                forwardSpeed = 5
        else: 
            # turnSpeed = 0
            turnSpeed = getTurnSpeed(angleToTarget)
            forwardSpeed = 10


    return (turnSpeed, forwardSpeed)
    