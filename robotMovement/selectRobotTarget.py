from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation, calculateAngleOfTwoPoints
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from imageRecognition.positionEstimator import CrossInfo, findIntermediatyCrossPoint, analyze_point_with_polygon
import numpy as np
import cv2
from robotMovement.tools import tuple_toint
import math
import numpy as np
from robotMovement.obstacleAvoidance import avoidObstacle
import time
import threading
from imageRecognition.positionEstimator import estimateGoals, estimateCross, estimatePlayArea, estimatePlayAreaIntermediate, analyze_point_with_polygon, CrossInfo, is_point_in_polygon

abort = False
firstimer = True

def setAbort(): 
    global abort
    abort = True
    

# States for state machine. Can be expanded later to handle situations calling for specific behaviour like getting ball from corner/cross.
SEARCH_BALLS = "SEARCH_BALLS"
TO_INTERMEDIARY = "TO_INTERMEDIARY"
TO_OA_INTERMEDIARY = "TO_OA_INTERMEDIARY"
TO_GOAL = "TO_GOAL"
TO_EXACT_ROTATION = "TO_EXACT_ROTATION"
BACKOFF = "BACKOFF"
COLLECT_BALL = "COLLECT_BALL"
COLLECT_BALL_BORDER = "COLLECT_BALL_BORDER"
VOMIT = "VOMIT"
WAIT = "WAIT"
LOST = "LOST"

stateQueue = [ # Format: (State,variables)
    
]

# SEARCH_BALLS
targetBall = None
# def log_state_transition(state: str, file_path: str = "state_transitions.txt"):
#     with open(file_path, "a") as f:
#         f.write(f"{state}\n")


def goToGoalIntermidararyPoint(detectedObjects, robotPos):
    intermediaryPoint = detectedObjects["goals"][0] + detectedObjects["goalNormals"][0] * 150
    stateQueue.clear()
    if abort:
        stateQueue.append(BACKOFF, robotPos[0], 100)
    handleOA(robotPos, intermediaryPoint, detectedObjects)
    stateQueue.append((TO_INTERMEDIARY, intermediaryPoint))
    stateQueue.append((TO_GOAL,)) # Comma to make it a tuple


def is_objectmiddle_in_circle(objectpos, center, radius):
    #middle = ( (objectpos[0][0] + objectpos[1][0])/2, (objectpos[0][1] + objectpos[1][1])/2 )
    point = np.array(objectpos)
    center = np.array(center)
    distance_squared = np.sum((point - center) ** 2)
    return distance_squared <= radius ** 2

def is_objectmiddle_close_circle(objectpos, center, radius):
    #middle = ( (objectpos[0][0] + objectpos[1][0])/2, (objectpos[0][1] + objectpos[1][1])/2 )
    point = np.array(objectpos)
    center = np.array(center)
    distance_squared = np.sum((point - center) ** 2)
    return distance_squared <= radius ** 2

def add_angle(a1, a2):
    return (a1 + a2 + np.pi) % (2*np.pi) - np.pi


def handleOA(pos, target, objects):
    path = avoidObstacle(pos[0], target, objects["cross"])

    # If an obstacle is in the way but no valid path is found, do nothing but print alert.
    if path is None:
        print("WARNING: Obstacle in way, but no viable path found")

    # If necessary, calculates intermediary points to navigate to before going to target and adds them to state queue
    elif path != [target]:
        print("Obstacle in the way, navigating to intermediary point(s)")
        for OAIP in reversed(path[:-1]):
            stateQueue.insert(0, (TO_OA_INTERMEDIARY, OAIP))

