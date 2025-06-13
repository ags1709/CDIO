# from robotMovement.distanceBetweenObjects import getDistance
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def getDistance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Check if the points A, B, C are in counter clockwise order
def ccw(A, B, C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

# Check if line segment from A-B intersects with line segment from C-D
def segments_intersect(A, B, C, D):
    return (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D))

# TODO: 
def doesLineIntersectRectangle(A, B, obstacle):
    xMin, yMin = obstacle[0]
    xMax, yMax = obstacle[1]

    if segments_intersect(A, B, (xMin, yMin), (xMax, yMin)) or \
   segments_intersect(A, B, (xMax, yMin), (xMax, yMax)) or \
   segments_intersect(A, B, (xMax, yMax), (xMin, yMax)) or \
   segments_intersect(A, B, (xMin, yMax), (xMin, yMin)):
       return True
    return False

# Given robot and target position and obstacles, check if an intermediary point is necessary to avoid and if so, calculate it.
def avoidObstacle(robotPos, targetPos, obstacle):
    """If a straight path from robot to target would collide with obstacle, an intermediate point is returned that can be safely navigated
    to before then navigating straight to target point. If not, returns None"""

    if not doesLineIntersectRectangle(robotPos, targetPos, obstacle):
        return None

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
        if not doesLineIntersectRectangle(robotPos, candidate, obstacle) and not doesLineIntersectRectangle(candidate, targetPos, obstacle):
            totalDist = getDistance(robotPos, candidate) + getDistance(candidate, targetPos)
            valid.append((candidate, totalDist))
    
    if valid:
        bestIntermediatePoint = min(valid, key=lambda x: x[1])
        return bestIntermediatePoint[0]
    else:
        return None

    


def visualizeScenario(robotPos, targetPos, obstacle, title="Scenario"):
    waypoint = avoidObstacle(robotPos, targetPos, obstacle)

    fig, ax = plt.subplots()

    # Plot points
    ax.plot(*robotPos, 'bo', label="Robot (A)")
    ax.plot(*targetPos, 'go', label="Target (B)")

    # Unpack obstacle
    xMin, yMin = obstacle[0]
    xMax, yMax = obstacle[1]
    width = xMax - xMin
    height = yMax - yMin

    # Draw the obstacle rectangle with better visibility
    rect_patch = patches.Rectangle(
        (xMin, yMin), width, height,
        linewidth=2,
        edgecolor='red',
        facecolor='red',
        alpha=0.3,  # semi-transparent
        label="Obstacle"
    )
    ax.add_patch(rect_patch)

    # Draw direct path
    ax.plot([robotPos[0], targetPos[0]], [robotPos[1], targetPos[1]], 'k--', label="Direct Path")

    # If an intermediate point was found
    if waypoint:
        ax.plot(*waypoint, 'ro', label="Waypoint")
        ax.plot([robotPos[0], waypoint[0]], [robotPos[1], waypoint[1]], 'b-', label="Path to Waypoint")
        ax.plot([waypoint[0], targetPos[0]], [waypoint[1], targetPos[1]], 'g-', label="Path to Target")

    # Title, grid, aspect
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True)

    # Move the legend to an empty corner
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    # Expand layout to avoid clipping
    plt.tight_layout()
    plt.show()


test_cases = [
    {
        "robotPos": (100, 100),
        "targetPos": (400, 400),
        "obstacle": [(200, 200), (300, 300)],
        "title": "Obstacle in Diagonal Path"
    },
    {
        "robotPos": (100, 100),
        "targetPos": (400, 100),
        "obstacle": [(200, 50), (300, 150)],
        "title": "Obstacle in Horizontal Path"
    },
    {
        "robotPos": (100, 400),
        "targetPos": (100, 100),
        "obstacle": [(50, 200), (150, 300)],
        "title": "Vertical Obstacle"
    },
    {
        "robotPos": (50, 50),
        "targetPos": (450, 50),
        "obstacle": [(200, 0), (300, 100)],
        "title": "Skimming Along Obstacle Bottom"
    },
    {
        "robotPos": (100, 100),
        "targetPos": (400, 400),
        "obstacle": [(500, 500), (600, 600)],
        "title": "Obstacle Not in Path"
    },
]

for test in test_cases:
    visualizeScenario(test["robotPos"], test["targetPos"], test["obstacle"], test["title"])