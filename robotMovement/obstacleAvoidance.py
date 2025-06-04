import numpy as np
import math
# from robotMovement.distanceBetweenObjects import calculateDistance

def toGridCoords(self, x, y, grid_resolution):
        return (x // grid_resolution, y // grid_resolution)
    
def toPixelCoords(self, gridX, gridY, grid_resolution):
    return (gridX * grid_resolution, gridY * grid_resolution)
    
def heuristic(self, a, b):
    # probably euclidean or manhatten distance.
    # Takes grid points as input.
    
    pixelA = toPixelCoords(a)
    pixelB = toPixelCoords(b)

    # euclideanDistance = calculateDistance(pixelA, pixelB)
    # return euclideanDistance
    return


def calculateMarkedGrid(fieldPixelSize, detectedObstacles):
    # Calculates a grid path from starting point to ending point
    # Resolution of grid. The smaller this is the better the accuracy, but the more computation power required.
    gridResolution = 10
    fieldWidthPx, fieldHeightPx = fieldPixelSize    
    # Width of grid in nr of cells
    gridWidth = fieldWidthPx // gridResolution
    # Height of grid in nr of cells
    gridHeight = fieldHeightPx // gridResolution

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

def astar(self, start, goal):
    # path finding from start to goal on the grid
    pass



testFieldPixelSize = (200, 100)
testGridResolution = 10
testFieldWidthPx, testFieldHeightPx = testFieldPixelSize
testGridWidth = testFieldWidthPx // testGridResolution
testGridHeight = testFieldHeightPx // testGridResolution
testGridBeforeObstacles = np.array([[0 for _ in range(testGridWidth)] for _ in range(testGridHeight)])
testObstacles = [((20, 20), (30, 30)), ((140, 50), (180, 100))]
testGridObstaclesMarked = calculateMarkedGrid(testFieldPixelSize, testObstacles)


print(f"Grid before:\n {testGridBeforeObstacles}")
print()
print(f"Grid With Obstacles:\n {testGridObstaclesMarked}")


    



