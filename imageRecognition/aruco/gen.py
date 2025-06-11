import cv2
import cv2.aruco as aruco
# pip install opencv-contrib-python

# Use predefined dictionary (4x4 with 50 markers)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Generate and save 4 markers
for marker_id in range(4):
    img = aruco.generateImageMarker(aruco_dict, marker_id, 200)
    cv2.imwrite(f"aruco_marker_{marker_id}.png", img)