def calcDistAndAngleToTarget(detectedObjects, crossInfo: CrossInfo, playAreaIntermediate: list[tuple[float, float]], frame):


    global targetBall; global stateQueue; global abort; global targetBallMemory
        
    robotDistance = 0
    robotAngle = 0

    # If no state has been set yet, put robot in ball searching state.
    if len(stateQueue) == 0:
        stateQueue.append((SEARCH_BALLS,))

    state = stateQueue[0][0] # State
    stateVariables = stateQueue[0][1:] # Variables for state

    # This is the two points used to identify the robots position. 
    robotPos = calculateRobotPositionFlexible(detectedObjects["frontLeftCorner"], detectedObjects["frontRightCorner"], detectedObjects["backLeftCorner"], detectedObjects["backRightCorner"])
    if robotPos is None:
        # We don't know where the robot is, use the temporary LOST state
        if state != LOST: stateQueue.insert(0, (LOST,))
        return robotDistance, robotAngle, LOST
    elif state == LOST:
        # We found the robot again, remove the LOST state
        stateQueue.pop(0)
        state, stateVariables = stateQueue[0][0], stateQueue[0][1:]
    # robotMiddle = ((robotPos[0][0] + robotPos[1][0]) / 2, (robotPos[0][1] + robotPos[1][1]) / 2)
    robotRotation = calculateAngleOfTwoPoints(robotPos[1], robotPos[0])
    
    if abort:
        goToGoalIntermidararyPoint(detectedObjects, robotPos)
        abort = False

    
    global firstimer
    # Use state machine to dictate robots target based on its state
    if state == SEARCH_BALLS:
        # TODO: WARNING! CHECK THAT THE TARGET BALL HAS NOT MOVED TOO MUCH!!!! HERE WE ASSUME IT IS STATIONARY WHICH IS BAAAAD
        # log_state_transition(SEARCH_BALLS)

        # ballcount = len(detectedObjects["orangeBalls"]) + len(detectedObjects["whiteBalls"])
        
        # If we're explicitly given a ball to go for
        if len(stateVariables) > 0:
            targetBall = stateVariables[0]

        # Else, find the closest ball
        else:
            if len(detectedObjects["whiteBalls"]) > 0:
                targetBall = min(detectedObjects["whiteBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
                handleBallTargetIntermediate(crossInfo, playAreaIntermediate, detectedObjects, robotPos, frame)

            # If the robot needs to go to goal 2 times, this needs to be moved over the white balls
            elif len(detectedObjects["orangeBalls"]) > 0: # and ballcount <= 6
                targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
                handleBallTargetIntermediate(crossInfo, playAreaIntermediate, detectedObjects, robotPos, frame)

            # If no balls are present, move to intermediary point in preperation for turning in balls
            else:
                print("No balls")
                goToGoalIntermidararyPoint(detectedObjects, robotPos)

        # Calculate distance and angle to the selected ball
        if targetBall is not None:
            handleOA(robotPos, targetBall, detectedObjects)
            robotDistance = calculateDistance(robotPos[0], targetBall)
            robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], targetBall)
            robotAngle = add_angle(robotToObjectAngle, -robotRotation)
            if robotDistance < 20:
                print("Found ball")
                stateQueue.pop(0)
                targetBall = None # Reset target ball

    if state == TO_INTERMEDIARY:
        if stateQueue[1][0] == TO_GOAL and (len(detectedObjects["whiteBalls"]) > 0 or len(detectedObjects["orangeBalls"]) > 0):
            stateQueue.clear()
        intermediaryPoint = stateVariables[0]
        cv2.circle(frame, tuple_toint(intermediaryPoint), 11, (50,200,50), 6) # Mark intermediary
        robotDistance = calculateDistance(robotPos[0], intermediaryPoint)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], intermediaryPoint)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)

        if robotDistance <= 50:# and -0.2 < robotAngle < 0.2:
            print("Reached intermediary point!")
            stateQueue.pop(0)

    elif state == TO_OA_INTERMEDIARY:
        intermediaryPoint = stateVariables[0]
        cv2.circle(frame, tuple_toint(intermediaryPoint), 11, (50,200,50), 6) # Mark intermediary
        robotDistance = calculateDistance(robotPos[0], intermediaryPoint)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], intermediaryPoint)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)

        if robotDistance <= 60:# and -0.2 < robotAngle < 0.2:
            print("Reached OA-intermediary point!")
            stateQueue.pop(0)


    elif state == TO_GOAL:
        if len(detectedObjects["whiteBalls"]) > 0 or len(detectedObjects["orangeBalls"]) > 0:
            stateQueue.clear()
        # If no balls are present, move to goal.
        goalPos = detectedObjects["goals"][0]
        robotDistance = calculateDistance(robotPos[0], goalPos)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], goalPos)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)

        if robotDistance <= 110:
            stateQueue.pop(0)
            stateQueue.append((VOMIT, time.time()))

    elif state == VOMIT:
        VOMIT_TIME = 6
        if (stateVariables[0] + VOMIT_TIME <= time.time()):
            stateQueue.clear()
            stateQueue.append((BACKOFF, robotPos[0], 100))
            stateQueue.append((SEARCH_BALLS,))

    elif state == WAIT:
        if (len(stateVariables) < 2):
            stateQueue[0] = (WAIT, stateVariables[0], time.time() + stateVariables[0])
            stateVariables = stateQueue[0][1:]
        if (stateVariables[1] <= time.time()):
            stateQueue.pop(0)

    elif state == TO_EXACT_ROTATION:

        exactRotationTarget = stateVariables[0]
        robotAngle = add_angle(exactRotationTarget, -robotRotation)  # TODO: Check if this works lol

        if -0.2 < robotAngle < 0.2:
            stateQueue.pop(0)
            targetBall = None # TODO: TEMP!!!
    
    elif state == BACKOFF:
        # Backoff to point
        startPoint = stateVariables[0]
        targetDistance = stateVariables[1]
        distance = calculateDistance(robotPos[0], startPoint)
        robotDistance = max(0, targetDistance - distance)
        if distance >= targetDistance:
            print("Reached BACKOFF point")
            stateQueue.clear()

    elif state == COLLECT_BALL:

        allBalls = detectedObjects.get("whiteBalls", []) + detectedObjects.get("orangeBalls", [])
        stateJson = stateVariables[0]
        targetBall = stateJson.get('target', None)

        if targetBall is None and targetBallMemory is not None:
            targetBall = targetBallMemory
            stateJson['target'] = targetBall

        if targetBall is None:
            print("No target ball and no memory — resetting")
            stateQueue.pop(0)
            targetBallMemory = None
            stateQueue.append((SEARCH_BALLS,))
            return robotDistance, robotAngle, state
        
        stateJson['memoryAge'] = stateJson.get('memoryAge', 0) + 1
        MaxMemoryAge = 120   # How many frames to remember the target ball before resetting it.

        if stateJson['memoryAge'] > MaxMemoryAge:
            print("Memory too old — resetting")
            stateQueue.pop(0)
            targetBall = None
            targetBallMemory = None
            stateQueue.append((SEARCH_BALLS,))
            return robotDistance, robotAngle, state

        nearestBall = min(allBalls, key=lambda b: calculateDistance(b, targetBall)) if allBalls else None

        if nearestBall:
            drift = calculateDistance(nearestBall, targetBall)
            if drift < 40:
            # Accept updated ball
                targetBall = nearestBall
                targetBallMemory = nearestBall
                stateJson['target'] = nearestBall
                stateJson['memoryAge'] = 0  # Reset memory age
            
        # Calculate movement toward the ball
        robotDistance = calculateDistance(robotPos[0], targetBall)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], targetBall)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)

        # Draw what we are trying to collect
        cv2.circle(frame, tuple_toint(targetBall), 20, (0,150,150), 5)

        if robotDistance <= 65:
            print("Ball collected!")
            stateQueue.pop(0)
            targetBall = None
            targetBallMemory = None
            stateQueue.append((SEARCH_BALLS,))
            return robotDistance, robotAngle, state
        

    
    # COPY OF COLLECT_BALL BUT WITH SPECIFIC SPEEDS FOR BORDER
    elif state == COLLECT_BALL_BORDER:
        allBalls = detectedObjects.get("whiteBalls", []) + detectedObjects.get("orangeBalls", [])
        stateJson = stateVariables[0]
        targetBall = stateJson.get('target', None)

        if targetBall is None and targetBallMemory is not None:
            targetBall = targetBallMemory
            stateJson['target'] = targetBall

        if targetBall is None:
            print("No target ball and no memory — resetting")
            stateQueue.pop(0)
            targetBallMemory = None
            stateQueue.append((SEARCH_BALLS,))
            return robotDistance, robotAngle, state
        
        stateJson['memoryAge'] = stateJson.get('memoryAge', 0) + 1
        MaxMemoryAge = 120   # How many frames to remember the target ball before resetting it.

        if stateJson['memoryAge'] > MaxMemoryAge:
            print("Memory too old — resetting")
            stateQueue.pop(0)
            targetBall = None
            targetBallMemory = None
            stateQueue.append((SEARCH_BALLS,))
            return robotDistance, robotAngle, state

        nearestBall = min(allBalls, key=lambda b: calculateDistance(b, targetBall)) if allBalls else None

        if nearestBall:
            drift = calculateDistance(nearestBall, targetBall)
            if drift < 40:
            # Accept updated ball
                targetBall = nearestBall
                targetBallMemory = nearestBall
                stateJson['target'] = nearestBall
                stateJson['memoryAge'] = 0  # Reset memory age
            
        # Calculate movement toward the ball
        robotDistance = calculateDistance(robotPos[0], targetBall)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], targetBall)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)

        # Draw what we are trying to collect
        cv2.circle(frame, tuple_toint(targetBall), 20, (0,150,150), 5)

        if robotDistance <= 65:
            print("Ball collected!")
            stateQueue.pop(0)
            targetBall = None
            targetBallMemory = None
            stateQueue.append((SEARCH_BALLS,))
            return robotDistance, robotAngle, state


            
    
    # Draw robot angle
    drobotAngle = add_angle(robotAngle, robotRotation)#(robotAngle - robotRotation + np.pi) % (2*np.pi) - np.pi
    cv2.arrowedLine(frame, tuple_toint(robotPos[0]), (int(robotPos[0][0] + math.cos(drobotAngle)*250), int(robotPos[0][1] + math.sin(drobotAngle)*250)), (255,0,0), 4, tipLength=0.2) 

    print(f"State queue: {stateQueue}")

    return robotDistance, robotAngle, state
    

