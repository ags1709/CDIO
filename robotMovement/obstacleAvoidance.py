import numpy as np
from robotMovement.distanceBetweenObjects import calculateDistance

def toGridCoords(self, x, y, grid_resolution):
        return (x // grid_resolution, y // grid_resolution)
    
def toPixelCoords(self, gridX, gridY, grid_resolution):
    return (gridX * grid_resolution, gridY * grid_resolution)
    
def heuristic(self, a, b):
    # probably euclidean or manhatten distance.
    # Takes grid points as input.
    
    pixelA = toPixelCoords(a)
    pixelB = toPixelCoords(b)

    euclideanDistance = calculateDistance(pixelA, pixelB)
    return euclideanDistance


def returnPath(startingPoint, endingPoint, fieldPixelSize, detectedObstacles):
    # Calculates a grid path from starting point to ending point
    # Resolution of grid. The smaller this is the better the accuracy, but the more computation power required.
    GRID_RESOLUTION = 10
    GRID_WIDTH = fieldPixelSize[0] // GRID_RESOLUTION
    GRID_HEIGHT = fieldPixelSize[1] // GRID_RESOLUTION

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    for obstacle in detectedObstacles:
        # for each obstacle figure out all grid points it overlaps and set them to 1.
        xMin, yMin = obstacle[0]
        xMax, yMax = obstacle[1]
        colStart = int(xMin / GRID_WIDTH) 
        colEnd = int(xMax / GRID_WIDTH)
        rowStart = int(yMin / GRID_HEIGHT)
        rowEnd = int(yMax / GRID_HEIGHT)

        # obstacleGridPos = toGridCoords(obstacle[0], obstacle[1])
        # grid[obstacleGridPos[1]][obstacleGridPos[0]] = 1

    


    

    def astar(self, start, goal):
        # path finding from start to goal on the grid
        pass


