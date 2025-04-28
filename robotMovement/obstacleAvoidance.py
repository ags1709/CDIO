import numpy as np


class obstacleAvoidance:
    # FieldPixelSize is expected in (width, height)
    def __init__(self, fieldPixelSize):
        # Resolution of grid. The smaller this is the better the accuracy, but the more computation power required.
        self. GRID_RESOLUTION = 10
        self.GRID_WIDTH = fieldPixelSize[0] // self.GRID_RESOLUTION
        self. GRID_HEIGHT = fieldPixelSize[1] // self.GRID_RESOLUTION

    def toGridCoords(self, x, y):
        return (x // self.GRID_RESOLUTION, y // self.GRID_RESOLUTION)
    
    def toPixelCoords(self, gridX, gridY):
        return (gridX * self.GRID_RESOLUTION, gridY * self.GRID_RESOLUTION)
    
    def heuristic(self, a, b):
        # probably euclidean or manhatten distance.
        # Takes grid points as input.
        pass

    def astar(self, start, goal):
        # path finding from start to goal on the grid
        pass


    
# Testing
OA = obstacleAvoidance((847, 1549))
pixelPoint = (309, 823)
gridPoint = OA.toGridCoords(pixelPoint[0], pixelPoint[1])

print(gridPoint)
