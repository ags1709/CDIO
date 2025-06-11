



# def lineIntersectRectangle(point1, point2, rectangle):

def ccw(A, B, C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def segments_intersect(A, B, C, D):
    return (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D))

def doesLineIntersectRectangle(A, B, xMin, yMin, xMax, yMax):
    if segments_intersect(A, B, (xMin, yMin), (xMax, yMin)) or \
   segments_intersect(A, B, (xMax, yMin), (xMax, yMax)) or \
   segments_intersect(A, B, (xMax, yMax), (xMin, yMax)) or \
   segments_intersect(A, B, (xMin, yMax), (xMin, yMin)):
       return True

# Given robot and target position and obstacles, check if an intermediary point is necessary to avoid and if so, calculate it.
# 
def avoidObstacle(robotPos, targetPos, obstacle):
    xMin, yMin = obstacle[0]
    xMax, yMax = obstacle[1]

    # margin with which to avoid the obstacle in pixels
    margin = 50

    candidates = [
        ((xMin + xMax)/2, yMax + margin),  # above
        ((xMin + xMax)/2, yMin - margin),  # below
        (xMin - margin, (yMin + yMax)/2),  # xMin
        (xMax + margin, (yMin + yMax)/2),  # xMax
        (xMin - margin, yMax + margin),     # yMin-xMin
        (xMax + margin, yMax + margin),     # yMin-xMax
        (xMin - margin, yMin - margin),     # yMax-xMin
        (xMax + margin, yMin - margin),     # yMax-xMax
    ]

    valid = []
    for candidate in candidates:
        

    