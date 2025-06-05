import math

def subtract(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def MidPoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def find_fourth_corner(A, B, C):
    return add(A, subtract(C, B))

def find_perpendicular_corner(A, C, direction=1):
    v = subtract(A, C)
    M = MidPoint(A, C)
    perp = (-v[1], v[0])
    half_perp = (perp[0] / 2, perp[1] / 2)
    return (M[0] + direction * half_perp[0], M[1] + direction * half_perp[1])

def get_center_pair(frontLeft, frontRight, backLeft, backRight):
    frontMid = MidPoint(frontLeft, frontRight)
    backMid = MidPoint(backLeft, backRight)
    return frontMid, backMid

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
            frontLeftCorner = find_fourth_corner(frontRightCorner, backLeftCorner, backRightCorner)
        if frontRightCorner and backLeftCorner:
            frontLeftCorner = (backLeftCorner[0], frontRightCorner[1])
        elif frontRightCorner and backRightCorner:
            frontLeftCorner = (frontRightCorner[0], frontRightCorner[1])
        elif backLeftCorner and backRightCorner:
            frontLeftCorner = (backLeftCorner[0], backLeftCorner[1] + height)
        print(f"\nfrontLeft: {frontLeftCorner}\n")
    
    if not frontRightCorner:
        if frontLeftCorner and backLeftCorner and backRightCorner:
            frontRightCorner = find_fourth_corner(frontLeftCorner, backLeftCorner, backRightCorner)
        elif frontLeftCorner and backRightCorner:
            print("Calculating frontRightCorner from frontLeftCorner and backRightCorner")
            frontRightCorner = find_Top_Corner(frontLeftCorner, backRightCorner)
        elif frontLeftCorner and backLeftCorner:
            print("Calculating frontRightCorner from frontLeftCorner and backLeftCorner")
            frontRightCorner = (frontLeftCorner[0] + width, frontLeftCorner[1])
        elif backLeftCorner and backRightCorner:
            print("Calculating frontRightCorner from backLeftCorner and backRightCorner")
            frontRightCorner = (backRightCorner[0], backRightCorner[1] + height)
        print(f"\nfrontRightCorner: {frontRightCorner}\n")
        

    if not backLeftCorner:
        if backRightCorner and frontRightCorner and frontLeftCorner:
            backLeftCorner = find_fourth_corner(frontRightCorner, frontLeftCorner, backRightCorner)
        if backRightCorner and frontLeftCorner:
            backLeftCorner = find_Bottom_Corner(frontLeftCorner, backRightCorner)
        elif frontLeftCorner and frontRightCorner:
            backLeftCorner = (frontLeftCorner[0], frontLeftCorner[1] - height)
        elif frontRightCorner and backRightCorner:
            backLeftCorner = (backRightCorner[0] - width, backRightCorner[1])
        print(f"\nbackLeftCorner: {backLeftCorner}\n")
        

    if not backRightCorner:
        if backLeftCorner and frontLeftCorner and frontRightCorner:
            backRightCorner = find_fourth_corner(frontLeftCorner, frontRightCorner, backLeftCorner)
        if backLeftCorner and frontRightCorner:
            backRightCorner = (frontRightCorner[0], backLeftCorner[1])
        elif frontLeftCorner and frontRightCorner:
            backRightCorner = (frontRightCorner[0], frontRightCorner[1] - height)
        elif frontLeftCorner and backLeftCorner:
            backRightCorner = (backLeftCorner[0] + width, backLeftCorner[1])
        print(f"\nbackRight: {backRightCorner}\n")
        

    # Now calculate points
    if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
        print(f"\n Front Left Corner: {frontLeftCorner}: Front Right Corner {frontRightCorner}: Back Left Corner {backLeftCorner}: Back Right Corner {backRightCorner}")
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        print(f"\n Forward point {forwardsPoint}, Backward points {backwardsPoint} \n")
        return (forwardsPoint, backwardsPoint)
    else:
        return((0,0),(0,0))
        #raise ValueError("Not enough information to calculate corners.")

def VectorCalculation(frontLeftCorner=None, backLeftCorner=None, backRightCorner=None, frontRightCorner=None):
    if frontLeftCorner and backLeftCorner:
        dx = frontLeftCorner[0] - backLeftCorner[0]
        dy = frontLeftCorner[1] - backLeftCorner[1]
        return (dx, dy)
    elif frontLeftCorner and backRightCorner:
        dx = frontLeftCorner[0] - backRightCorner[0]
        dy = frontLeftCorner[1] - backRightCorner[1]
        return (dx, dy)
    return (0.0, 0.0)


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
    perp_scaled = scale(perp, height)

    C = add(B, perp_scaled)
    D = add(A, perp_scaled)
    return C, D