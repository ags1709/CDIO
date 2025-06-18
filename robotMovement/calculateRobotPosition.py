import math
import numpy as np

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


# # Done with chatGPT
# # NOTE: Insert default width and height. Should be the pixel distences between corners
# def calculateRobotPositionFlexible(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner, width=102, height=138):
#     # Fill missing corners if possible
#     if not frontLeftCorner:
#         if frontRightCorner and backLeftCorner and backRightCorner:
#             frontLeftCorner = find_fourth_corner(backLeftCorner, backRightCorner, frontRightCorner)
#         elif frontRightCorner and backLeftCorner:
#             frontLeftCorner = find_Top_Corner(frontRightCorner, backLeftCorner)
#         elif frontRightCorner and backRightCorner:
#             frontLeftCorner, backLeftCorner = find_opposite_side(frontRightCorner, backRightCorner, width, height)
#         elif backLeftCorner and backRightCorner:
#             frontLeftCorner, frontRightCorner = find_opposite_side(backLeftCorner, backRightCorner, width, height)
    
#     if not frontRightCorner:
#         if frontLeftCorner and backLeftCorner and backRightCorner:
#             frontRightCorner = find_fourth_corner(backRightCorner, backLeftCorner, frontLeftCorner)
#         elif frontLeftCorner and backRightCorner:
#             frontRightCorner = find_Top_Corner(frontLeftCorner, backRightCorner)
#         elif frontLeftCorner and backLeftCorner:
#             frontRightCorner, backRightCorner = find_opposite_side(frontLeftCorner, backLeftCorner, width, height)
#         elif backLeftCorner and backRightCorner:
#             frontRightCorner, frontLeftCorner = find_opposite_side(backLeftCorner, backRightCorner, width, height)
        
#     if not backLeftCorner:
#         if backRightCorner and frontRightCorner and frontLeftCorner:
#             backLeftCorner = find_fourth_corner(frontLeftCorner, frontRightCorner, backRightCorner)
#         elif backRightCorner and frontLeftCorner:
#             backLeftCorner = find_Bottom_Corner(frontLeftCorner, backRightCorner)
#         elif frontLeftCorner and frontRightCorner:
#             backLeftCorner, backRightCorner = find_opposite_side(frontLeftCorner, frontRightCorner, width, height)
#         elif frontRightCorner and backRightCorner:
#             backLeftCorner, frontLeftCorner = find_opposite_side(frontRightCorner, backRightCorner, width, height)
        

#     if not backRightCorner:
#         if backLeftCorner and frontLeftCorner and frontRightCorner:
#             backRightCorner = find_fourth_corner(frontRightCorner, frontLeftCorner, backLeftCorner)
#         elif backLeftCorner and frontRightCorner:
#             backRightCorner = find_Bottom_Corner(frontRightCorner, backLeftCorner)
#         elif frontLeftCorner and frontRightCorner:
#             backRightCorner, backLeftCorner = find_opposite_side(frontLeftCorner, frontRightCorner, width, height)
#         elif frontLeftCorner and backLeftCorner:
#             backRightCorner, frontRightCorner = find_opposite_side(frontLeftCorner, backLeftCorner, width, height)

#     # Now calculate points
#     if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
#         # Transform the points down to the ground plane instead of being in the air
#         frontLeftCorner  = correctPerspective(frontLeftCorner)
#         frontRightCorner = correctPerspective(frontRightCorner)
#         backLeftCorner   = correctPerspective(backLeftCorner)
#         backRightCorner  = correctPerspective(backRightCorner)
#         #print(f"\n Front Left Corner: {frontLeftCorner}: Front Right Corner {frontRightCorner}: Back Left Corner {backLeftCorner}: Back Right Corner {backRightCorner}")
#         forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
#         backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
#         #print(f"\n Forward point {forwardsPoint}, Backward points {backwardsPoint} \n")
#         return (forwardsPoint, backwardsPoint)
#     else:
#         return((0,0),(0,0))
#         #raise ValueError("Not enough information to calculate corners.")
# --------------------------------------------------------------------------------------------------------------------------------
# New attempt
import math

# Assume width and height are globally known
WIDTH = 119
HEIGHT = 127

def getRobotPos(corners):
    notNoneCount, notNoneidxs = notNoneCounterAndFinder(corners)
    modifiedCorners = [corners[]]
    if notNoneCount == 4:
        return getRobotPosFromFourCorners()
    
    
    elif notNoneCount == 3:
        robotCorners = findCornersFromThree(corners[notNoneidxs[0]], corners[notNoneidxs[1]], corners[notNoneidxs[2]])

    elif notNoneCount == 2:
        robotCorners = findCornersFromTwo(corners[notNoneidxs[0]], corners[notNoneidxs[1]])
    
    return getRobotPosFromFourCorners(robotCorners[0], robotCorners[1], robotCorners[2], robotCorners[3])

def getRobotPosFromFourCorners(frontLeftYellow, frontRightGreen, backLeftPink, backRightBrown):
    frontLeftCorner  = correctPerspective(frontLeftYellow)
    frontRightCorner = correctPerspective(frontRightGreen)
    backLeftCorner   = correctPerspective(backLeftPink)
    backRightCorner  = correctPerspective(backRightBrown)
    forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
    backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
    return (forwardsPoint, backwardsPoint)

