import math
import numpy as np
from imageRecognition.positionEstimator import edge_normal

type Point = np.ndarray[tuple[int], np.dtype[np.floating]]

# The heights of different things in cm
camera_height = 165
corner_height = 17.5
target_height = 3

# Camera resolution, really scuffed
frame_w = 1920
frame_h = 1080

def calculateRobotPosition(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner):
    if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        return (forwardsPoint, backwardsPoint)


# Partially done with ChatGPT
# NOTE: Insert default width and height. Should be the pixel distences between corners
def calculateRobotPositionFlexible(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner, width=77, length=77):
    if (frontLeftCorner is not None): frontLeftCorner = np.array(frontLeftCorner, float)
    if (frontRightCorner is not None): frontRightCorner = np.array(frontRightCorner, float)
    if (backLeftCorner is not None): backLeftCorner = np.array(backLeftCorner, float)
    if (backRightCorner is not None): backRightCorner = np.array(backRightCorner, float)
    # Fill missing corners if possible
    if frontLeftCorner is None:
        if frontRightCorner is not None and backLeftCorner is not None and backRightCorner is not None:
            frontLeftCorner = find_fourth_corner(backLeftCorner, backRightCorner, frontRightCorner)
        elif frontRightCorner is not None and backLeftCorner is not None:
            frontLeftCorner = find_diagonal_corner(frontRightCorner, backLeftCorner)
        elif frontRightCorner is not None and backRightCorner is not None:
            frontLeftCorner, backLeftCorner = find_opposite_side(frontRightCorner, backRightCorner, width)
        elif backLeftCorner is not None and backRightCorner is not None:
            frontRightCorner, frontLeftCorner = find_opposite_side(backRightCorner, backLeftCorner, length)
    
    if frontRightCorner is None:
        if frontLeftCorner is not None and backLeftCorner is not None and backRightCorner is not None:
            frontRightCorner = find_fourth_corner(backRightCorner, backLeftCorner, frontLeftCorner)
        elif frontLeftCorner is not None and backRightCorner is not None:
            frontRightCorner = find_diagonal_corner(backRightCorner, frontLeftCorner)
        elif frontLeftCorner is not None and backLeftCorner is not None:
            backRightCorner, frontRightCorner = find_opposite_side(backLeftCorner, frontLeftCorner, width)
        elif backLeftCorner is not None and backRightCorner is not None:
            frontRightCorner, frontLeftCorner = find_opposite_side(backRightCorner, backLeftCorner, length)

    if backLeftCorner is None:
        if backRightCorner is not None and frontRightCorner is not None and frontLeftCorner is not None:
            backLeftCorner = find_fourth_corner(frontLeftCorner, frontRightCorner, backRightCorner)
        elif backRightCorner is not None and frontLeftCorner is not None:
            backLeftCorner = find_diagonal_corner(frontLeftCorner, backRightCorner)
        elif frontLeftCorner is not None and frontRightCorner is not None:
            backLeftCorner, backRightCorner = find_opposite_side(frontLeftCorner, frontRightCorner, length)
        elif frontRightCorner is not None and backRightCorner is not None:
            frontLeftCorner, backLeftCorner = find_opposite_side(frontRightCorner, backRightCorner, width)

    if backRightCorner is None:
        if backLeftCorner is not None and frontLeftCorner is not None and frontRightCorner is not None:
            backRightCorner = find_fourth_corner(frontRightCorner, frontLeftCorner, backLeftCorner)
        elif backLeftCorner is not None and frontRightCorner is not None:
            backRightCorner = find_diagonal_corner(backLeftCorner, frontRightCorner)
        elif frontLeftCorner is not None and frontRightCorner is not None:
            backLeftCorner, backRightCorner = find_opposite_side(frontLeftCorner, frontRightCorner, length)
        elif frontLeftCorner is not None and backLeftCorner is not None:
            backRightCorner, frontRightCorner = find_opposite_side(backLeftCorner, frontLeftCorner, width)

    # Now calculate points
    if (frontLeftCorner is not None and frontRightCorner is not None and backLeftCorner is not None and backRightCorner is not None):
        # Transform the points down to the ground plane instead of being in the air
        frontLeftCorner  = correctPerspective(frontLeftCorner)
        frontRightCorner = correctPerspective(frontRightCorner)
        backLeftCorner   = correctPerspective(backLeftCorner)
        backRightCorner  = correctPerspective(backRightCorner)
        #print(f"\n Front Left Corner: {frontLeftCorner}: Front Right Corner {frontRightCorner}: Back Left Corner {backLeftCorner}: Back Right Corner {backRightCorner}")
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        #print(f"\n Forward point {forwardsPoint}, Backward points {backwardsPoint} \n")
        return (forwardsPoint, backwardsPoint)
    else:
        return None
        #raise ValueError("Not enough information to calculate corners.")

def correctPerspective(point):
    factor = (camera_height - corner_height) / (camera_height - target_height)
    x, y = frame_w / 2, frame_h / 2
    return (factor * (point[0]  - x) + x, factor * (point[1]  - y) + y)

def find_fourth_corner(A: Point, B: Point, C: Point):
    return A + (C - B)

def find_diagonal_corner(A: Point, C: Point):
    """Calculates one of the two missing corners from two diagonal corners. This function assumes a square!"""
    v = (C - A) / 2
    M = (A + C) / 2

    perp = np.array((-v[1], v[0])) # Rotate 90 degrees clockwise

    return M + perp

def find_opposite_side(A: Point, B: Point, side_length: float):
    perp = edge_normal(A, B) * side_length
    return A + perp, B + perp
