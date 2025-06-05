from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from imageRecognition.positionEstimator import CrossInfo, findIntermediatyCrossPoint
import numpy as np
import cv2
from robotMovement.tools import tuple_toint

# TO_INTERMEDIARY
intermediaryPoint = None
intermediaryFinishState = None

# TO_EXACT_ROTATION
exactRotationTarger = None

# SEARCH_BALLS
targetBall = None

def is_objectmiddle_in_circle(objectpos, center, radius):
    #middle = ( (objectpos[0][0] + objectpos[1][0])/2, (objectpos[0][1] + objectpos[1][1])/2 )
    point = np.array(objectpos)
    center = np.array(center)
    distance_squared = np.sum((point - center) ** 2)
    return distance_squared <= radius ** 2

def calcDistAndAngleToTarget(detectedObjects, state, crossInfo: CrossInfo, frame):
    # States for state machine. Can be expanded later to handle situations calling for specific behaviour like getting ball from corner/cross.
    SEARCH_BALLS = "SEARCH_BALLS"
    TO_INTERMEDIARY = "TO_INTERMEDIARY"
    TO_GOAL = "TO_GOAL"
    TO_EXACT_ROTATION = "TO_EXACT_ROTATION"

    global intermediaryPoint; global exactRotationTarger; global intermediaryFinishState; global targetBall
        
    robotDistance = None
    robotAngle = None
    
    # TEMP!
    state = SEARCH_BALLS
    targetBall = None

    # If no state has been set yet, put robot in ball searching state.
    if state == None:
        state = SEARCH_BALLS

    # This is the two points used to identify the robots position. 
    robotPos = calculateRobotPositionFlexible(detectedObjects["frontLeftCorner"], detectedObjects["frontRightCorner"], detectedObjects["backLeftCorner"], detectedObjects["backRightCorner"])

    # Use state machine to dictate robots target based on its state
    if state == SEARCH_BALLS:
        # TODO: WARNING! CHECK THAT THE TARGET BALL HAS NOT MOVED TOO MUCH!!!! HERE WE ASSUME IT IS STATIONARY WHICH IS BAAAAD
        if targetBall == None:
            if detectedObjects.get("whiteBalls") and len(detectedObjects["whiteBalls"]) > 0:
                targetBall = min(detectedObjects["whiteBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
                # TODO: Apply cross logic to white also
            elif detectedObjects.get("orangeBalls") and len(detectedObjects["orangeBalls"]) > 0:
                targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
                if is_objectmiddle_in_circle(targetBall, crossInfo.middle_point, crossInfo.size):
                    print("ORANGE BALL IN CROSS!")
                    intermediaryFinishState = SEARCH_BALLS
                    intermediaryPoint = findIntermediatyCrossPoint(targetBall, crossInfo.middle_point, crossInfo.robot_gap, crossInfo.robot_intermediary_corners)
                    cv2.circle(frame, tuple_toint(intermediaryPoint), 11, (50,200,50), 6) # Mark closest
                    #state = TO_INTERMEDIARY TODO: Temporarily disabled to test!
            elif not detectedObjects["whiteBalls"] and not detectedObjects["orangeBalls"]:
                intermediaryFinishState = TO_GOAL
                state = TO_INTERMEDIARY

        

        # Calculate distance and angle to the selected ball
        if targetBall and robotPos[0] is not None and robotPos[1] is not None:
            robotDistance = calculateDistance(robotPos[0], targetBall)
            robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], targetBall)

        # If no balls are present, move to intermediary point in preperation for turning in balls.

    elif state == TO_INTERMEDIARY:

        # if detectedObjects["whiteBalls"] or detectedObjects["orangeBalls"]:
        #     state = SEARCH_BALLS

        #intermediaryPoint = (detectedObjects["goals"][1][0] - 300, detectedObjects["goals"][1][1])
        # Have robots middle point reach the intermediary point as it makes for better arrival at goal.
        robotMiddle = ((robotPos[0][0] + robotPos[1][0]) / 2, (robotPos[0][1] + robotPos[1][1]) / 2)

        robotDistance = calculateDistance(robotMiddle, intermediaryPoint)
        robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], intermediaryPoint)    

        if robotDistance <= 10 and -0.2 < robotAngle < 0.2:
            state = intermediaryFinishState if intermediaryFinishState is not None else TO_GOAL
    
    elif state == TO_GOAL:
        if detectedObjects["whiteBalls"] or detectedObjects["orangeBalls"]:
            state = SEARCH_BALLS
        # NOTE: This turns in balls in the small goal. This assumes that the small goal is on the right side of the camera
        goalPos = detectedObjects["goals"][1]

        robotDistance = calculateDistance(robotPos[0], goalPos)
        robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], goalPos)

    return robotDistance, robotAngle, state