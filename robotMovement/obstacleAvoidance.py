import numpy as np
import math
from distanceBetweenObjects import calculateDistance
import heapq
# from robotMovement.distanceBetweenObjects import calculateDistance

GRID_RESOLUTION = 10

def toGridCoords(x, y, gridResolution):
        return (x // gridResolution, y // gridResolution)
    
def toPixelCoords(gridX, gridY, gridResolution):
    return (gridX * gridResolution, gridY * gridResolution)
    
def heuristic(a, b):
    # probably euclidean or manhatten distance.
    # Takes grid points as input.
    
    # pixelA = toPixelCoords(a)
    # pixelB = toPixelCoords(b)
    pixelA, pixelB = toPixelCoords(a, b, GRID_RESOLUTION)

    euclideanDistance = calculateDistance(pixelA, pixelB)
    return euclideanDistance


def calculateMarkedGrid(fieldPixelSize, detectedObstacles):
    # Calculates a grid path from starting point to ending point
    # Resolution of grid. The smaller this is the better the accuracy, but the more computation power required.
    # gridResolution = 10
    fieldWidthPx, fieldHeightPx = fieldPixelSize    
    # Width of grid in nr of cells
    gridWidth = fieldWidthPx // GRID_RESOLUTION
    # Height of grid in nr of cells
    gridHeight = fieldHeightPx // GRID_RESOLUTION

    grid = [[0 for _ in range(gridWidth)] for _ in range(gridHeight)]

    cellWidthPx = fieldWidthPx / gridWidth 
    cellHeightPx = fieldHeightPx / gridHeight
    # Assume each obstacle is a list or tuple of two points, each point being a tuple.
    for obstacle in detectedObstacles:
        # for each obstacle figure out all grid points it overlaps and set them to 1.
        
        xMin, yMin = obstacle[0]
        xMax, yMax = obstacle[1]

        # Make sure min <= max
        xMin, xMax = sorted((xMin, xMax))
        yMin, yMax = sorted((yMin, yMax))

        colStart = max(0, min(gridWidth - 1, int(math.floor(xMin / cellWidthPx))))
        colEnd   = max(0, min(gridWidth - 1, int(math.ceil(xMax / cellWidthPx) - 1)))
        rowStart = max(0, min(gridHeight - 1, int(math.floor(yMin / cellHeightPx))))
        rowEnd   = max(0, min(gridHeight - 1, int(math.ceil(yMax / cellHeightPx) - 1)))

        for row in range(rowStart, rowEnd + 1):
             for col in range(colStart, colEnd + 1):
                  grid[row][col] = 1

    return np.array(grid)


def astar(grid, start, goal, heuristic):
    # path finding from start to goal on the grid
    n, m = grid.shape
    openSet = []
    heapq.heappush(openSet, (0 + heuristic(start, goal), 0, start))

    cameFrom = {}

    gScore = {start: 0}

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]

    while openSet:
        _, currentG, current = heapq.heappop(openSet)

        if current == goal:
            # Reconstruct the path
            path = [current]
            while current in cameFrom:
                 current = cameFrom[current]
                 path.append(current)
            path.reverse()
            return path
        
        for dx, dy in directions:
            neighbor = current[0] + dx, current[1] + dy
            # Check bounds 
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m:
                #  check if walkable
                if grid[neighbor[0], neighbor[1]] == 0:
                    tentativeG = currentG + 1

                    if neighbor not in gScore or tentativeG < gScore[neighbor]:
                        gScore[neighbor] = tentativeG
                        fScore = tentativeG + heuristic(neighbor, goal)
                        heapq.heappush(openSet, (fScore, tentativeG, neighbor))
                        cameFrom[neighbor] = current

    return None

        



# Testing of creating marked grid
testFieldPixelSize = (200, 100)
testGridResolution = 10
testFieldWidthPx, testFieldHeightPx = testFieldPixelSize
testGridWidth = testFieldWidthPx // testGridResolution
testGridHeight = testFieldHeightPx // testGridResolution
testGridBeforeObstacles = np.array([[0 for _ in range(testGridWidth)] for _ in range(testGridHeight)])
testObstacles = [((20, 20), (30, 30)), ((70, 25), (120, 75)), ((140, 50), (180, 100))]
testGridObstaclesMarked = calculateMarkedGrid(testFieldPixelSize, testObstacles)

print(f"Grid before:\n {testGridBeforeObstacles}")
print()
print(f"Grid With Obstacles:\n {testGridObstaclesMarked}")


# Testing of astar search on grid
start = (0, 0)
end = (9, 19)

path = astar(testGridObstaclesMarked, start, end, heuristic)
print("Path:", path)
    



