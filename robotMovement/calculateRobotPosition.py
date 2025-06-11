import math

# The heights of different things in cm
camera_height = 170
corner_height = 25

def calculateRobotPosition(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner):
    if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        return (forwardsPoint, backwardsPoint)


# Done with chatGPT
# NOTE: Insert default width and height. Should be the pixel distences between corners
def calculateRobotPositionFlexible(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner, width=102, height=138):
    # Fill missing corners if possible
    if not frontLeftCorner:
        if frontRightCorner and backLeftCorner and backRightCorner:
            frontLeftCorner = find_fourth_corner(backLeftCorner, backRightCorner, frontRightCorner)
        elif frontRightCorner and backLeftCorner:
            frontLeftCorner = find_Top_Corner(frontRightCorner, backLeftCorner)
        elif frontRightCorner and backRightCorner:
            frontLeftCorner, backLeftCorner = find_opposite_side(frontRightCorner, backRightCorner, width, height)
        elif backLeftCorner and backRightCorner:
            frontLeftCorner, frontRightCorner = find_opposite_side(backLeftCorner, backRightCorner, width, height)
    
    if not frontRightCorner:
        if frontLeftCorner and backLeftCorner and backRightCorner:
            frontRightCorner = find_fourth_corner(backRightCorner, backLeftCorner, frontLeftCorner)
        elif frontLeftCorner and backRightCorner:
            frontRightCorner = find_Top_Corner(frontLeftCorner, backRightCorner)
        elif frontLeftCorner and backLeftCorner:
            frontRightCorner, backRightCorner = find_opposite_side(frontLeftCorner, backLeftCorner, width, height)
        elif backLeftCorner and backRightCorner:
            frontRightCorner, frontLeftCorner = find_opposite_side(backLeftCorner, backRightCorner, width, height)
        
    if not backLeftCorner:
        if backRightCorner and frontRightCorner and frontLeftCorner:
            backLeftCorner = find_fourth_corner(frontLeftCorner, frontRightCorner, backRightCorner)
        elif backRightCorner and frontLeftCorner:
            backLeftCorner = find_Bottom_Corner(frontLeftCorner, backRightCorner)
        elif frontLeftCorner and frontRightCorner:
            backLeftCorner, backRightCorner = find_opposite_side(frontLeftCorner, frontRightCorner, width, height)
        elif frontRightCorner and backRightCorner:
            backLeftCorner, frontLeftCorner = find_opposite_side(frontRightCorner, backRightCorner, width, height)
        

    if not backRightCorner:
        if backLeftCorner and frontLeftCorner and frontRightCorner:
            backRightCorner = find_fourth_corner(frontRightCorner, frontLeftCorner, backLeftCorner)
        elif backLeftCorner and frontRightCorner:
            backRightCorner = find_Bottom_Corner(frontRightCorner, backLeftCorner)
        elif frontLeftCorner and frontRightCorner:
            backRightCorner, backLeftCorner = find_opposite_side(frontLeftCorner, frontRightCorner, width, height)
        elif frontLeftCorner and backLeftCorner:
            backRightCorner, frontRightCorner = find_opposite_side(frontLeftCorner, backLeftCorner, width, height)

    # Now calculate points
    if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
        # Transform the points down to the ground plane instead of being in the air
        factor = (camera_height - corner_height) / camera_height
        frontLeftCorner  = (factor * frontLeftCorner[0],  factor * frontLeftCorner[1])
        frontRightCorner = (factor * frontRightCorner[0], factor * frontRightCorner[1])
        backLeftCorner   = (factor * backLeftCorner[0],   factor * backLeftCorner[1])
        backRightCorner  = (factor * backRightCorner[0],  factor * backRightCorner[1])
        #print(f"\n Front Left Corner: {frontLeftCorner}: Front Right Corner {frontRightCorner}: Back Left Corner {backLeftCorner}: Back Right Corner {backRightCorner}")
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        #print(f"\n Forward point {forwardsPoint}, Backward points {backwardsPoint} \n")
        return (forwardsPoint, backwardsPoint)
    else:
        return((0,0),(0,0))
        #raise ValueError("Not enough information to calculate corners.")


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