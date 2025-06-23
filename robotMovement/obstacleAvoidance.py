import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from shapely.geometry import Polygon, box
from shapely.geometry import LineString
import numpy as np

# ROBOT_WIDTH = 119
ROBOT_WIDTH = 135
MARGIN = 150

def calculateDistance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def robotPath(fromPos, toPos, robotWidth=ROBOT_WIDTH):
    # Simulate robot body swept along the path
    path = LineString([fromPos, toPos])
    return path.buffer(robotWidth / 2, cap_style=2)


def pathIntersectsObstacle(polygon, obstacle):
    obs = box(obstacle[0][0], obstacle[0][1], obstacle[1][0], obstacle[1][1])
    return polygon.intersects(obs)

# ------------------------------------------------------------------------------------------
# New avoid obstacle attempt to handle edge case
def avoidObstacle(robotPos, targetPos, obstacle, robotWidth=119, depth=0, maxDepth=5, visited=None):
    if visited is None:
        visited = set()

    if not pathIntersectsObstacle(robotPath(robotPos, targetPos, robotWidth), obstacle):
        return [targetPos]  # Return path with just the target

    # Avoid infinite recursion
    if depth >= maxDepth:
        return None

    visited.add((round(robotPos[0]), round(robotPos[1])))

    xMin, yMin = obstacle[0]
    xMax, yMax = obstacle[1]

    margin = MARGIN  # Pixels to avoid obstacle by

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

    # center_x = (xMin + xMax) / 2
    # center_y = (yMin + yMax) / 2

    # num_candidates = 20
    # radius = max(xMax - xMin, yMax - yMin) / 2 + margin  # Distance from obstacle

    # angles = np.linspace(0, 2 * np.pi, num_candidates, endpoint=False)

    # candidates = [
    #     (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
    #     for angle in angles
    # ]

    validPaths = []

    for candidate in candidates:
        rounded = (round(candidate[0]), round(candidate[1]))
        if rounded in visited:
            continue

        path1 = robotPath(robotPos, candidate, robotWidth)
        if pathIntersectsObstacle(path1, obstacle):
            continue

        # Recursively check from this candidate to target
        subPath = avoidObstacle(candidate, targetPos, obstacle, robotWidth, depth + 1, maxDepth, visited.copy())
        if subPath:
            totalDist = calculateDistance(robotPos, candidate) + sum(
                calculateDistance(subPath[i], subPath[i + 1]) for i in range(len(subPath) - 1)
            )
            validPaths.append(([candidate] + subPath, totalDist))

    if validPaths:
        # Return the shortest valid full path
        bestPath = min(validPaths, key=lambda x: x[1])[0]
        return bestPath

    return None  # No valid path found


# ------------------------------------------------------------------------------------------------
# Visualization of obstacle avoidance. DO NOT DELETE.

# def visualizeScenario(robotPos, targetPos, obstacle, robotWidth, title="Scenario"):
#     direct_path_valid = not pathIntersectsObstacle(robotPath(robotPos, targetPos, robotWidth), obstacle)

#     if direct_path_valid:
#         path = [targetPos]  # Just go straight to the target
#     else:
#         path = avoidObstacle(robotPos, targetPos, obstacle, robotWidth)

#     fig, ax = plt.subplots()

#     ax.plot(*robotPos, 'bo', label="Robot Start")
#     ax.plot(*targetPos, 'go', label="Target")

#     # Draw the obstacle
#     xMin, yMin = obstacle[0]
#     xMax, yMax = obstacle[1]
#     rect_patch = patches.Rectangle((xMin, yMin), xMax - xMin, yMax - yMin,
#                                    linewidth=2, edgecolor='red', facecolor='red', alpha=0.3, label="Obstacle")
#     ax.add_patch(rect_patch)

#     if path:
#         full_path = [robotPos] + path
#         for i in range(len(full_path) - 1):
#             start = full_path[i]
#             end = full_path[i + 1]

#             # Plot segment line
#             ax.plot([start[0], end[0]], [start[1], end[1]],
#                     'b-' if i == 0 else 'g-', label="To Waypoint" if i == 0 else None)

#             # Plot swept path
#             swept = robotPath(start, end, robotWidth)
#             ax.add_patch(patches.Polygon(list(swept.exterior.coords), alpha=0.1,
#                                          color='blue' if i == 0 else 'green'))

#             # Plot waypoints
#             if i > 0 and i < len(full_path) - 1:  # Only intermediate waypoints
#                 ax.plot(*start, 'ro', label="Waypoint" if i == 1 else None)

#     else:
#         # No valid path at all
#         ax.plot([robotPos[0], targetPos[0]], [robotPos[1], targetPos[1]], 'k--', label="Blocked Path")
#         swept = robotPath(robotPos, targetPos, robotWidth)
#         ax.add_patch(patches.Polygon(list(swept.exterior.coords), alpha=0.1, color='gray'))

#     ax.set_title(title)
#     ax.set_aspect('equal')
#     ax.grid(True)
#     ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
#     plt.tight_layout()
#     plt.show()


# # # Test cases
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

# for test in test_cases:
#     visualizeScenario(test["robotPos"], test["targetPos"], test["obstacle"], ROBOT_WIDTH, test["title"])

