import numpy as np

color_ranges = {
    "Orange": [np.array([0, 90, 185]), np.array([100, 220, 255])],
    "Dark Blue": [np.array([0, 0, 100]), np.array([100, 100, 255])],
    "Magenta": [np.array([100, 0, 150]), np.array([255, 150, 255])],
    "White": [np.array([120, 120, 120]), np.array([255, 255, 255])]
    #"Gray": [np.array([50, 50, 50]), np.array([200, 200, 200])]
}

def get_color_name(bgr_value):
    for color_name, (lower, upper) in color_ranges.items():
        if np.all(bgr_value >= lower) and np.all(bgr_value <= upper):
            return color_name
    return "Unknown"  # Return "Unknown" if no match