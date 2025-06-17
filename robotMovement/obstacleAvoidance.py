import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from shapely.geometry import Polygon, box
from shapely.geometry import LineString
import numpy as np

ROBOT_WIDTH = 119

def calculateDistance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def robotPath(fromPos, toPos, robotWidth=ROBOT_WIDTH):
    # Simulate robot body swept along the path
    path = LineString([fromPos, toPos])
    return path.buffer(robotWidth / 2, cap_style=2)


def pathIntersectsObstacle(polygon, obstacle):
    obs = box(obstacle[0][0], obstacle[0][1], obstacle[1][0], obstacle[1][1])
    return polygon.intersects(obs)


def avoidObstacle(robotPos, targetPos, obstacle, robotWidth):
    # Initial swept path check from robot to target
    if not pathIntersectsObstacle(robotPath(robotPos, targetPos, robotWidth), obstacle):
        return None

    xMin, yMin = obstacle[0]
    xMax, yMax = obstacle[1]

    margin = 200  # Pixels to avoid obstacle by
    candidates = [
        ((xMin + xMax)/2, yMax + margin),  # above
        ((xMin + xMax)/2, yMin - margin),  # below
        (xMin - margin, (yMin + yMax)/2),  # left
        (xMax + margin, (yMin + yMax)/2),  # right
        (xMin - margin, yMax + margin),    # top-left
        (xMax + margin, yMax + margin),    # top-right
        (xMin - margin, yMin - margin),    # bottom-left
        (xMax + margin, yMin - margin),    # bottom-right
    ]

    valid = []
    for candidate in candidates:
        path1 = robotPath(robotPos, candidate, robotWidth)
        path2 = robotPath(candidate, targetPos, robotWidth)

        if pathIntersectsObstacle(path1, obstacle):
            continue
        if pathIntersectsObstacle(path2, obstacle):
            continue

        totalDist = calculateDistance(robotPos, candidate) + calculateDistance(candidate, targetPos)
        valid.append((candidate, totalDist))

    if valid:
        bestIntermediatePoint = min(valid, key=lambda x: x[1])
        return bestIntermediatePoint[0]
    else:
        return None

#------------------------------------------------------------------------------------------------
# Visualization and testing 
# chatGPT used for the below visualization code and test cases

# def computeFrontCornersFromPose(position, headingTarget, robotWidth):
#     dx = headingTarget[0] - position[0]
#     dy = headingTarget[1] - position[1]
#     length = math.hypot(dx, dy)
#     if length == 0:
#         return position, position

#     dx /= length
#     dy /= length

#     perp_x = -dy
#     perp_y = dx

#     offset_x = perp_x * (robotWidth / 2)
#     offset_y = perp_y * (robotWidth / 2)

#     frontLeft = (position[0] + offset_x, position[1] + offset_y)
#     frontRight = (position[0] - offset_x, position[1] - offset_y)

#     return frontLeft, frontRight

# def visualizeScenario(robotPos, targetPos, obstacle, robotWidth, title="Scenario"):
#     # frontLeftCorner, frontRightCorner = computeFrontCornersFromPose(robotPos, targetPos, robotWidth)
#     waypoint = avoidObstacle(robotPos, targetPos, obstacle, robotWidth)

#     fig, ax = plt.subplots()

#     ax.plot(*robotPos, 'bo', label="Robot Center")
#     ax.plot(*targetPos, 'go', label="Target")
#     # ax.plot(*frontLeftCorner, 'co', label="Front Left")
#     # ax.plot(*frontRightCorner, 'mo', label="Front Right")

#     xMin, yMin = obstacle[0]
#     xMax, yMax = obstacle[1]
#     rect_patch = patches.Rectangle((xMin, yMin), xMax - xMin, yMax - yMin,
#                                    linewidth=2, edgecolor='red', facecolor='red', alpha=0.3, label="Obstacle")
#     ax.add_patch(rect_patch)

#     if waypoint:
#         ax.plot(*waypoint, 'ro', label="Waypoint")
#         ax.plot([robotPos[0], waypoint[0]], [robotPos[1], waypoint[1]], 'b-', label="To Waypoint")
#         ax.plot([waypoint[0], targetPos[0]], [waypoint[1], targetPos[1]], 'g-', label="To Target")

#         # Visualize swept areas (optional debugging)
#         path1 = robotPath(robotPos, waypoint, robotWidth)
#         path2 = robotPath(waypoint, targetPos, robotWidth)
#         ax.add_patch(patches.Polygon(list(path1.exterior.coords), color='blue', alpha=0.1))
#         ax.add_patch(patches.Polygon(list(path2.exterior.coords), color='green', alpha=0.1))
#     else:
#         ax.plot([robotPos[0], targetPos[0]], [robotPos[1], targetPos[1]], 'k--', label="Direct Path")
#         path = robotPath(robotPos, targetPos, robotWidth)
#         ax.add_patch(patches.Polygon(list(path.exterior.coords), color='gray', alpha=0.1))

#     ax.set_title(title)
#     ax.set_aspect('equal')
#     ax.grid(True)
#     ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
#     plt.tight_layout()
#     plt.show()

# # Test cases
# test_cases = [
#     {
#         "robotPos": (100, 100),
#         "targetPos": (400, 400),
#         "obstacle": [(200, 200), (300, 300)],
#         "title": "Obstacle in Diagonal Path"
#     },
#     {
#         "robotPos": (100, 100),
#         "targetPos": (400, 100),
#         "obstacle": [(200, 50), (300, 150)],
#         "title": "Obstacle in Horizontal Path"
#     },
#     {
#         "robotPos": (100, 400),
#         "targetPos": (100, 100),
#         "obstacle": [(50, 200), (150, 300)],
#         "title": "Vertical Obstacle"
#     },
#     {
#         "robotPos": (50, 50),
#         "targetPos": (450, 50),
#         "obstacle": [(200, 0), (300, 100)],
#         "title": "Skimming Along Obstacle Bottom"
#     },
#     {
#         "robotPos": (100, 100),
#         "targetPos": (400, 400),
#         "obstacle": [(500, 500), (600, 600)],
#         "title": "Obstacle Not in Path"
#     },
# ]

# robotWidth = 119  # pixels

# for test in test_cases:
#     visualizeScenario(test["robotPos"], test["targetPos"], test["obstacle"], robotWidth, test["title"])
