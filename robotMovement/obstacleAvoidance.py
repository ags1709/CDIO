import numpy as np

GRID_WIDTH = 20
GRID_HEIGHT = 20
GRID_RESOLUTION = 10

def toGridCoords(x, y):
    return (x // GRID_RESOLUTION, y // GRID_RESOLUTION)

def toPixelCoords(gridX, gridY):
    return (gridX * GRID_RESOLUTION, gridY * GRID_RESOLUTION)