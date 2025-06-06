import numpy as np
import math
from distanceBetweenObjects import calculateDistance
import heapq
# from robotMovement.distanceBetweenObjects import calculateDistance

GRID_RESOLUTION = 10

# def toGridCoords(x, y):
#         return (x // GRID_RESOLUTION, y // GRID_RESOLUTION)
    
# def toPixelCoords(gridX, gridY):
#     return (gridX * GRID_RESOLUTION, gridY * GRID_RESOLUTION)

def toGridCoords(x, y, fieldOrigin=(0, 0)):
    """Convert pixel coordinates to grid coordinates"""
    adjusted_x = x - fieldOrigin[0]
    adjusted_y = y - fieldOrigin[1]
    return (int(adjusted_x // GRID_RESOLUTION), int(adjusted_y // GRID_RESOLUTION))
    
def toPixelCoords(gridX, gridY, fieldOrigin=(0, 0)):
    """Convert grid coordinates to pixel coordinates"""
    pixel_x = gridX * GRID_RESOLUTION + fieldOrigin[0] + GRID_RESOLUTION // 2
    pixel_y = gridY * GRID_RESOLUTION + fieldOrigin[1] + GRID_RESOLUTION // 2
    return (pixel_x, pixel_y)
    
def heuristic(a, b):
    # Calculates euclidean distance in grid coordinates
    # Takes grid points as input.
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.hypot(dx, dy)


def calculateMarkedGrid(fieldPixelSize, detectedObstacles):
    # Calculates a grid path from starting point to ending point
    # Resolution of grid. The smaller this is the better the accuracy, but the more computation power required.
    # GRID_RESOLUTION = 10
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
                    moveCost = math.sqrt(2) if dx != 0 and dy != 0 else 1
                    tentativeG = currentG + moveCost
                    
                    # tentativeG = currentG + 1

                    if neighbor not in gScore or tentativeG < gScore[neighbor]:
                        gScore[neighbor] = tentativeG
                        fScore = tentativeG + heuristic(neighbor, goal)
                        heapq.heappush(openSet, (fScore, tentativeG, neighbor))
                        cameFrom[neighbor] = current

    return None


class PathFollower:
    """Class to handle path following logic"""
    
    def __init__(self, lookahead_distance=50):
        self.current_path = None
        self.current_target_index = 0
        self.lookahead_distance = lookahead_distance
        self.path_complete = False
    
    def setPath(self, path, fieldOrigin=(0, 0)):
        """Set a new path to follow"""
        if path is None or len(path) == 0:
            self.current_path = None
            self.path_complete = True
            return
            
        # Convert grid path to pixel coordinates
        self.current_path = [toPixelCoords(point[0], point[1], fieldOrigin) for point in path]
        self.current_target_index = 0 if len(self.current_path) > 1 else 0
        self.path_complete = False
        
    def getNextTarget(self, robotPos):
        """Get the next target point along the path"""
        if (self.current_path is None or len(self.current_path) == 0 or 
            self.path_complete or self.current_target_index >= len(self.current_path)):
            return None
    
        # Check if we've reached the current target
        current_target = self.current_path[self.current_target_index]
        distance_to_target = calculateDistance(robotPos, current_target)
        
        # If close to current target, move to next one
        if distance_to_target < self.lookahead_distance:
            self.current_target_index += 1
            
            # Check if we've reached the end of the path
            if self.current_target_index >= len(self.current_path):
                self.path_complete = True
                return None
                
            return self.current_path[self.current_target_index]
        
        return current_target
        
    def isPathComplete(self):
        """Check if the current path has been completed"""
        return self.path_complete
        
    def getCurrentPath(self):
        """Get the current path for debugging/visualization"""
        return self.current_path


def getFieldSize(playfield):
    """Calculate the size of the playfield"""
    if playfield is None or len(playfield) < 2:
        return (800, 600)  # Default size
    
    width = abs(max(playfield[:, 0]) - min(playfield[:, 0]))
    height = abs(max(playfield[:, 1]) - min(playfield[:, 1]))
    return (width, height)



# Testing of creating marked grid
testFieldPixelSize = (200, 100)
testGridResolution = 10
testFieldWidthPx, testFieldHeightPx = testFieldPixelSize
testGridWidth = testFieldWidthPx // testGridResolution
testGridHeight = testFieldHeightPx // testGridResolution
testGridBeforeObstacles = np.array([[0 for _ in range(testGridWidth)] for _ in range(testGridHeight)])
testObstacles = [((20, 20), (30, 30)), ((70, 25), (120, 75)), ((140, 50), (180, 100))]
testGridObstaclesMarked = calculateMarkedGrid(testFieldPixelSize, testObstacles)

# print(f"Grid before:\n {testGridBeforeObstacles}")
# print()
print(f"Grid With Obstacles:\n {testGridObstaclesMarked}")


# Testing of astar search on grid
start = (0, 0)
end = (9, 19)

path = astar(testGridObstaclesMarked, start, end, heuristic)
print("Path:", path)
    



