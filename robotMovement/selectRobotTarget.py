# from robotMovement.distanceBetweenObjects import calculateDistance
# from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
# from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible

from robotMovement.distanceBetweenObjects import calculateDistance
from robotMovement.angleOfRotationCalculator import calculateAngleOfRotation
from robotMovement.calculateRobotPosition import calculateRobotPositionFlexible
from robotMovement.obstacleAvoidance import (
    calculateMarkedGrid, astar, toGridCoords, toPixelCoords, 
    path_follower, getFieldOrigin, getFieldSize
)

grid = None
lastObstacles = None
fieldOrigin = None
fieldSize = None

def calcDistAndAngleToTarget(detectedObjects, state):
    global grid, lastObstacles, fieldOrigin, fieldSize
    # States for state machine. Can be expanded later to handle situations calling for specific behaviour like getting ball from corner/cross.
    SEARCH_BALLS = "SEARCH_BALLS"
    TO_INTERMEDIARY = "TO_INTERMEDIARY"
    TO_GOAL = "TO_GOAL"

    robotDistance = None
    robotAngle = None

    # If no state has been set yet, put robot in ball searching state.
    if state == None:
        state = SEARCH_BALLS

    # This is the two points used to identify the robots position. 
    robotPos = calculateRobotPositionFlexible(
        detectedObjects["frontLeftCorner"],
        detectedObjects["frontRightCorner"],
        detectedObjects["backLeftCorner"],
        detectedObjects["backRightCorner"])

    playfield = detectedObjects["playfield"]
    currentFieldSize = getFieldSize(playfield)

    # Create list of obstacle and add obstacles
    obstacles = []
    if detectedObjects.append(detectedObjects["cross"]) is not None:
        obstacles.append(detectedObjects["cross"])
    if detectedObjects.append(detectedObjects["egg"]) is not None:
        obstacles.append(detectedObjects["egg"])

    # Update grid only if needed
    if (grid is None or 
        lastObstacles != obstacles or 
        fieldSize != currentFieldSize):
        
        grid = calculateMarkedGrid(currentFieldSize, obstacles)
        lastObstacles = obstacles.copy()

    
    # Use state machine to dictate robots target based on its state
    if state == SEARCH_BALLS:
        targetBall = None
        if detectedObjects.get("whiteBalls") and len(detectedObjects["whiteBalls"]) > 0:
            targetBall = min(detectedObjects["whiteBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))
        elif detectedObjects.get("orangeBalls") and len(detectedObjects["orangeBalls"]) > 0:
            targetBall = min(detectedObjects["orangeBalls"], key=lambda ball: calculateDistance(robotPos[0], ball))

        # Calculate distance and angle to the selected ball
        if targetBall and robotPos[0] is not None and robotPos[1] is not None:
            robotGridPos = toGridCoords(robotPos[0, 0], robotPos[0, 1])
            ballGridPos = toGridCoords(targetBall[0], targetBall[0])

            # Calculate direct distance to ball to see if pathfinding is necessary
            directDistance = calculateDistance(robotPos[0], targetBall)

            if len(obstacles) > 0 and directDistance > 100:
                pass
            
            robotDistance = calculateDistance(robotPos[0], targetBall)
            robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], targetBall)

        # If no balls are present, move to intermediary point in preperation for turning in balls.
        if not detectedObjects["whiteBalls"] and not detectedObjects["orangeBalls"]:
            state = TO_INTERMEDIARY

    elif state == TO_INTERMEDIARY:

        if detectedObjects["whiteBalls"] or detectedObjects["orangeBalls"]:
            state = SEARCH_BALLS

        intermediaryPoint = (detectedObjects["goals"][1][0] - 300, detectedObjects["goals"][1][1])
        # Have robots middle point reach the intermediary point as it makes for better arrival at goal.
        robotMiddle = ((robotPos[0][0] + robotPos[1][0]) / 2, (robotPos[0][1] + robotPos[1][1]) / 2)

        robotDistance = calculateDistance(robotMiddle, intermediaryPoint)
        robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], intermediaryPoint)    

        if robotDistance <= 10 and -0.2 < robotAngle < 0.2:
            state = TO_GOAL
    
    elif state == TO_GOAL:
        if detectedObjects["whiteBalls"] or detectedObjects["orangeBalls"]:
            state = SEARCH_BALLS
        # NOTE: This turns in balls in the small goal. This assumes that the small goal is on the right side of the camera
        goalPos = detectedObjects["goals"][1]

        robotDistance = calculateDistance(robotPos[0], goalPos)
        robotAngle = calculateAngleOfRotation(robotPos[0], robotPos[1], goalPos)

    return robotDistance, robotAngle, state