def findCornersFromTwo(corner1, corner2):
    import numpy as np

    # Extract positions and color tags
    (x1, y1, color1) = corner1
    (x2, y2, color2) = corner2

    # Map of color to logical position
    color_to_offset = {
        'yellow': (0, HEIGHT),
        'green': (WIDTH, HEIGHT),
        'pink': (0, 0),
        'brown': (WIDTH, 0)
    }

    # Compute vector from corner1 to corner2
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    vec = p2 - p1

    # Offset vector in unrotated frame
    offset1 = np.array(color_to_offset[color1])
    offset2 = np.array(color_to_offset[color2])
    logical_vec = offset2 - offset1

    # Compute rotation matrix that maps logical_vec to vec
    def unit(v): return v / np.linalg.norm(v)

    if np.all(logical_vec == 0):
        raise ValueError("Two corners cannot have the same logical position")

    angle = math.atan2(vec[1], vec[0]) - math.atan2(logical_vec[1], logical_vec[0])
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    R = np.array([[cos_a, -sin_a], [sin_a, cos_a]])

    # Now find the position of the origin corner (0,0 in unrotated frame)
    # That maps to position: p1 - R @ offset1
    origin = p1 - R @ offset1

    # Compute all corners
    yellow = tuple(np.round(origin + R @ np.array(color_to_offset['yellow'])).astype(int))
    green = tuple(np.round(origin + R @ np.array(color_to_offset['green'])).astype(int))
    pink = tuple(np.round(origin + R @ np.array(color_to_offset['pink'])).astype(int))
    brown = tuple(np.round(origin + R @ np.array(color_to_offset['brown'])).astype(int))

    return (yellow, green, pink, brown)

def findCornersFromThree(corner1, corner2, corner3):
    # Logical layout before rotation
    color_to_logical = {
        'yellow': (0, HEIGHT),
        'green': (WIDTH, HEIGHT),
        'pink': (0, 0),
        'brown': (WIDTH, 0)
    }

    # Parse the inputs
    inputs = [corner1, corner2, corner3]
    real_points = []
    logical_points = []

    for (x, y, color) in inputs:
        real_points.append([x, y])
        logical_points.append(list(color_to_logical[color]))

    real_points = np.array(real_points).T  # Shape: 2x3
    logical_points = np.array(logical_points).T  # Shape: 2x3

    # Add a row of ones for affine transformation solving
    logical_points_aug = np.vstack([logical_points, np.ones(3)])

    # Solve for affine transformation matrix A such that:
    # real_points ≈ A @ logical_points_aug
    A, _, _, _ = np.linalg.lstsq(logical_points_aug.T, real_points.T, rcond=None)
    # A has shape 3x2 (transpose it to get 2x3)
    A = A.T

    # Now apply A to all 4 logical corners
    def transform(logical_pt):
        vec = np.array([logical_pt[0], logical_pt[1], 1])
        result = A @ vec
        return tuple(np.round(result).astype(int))

    yellow = transform(color_to_logical['yellow'])
    green = transform(color_to_logical['green'])
    pink = transform(color_to_logical['pink'])
    brown = transform(color_to_logical['brown'])

    return (yellow, green, pink, brown)

def notNoneCounterAndFinder(corners):
    count = 0
    idxs = []
    for i in range(len(corners)):
        if corners[i] != None:
            count += 1
            idxs.append(i)
    return count, idxs
# ----------------------------------------------------------------------------------------------------------------------------
def correctPerspective(point):
    factor = (camera_height - corner_height) / (camera_height - target_height)
    x, y = frame_w / 2, frame_h / 2
    return (factor * (point[0]  - x) + x, factor * (point[1]  - y) + y)

# Help from ChatGPT
#--------------------------
def subtract(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def MidPoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def find_fourth_corner(A, B, C):
    return add(A, subtract(C, B))

def find_Top_Corner(A,C):
    v = subtract(A,C)
    M = MidPoint(A,C)

    Perpendicular = (-v[1], v[0])  # Rotate 90 degrees
    HalfPerpendicular = (Perpendicular[0] / 2, Perpendicular[1] / 2)

    return (M[0] + HalfPerpendicular[0], M[1] + HalfPerpendicular[1])

def find_Bottom_Corner(A,C):
    v = subtract(A,C)
    M = MidPoint(A,C)
    Perpendicular = (-v[1], v[0])  # Rotate 90 degrees
    HalfPerpendicular = (Perpendicular[0] / 2, Perpendicular[1] / 2)

    return (M[0] - HalfPerpendicular[0], M[1] - HalfPerpendicular[1])

def scale(v, s):
    return (v[0]*s, v[1]*s)

def find_opposite_side(A, B, width, height):
    AB = subtract(B, A)
    length = math.hypot(AB[0], AB[1])

    AB_unit = (AB[0]/length, AB[1]/length)
    perp = (-AB_unit[1], AB_unit[0])
    perp_scaled = scale(perp, width)

    C = add(B, perp_scaled)
    D = add(A, perp_scaled)
    return C, D

#--------------------------