def handleBallTargetIntermediate(crossInfo, playAreaIntermediate, detectedObjects, robotPos, frame):
    global stateQueue; global targetBall
    if crossInfo is not None and is_objectmiddle_in_circle(targetBall, crossInfo.middle_point, crossInfo.size):
        print("BALL IN CROSS!")
        intermediaryPoint = findIntermediatyCrossPoint(targetBall, crossInfo.middle_point, crossInfo.robot_gap, crossInfo.robot_intermediary_corners)
        stateQueue.pop(0)
        
        handleOA(robotPos, intermediaryPoint, detectedObjects)
        stateQueue.append((TO_INTERMEDIARY, intermediaryPoint))
        exactRotationTarget = calculateAngleOfTwoPoints(intermediaryPoint, targetBall) # TODO: Suboptimal with intermediary point and not robot point used after reaching target but whatever.
        stateQueue.append((TO_EXACT_ROTATION, exactRotationTarget))
        stateQueue.append((COLLECT_BALL, {'target': targetBall}))
        stateQueue.append((WAIT, 1))
        stateQueue.append((BACKOFF, targetBall, calculateDistance(targetBall, intermediaryPoint) * 0.6))
    
    elif crossInfo is not None and is_objectmiddle_close_circle(targetBall, crossInfo.middle_point, crossInfo.size+100):
        print("BALL close to CROSS!")
        stateQueue.pop(0)
        handleOA(robotPos, targetBall, detectedObjects)        
        stateQueue.append((COLLECT_BALL, {'target': targetBall}))
        stateQueue.append((WAIT, 1))
        stateQueue.append((BACKOFF, targetBall, 80))
        
    
    if playAreaIntermediate is not None:
        inside, closest = analyze_point_with_polygon(targetBall, playAreaIntermediate)
        if not inside:
            print(f"Ball close to edge. Closest Point: {closest}")
            dist = calculateDistance(targetBall, closest)
            if (dist < 75):
                pushamt = 50
                print("Ball so close to edge trapezoid that we need to push it futher back!")
                ang = calculateAngleOfTwoPoints(targetBall, closest)
                closest = (closest[0] + np.cos(ang)*pushamt, closest[1] + np.sin(ang)*pushamt)
            
            stateQueue.pop(0)
            handleOA(robotPos, closest, detectedObjects)
            stateQueue.append((TO_INTERMEDIARY, closest))
            stateQueue.append((COLLECT_BALL_BORDER, {'target': targetBall}))
            stateQueue.append((WAIT, 1))
            # stateQueue.append((BACKOFF, targetBall, calculateDistance(targetBall, closest) * 0.6))
            stateQueue.append((BACKOFF, targetBall, 45))
            cv2.line(frame, tuple_toint(targetBall), tuple_toint(closest), (0, 150, 150), 2)
    
    else:
        targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
