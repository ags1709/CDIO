from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation, calculateAngleOfTwoPoints
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from imageRecognition.positionEstimator import CrossInfo, findIntermediatyCrossPoint
import numpy as np
import cv2
from robotMovement.tools import tuple_toint
import math
import numpy as np


stateQueue = [ # Format: (State,variables)
    
]

# SEARCH_BALLS
targetBall = None
# def log_state_transition(state: str, file_path: str = "state_transitions.txt"):
#     with open(file_path, "a") as f:
#         f.write(f"{state}\n")


def is_objectmiddle_in_circle(objectpos, center, radius):
    #middle = ( (objectpos[0][0] + objectpos[1][0])/2, (objectpos[0][1] + objectpos[1][1])/2 )
    point = np.array(objectpos)
    center = np.array(center)
    distance_squared = np.sum((point - center) ** 2)
    return distance_squared <= radius ** 2

def add_angle(a1, a2):
    return (a1 + a2 + np.pi) % (2*np.pi) - np.pi

def calcDistAndAngleToTarget(detectedObjects, crossInfo: CrossInfo, frame):
    # States for state machine. Can be expanded later to handle situations calling for specific behaviour like getting ball from corner/cross.
    SEARCH_BALLS = "SEARCH_BALLS"
    TO_INTERMEDIARY = "TO_INTERMEDIARY"
    TO_GOAL = "TO_GOAL"
    TO_EXACT_ROTATION = "TO_EXACT_ROTATION"

    global targetBall; global stateQueue
        
    robotDistance = 0
    robotAngle = 0
    
    # TEMP!
    #state = SEARCH_BALLS
    #targetBall = None

    # If no state has been set yet, put robot in ball searching state.
    if len(stateQueue) == 0:
        stateQueue.append((SEARCH_BALLS, ""))

    # This is the two points used to identify the robots position. 
    robotPos = calculateRobotPositionFlexible(detectedObjects["frontLeftCorner"], detectedObjects["frontRightCorner"], detectedObjects["backLeftCorner"], detectedObjects["backRightCorner"])
    robotMiddle = ((robotPos[0][0] + robotPos[1][0]) / 2, (robotPos[0][1] + robotPos[1][1]) / 2)
    robotRotation = calculateAngleOfTwoPoints(robotPos[1], robotPos[0])
    

    state = stateQueue[0][0] # State
    stateVariables = stateQueue[0][1:] # Variables for state
    # Use state machine to dictate robots target based on its state
    if state == SEARCH_BALLS:
        # TODO: WARNING! CHECK THAT THE TARGET BALL HAS NOT MOVED TOO MUCH!!!! HERE WE ASSUME IT IS STATIONARY WHICH IS BAAAAD
        # log_state_transition(SEARCH_BALLS)

        if targetBall == None:
            if detectedObjects.get("whiteBalls") and len(detectedObjects["whiteBalls"]) > 0:
                targetBall = min(detectedObjects["whiteBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
                # TODO: Apply cross logic to white also
            elif detectedObjects.get("orangeBalls") and len(detectedObjects["orangeBalls"]) > 0:
                targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
                print("ORANGE BALL DETECTED!")
                if is_objectmiddle_in_circle(targetBall, crossInfo.middle_point, crossInfo.size):
                    print("ORANGE BALL IN CROSS!")
                    intermediaryPoint = findIntermediatyCrossPoint(targetBall, crossInfo.middle_point, crossInfo.robot_gap, crossInfo.robot_intermediary_corners)
                    stateQueue.pop(0)
                    stateQueue.append((TO_INTERMEDIARY, intermediaryPoint))
                    #exactRotationTarget = (crossInfo.angle_rad + np.pi + np.pi) % (2*np.pi) - np.pi
                    exactRotationTarget = calculateAngleOfTwoPoints(intermediaryPoint, targetBall) # TODO: Suboptimal with intermediary point and not robot point used after reaching target but whatever.
                    stateQueue.append((TO_EXACT_ROTATION, exactRotationTarget))
                    stateQueue.append((SEARCH_BALLS, ""))
            if not detectedObjects["whiteBalls"] and not detectedObjects["orangeBalls"]:
                print("No white balls")
                intermediaryPoint = (detectedObjects["goals"][1][0] - 300, detectedObjects["goals"][1][1])
                stateQueue.pop(0) 
                stateQueue.append((TO_INTERMEDIARY, intermediaryPoint))
                stateQueue.append((TO_GOAL,))  # Har sat et komma, pga at det er en tuple.


        

        # Calculate distance and angle to the selected ball
        if state is SEARCH_BALLS and targetBall and robotPos[0] is not None and robotPos[1] is not None:
            robotDistance = calculateDistance(robotPos[0], targetBall)
            robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], targetBall)
            robotAngle = add_angle(robotToObjectAngle, -robotRotation)
            if robotDistance < 25:
                print("Found ball")
                stateQueue.pop(0)
                targetBall = None # Reset target ball


        # If no balls are present, move to intermediary point in preperation for turning in balls.

    if state == TO_INTERMEDIARY: # 
        # log_state_transition(TO_INTERMEDIARY)

        # if detectedObjects["whiteBalls"] or detectedObjects["orangeBalls"]:
        #     state = SEARCH_BALLS

        #intermediaryPoint = (detectedObjects["goals"][1][0] - 300, detectedObjects["goals"][1][1])
        # Have robots middle point reach the intermediary point as it makes for better arrival at goal.
        intermediaryPoint = stateVariables[0]

        cv2.circle(frame, tuple_toint(intermediaryPoint), 11, (50,200,50), 6) # Mark intermediary
        robotDistance = calculateDistance(robotMiddle, intermediaryPoint)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], intermediaryPoint)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)   

        if robotDistance <= 50:# and -0.2 < robotAngle < 0.2:
            print("Reached intermediary point!")
            #state = intermediaryFinishState if intermediaryFinishState is not None else TO_GOAL
            stateQueue.pop(0)
           

    elif state == TO_GOAL:
        # log_state_transition(TO_GOAL)

        print("TO_GOAL")
        # If no balls are present, move to goal.
        goalPos = detectedObjects["goals"][1]
        robotDistance = calculateDistance(robotPos[0], goalPos)
        robotToObjectAngle = calculateAngleOfTwoPoints(robotPos[0], goalPos)
        robotAngle = add_angle(robotToObjectAngle, -robotRotation)

    # Add a condition for arrival if needed
        if robotDistance <= 50:
            print("Reached the goal!")
            stateQueue.pop(0)
        
    elif state == TO_EXACT_ROTATION:
        # log_state_transition(TO_EXACT_ROTATION)

        exactRotationTarget = stateVariables[0]
        robotAngle = add_angle(exactRotationTarget, -robotRotation)  # TODO: Check if this works lol

        if -0.2 < robotAngle < 0.2:
            #state = intermediaryFinishState if intermediaryFinishState is not None else TO_GOAL
            stateQueue.pop(0)
            targetBall = None # TODO: TEMP!!!
    # Draw robot angle
    drobotAngle = add_angle(robotAngle, robotRotation)#(robotAngle - robotRotation + np.pi) % (2*np.pi) - np.pi
    cv2.arrowedLine(frame, tuple_toint(robotPos[0]), (int(robotPos[0][0] + math.cos(drobotAngle)*250), int(robotPos[0][1] + math.sin(drobotAngle)*250)), (255,0,0), 4, tipLength=0.2) 

    
    return robotDistance, robotAngle, state