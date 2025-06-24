import numpy as np

def getTurnSpeed(angleToTarget, kpTurn=50, minTurn=-100, maxTurn=100):
    # turn = max(-100, min(100, angleToTarget**5*2+angleToTarget*40)) # x^(3)*40+x*50
    #turn += 2 if turn>0 else -2
    #turn = np.clip(turn, -100, 100)
    turn = np.clip(angleToTarget * kpTurn, a_min=minTurn, a_max=maxTurn)
    return turn


def getForwardSpeed(distanceToTarget, kpForward=0.1, minSpeed=-100, maxSpeed=100):
    return np.clip(distanceToTarget * kpForward, a_min=minSpeed, a_max=maxSpeed)


def calculateSpeedAndRotation(distanceFromTarget, angleToTarget, state):
    turnSpeed=0;forwardSpeed=0

    if state == "SEARCH_BALLS":
        # Proportionality constants. Tune to change how fast speed changes    
        if distanceFromTarget > 100:
            kp_forward = 0.2
            kp_turn = 30
            maxSpeed = 80
            turnSpeed = np.sign(angleToTarget) * 100
            if abs(angleToTarget) < 0.349: # 20 degrees
                turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
                forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
            elif abs(angleToTarget) < 0.785: # 45 degrees
                forwardSpeed = 15
            elif abs(angleToTarget) < np.pi/2: # 90 degrees
                forwardSpeed = 20
            else:
                forwardSpeed = maxSpeed

        else:
            kp_forward = 0.2
            kp_turn = 30
            maxSpeed = 25
            turnSpeed = np.sign(angleToTarget) * 100
            if abs(angleToTarget) < 0.0872: # 5 degrees
                turnSpeed = 0
                forwardSpeed = 10
            elif abs(angleToTarget) < 0.52: # 30 degrees
                forwardSpeed = 10
            elif abs(angleToTarget) < np.pi/2: # 90 degrees
                forwardSpeed = 15
            else:
                # turnSpeed = 0
                forwardSpeed = maxSpeed

            # # New approach to movement: Turn before moving
            # if angleToTarget < -0.0872665: # 5 degrees
            #     turnSpeed = -100
            #     forwardSpeed = 2
            #     if angleToTarget < -0.52: # 30 degrees
            #         forwardSpeed = 15
            # elif angleToTarget >= 0.0872665:
            #     turnSpeed = 100
            #     forwardSpeed = 2
            #     if angleToTarget > 0.52:
            #         forwardSpeed = 15
            # else: 
            #     # turnSpeed = 0
            #     turnSpeed = getTurnSpeed(angleToTarget * 2)
            #     forwardSpeed = 40


    elif state == "TO_INTERMEDIARY":
        kp_forward = 0.15

        # Testing new faster movement. Tune constants
        if distanceFromTarget > 50:
            kp_forward = 0.2
            kp_turn = 30
            maxSpeed = 80
            turnSpeed = np.sign(angleToTarget) * 100
            if abs(angleToTarget) < 0.349: # 20 degrees
                turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
                forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
            elif abs(angleToTarget) < 0.785: # 45 degrees
                forwardSpeed = 15
            elif abs(angleToTarget) < np.pi/2: # 90 degrees
                forwardSpeed = 20
            else:
                forwardSpeed = maxSpeed

        else:
            kp_forward = 0.2
            kp_turn = 30
            maxSpeed = 25
            turnSpeed = np.sign(angleToTarget) * 100
            if abs(angleToTarget) < 0.0872: # 5 degrees
                turnSpeed = 0
                forwardSpeed = 10
            elif abs(angleToTarget) < 0.52: # 30 degrees
                forwardSpeed = 10
            elif abs(angleToTarget) < np.pi/2: # 90 degrees
                forwardSpeed = 15
            else:
                # turnSpeed = 0
                forwardSpeed = maxSpeed

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
        
        # if distanceFromTarget > 50:
        kp_forward = 0.2
        kp_turn = 30
        maxSpeed = 80
        turnSpeed = np.sign(angleToTarget) * 100
        if abs(angleToTarget) < 0.349: # 20 degrees
            turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
            forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
        elif abs(angleToTarget) < 0.785: # 45 degrees
            forwardSpeed = 15
        elif abs(angleToTarget) < np.pi/2: # 90 degrees
            forwardSpeed = 20
        else:
            forwardSpeed = maxSpeed

        # else:
        #     kp_forward = 0.2
        #     kp_turn = 30
        #     maxSpeed = 25
        #     turnSpeed = np.sign(angleToTarget) * 100
        #     if abs(angleToTarget) < 0.0872: # 5 degrees
        #         turnSpeed = 0
        #         forwardSpeed = 10
        #     elif abs(angleToTarget) < 0.52: # 30 degrees
        #         forwardSpeed = 10
        #     elif abs(angleToTarget) < np.pi/2: # 90 degrees
        #         forwardSpeed = 15
        #     else:
        #         # turnSpeed = 0
        #         forwardSpeed = maxSpeed

        # kp_forward = 0.25
        # kp_turn = 30
        # maxSpeed = 60
        # turnSpeed = np.sign(angleToTarget) * 100
        # if abs(angleToTarget) < 0.349: # 20 degrees
        #     turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
        #     forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
        # elif abs(angleToTarget) < 0.785: # 45 degrees
        #     forwardSpeed = 30
        # elif abs(angleToTarget) < np.pi/2: # 90 degrees
        #     forwardSpeed = 50
        # else:
        #     forwardSpeed = maxSpeed

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
        kp_speed = 0.15

        goalDistanceFromBall = 130

        # New approach to movement
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
            turnSpeed = getTurnSpeed(angleToTarget)
            forwardSpeed = 10
            if distanceFromTarget < 110:
                forwardSpeed = 0
    # Comp Zoom Zoom
    # elif state == "TO_GOAL":
    #     kp_forward = 0.15
        
    #     # New to goal
    #     turnSpeed = np.sign(angleToTarget) * 100
    #     if abs(angleToTarget) < 0.0436: # 2.5 degrees
    #         # turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
    #         # forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=80)
    #         turnSpeed = 0
    #         forwardSpeed = 5
    #     elif abs(angleToTarget) < 0.0872: # 5 degrees
    #         forwardSpeed = 2 # 2
    #     elif abs(angleToTarget) < 0.174: # 10 degrees
    #         forwardSpeed = 3 # 3
    #     elif abs(angleToTarget) < np.pi/2:
    #         forwardSpeed = 5  # 5
    #     else:
    #         forwardSpeed = 10

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
        forwardSpeed = -50
        turnSpeed = 0

    elif state == "COLLECT_BALL":
        # kp_forward = 0.05
        kp_turn = 100

        if distanceFromTarget > 150:
            kp_forward = 0.2
            kp_turn = 30
            maxSpeed = 45
            turnSpeed = np.sign(angleToTarget) * 100
            if abs(angleToTarget) < 0.349: # 20 degrees
                turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
                forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
            elif abs(angleToTarget) < 0.785: # 45 degrees
                forwardSpeed = 25
            elif abs(angleToTarget) < np.pi/2: # 90 degrees
                forwardSpeed = 30
            else:
                forwardSpeed = maxSpeed

        else:
            # New approach to movement
            if angleToTarget < -0.0872665:
                turnSpeed = -100
                forwardSpeed = 2
                if angleToTarget < -0.52:
                    forwardSpeed = 10
                    if angleToTarget > -0.785:
                        forwardSpeed = 15
                        if angleToTarget > -np.pi/2:
                            forwardSpeed = 20
            elif angleToTarget >= 0.0872665:
                turnSpeed = 100
                forwardSpeed = 2
                if angleToTarget > 0.52:
                    forwardSpeed = 10
                    if angleToTarget > 0.785:
                        forwardSpeed = 15
                        if angleToTarget > np.pi/2:
                            forwardSpeed = 20
            else: 
                # turnSpeed = 0
                turnSpeed = getTurnSpeed(angleToTarget * 6)
                forwardSpeed = 10



    elif state == "COLLECT_BALL_BORDER":
        # kp_forward = 0.05
        # kp_turn = 100


        # if distanceFromTarget > 100:
        #     kp_forward = 0.2
        #     kp_turn = 80
        #     maxSpeed = 80
        #     turnSpeed = np.sign(angleToTarget) * 100
        #     if abs(angleToTarget) < 0.349: # 20 degrees
        #         turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
        #         forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
        #     elif abs(angleToTarget) < 0.785: # 45 degrees
        #         forwardSpeed = 15
        #     elif abs(angleToTarget) < np.pi/2: # 90 degrees
        #         forwardSpeed = 20
        #     else:
        #         forwardSpeed = maxSpeed

        # else:
        #     kp_forward = 0.2
        #     kp_turn = 30
        #     maxSpeed = 25
        #     turnSpeed = np.sign(angleToTarget) * 100
        #     if abs(angleToTarget) < 0.0872: # 5 degrees
        #         turnSpeed = 0
        #         forwardSpeed = 10
        #     elif abs(angleToTarget) < 0.52: # 30 degrees
        #         forwardSpeed = 10
        #     elif abs(angleToTarget) < np.pi/2: # 90 degrees
        #         forwardSpeed = 15
        #     else:
        #         # turnSpeed = 0
        #         forwardSpeed = maxSpeed

        # WORKS --------------------------------------------------
        if distanceFromTarget > 150:
            kp_forward = 0.2
            kp_turn = 30
            maxSpeed = 45
            turnSpeed = np.sign(angleToTarget) * 100
            if abs(angleToTarget) < 0.349: # 20 degrees
                turnSpeed = getTurnSpeed(angleToTarget, kp_turn)
                forwardSpeed = getForwardSpeed(distanceFromTarget, kp_forward, minSpeed=30, maxSpeed=maxSpeed)
            elif abs(angleToTarget) < 0.785: # 45 degrees
                forwardSpeed = 25
            elif abs(angleToTarget) < np.pi/2: # 90 degrees
                forwardSpeed = 30
            else:
                forwardSpeed = maxSpeed

        else:
            # New approach to movement
            if angleToTarget < -0.0872665:
                turnSpeed = -100
                forwardSpeed = 2
                if angleToTarget < -0.52:
                    forwardSpeed = 10
                    if angleToTarget > -0.785:
                        forwardSpeed = 15
                        if angleToTarget > -np.pi/2:
                            forwardSpeed = 20
            elif angleToTarget >= 0.0872665:
                turnSpeed = 100
                forwardSpeed = 2
                if angleToTarget > 0.52:
                    forwardSpeed = 10
                    if angleToTarget > 0.785:
                        forwardSpeed = 25
                        if angleToTarget > np.pi/2:
                            forwardSpeed = 35
            else: 
                # turnSpeed = 0
                turnSpeed = getTurnSpeed(angleToTarget * 6)
                forwardSpeed = 20

                
    elif state == "LOST":
        # Special temporary state for when we have less than two corners detected
        # Simply drive forwards, hoping for the corners to come back
        forwardSpeed = 20


    return (turnSpeed, forwardSpeed)
    