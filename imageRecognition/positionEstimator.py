import cv2
from ultralytics import YOLO
import numpy as np
import math

def estimateGoals(result, cap):
    boxes = result.boxes
    id_playfield = 3
    playfield_box = [x for x in boxes if x.cls == id_playfield]
    if len(playfield_box) > 1:
        print("WARNING! ", len(playfield_box), " playfield_boxes detected, expected 1")
    if (len(playfield_box) == 1):
        box = playfield_box[0]
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = xyxy
        ymid = int(y1+(y2-y1)/2)
        leftGoal = (x1,ymid)
        rightGoal = (x2,ymid)
        cv2.circle(cap, leftGoal, 30, (200, 150, 0), 3)
        cv2.circle(cap, rightGoal, 30, (200, 150, 0), 3)
        return [leftGoal, rightGoal]
    else:
        print("WARNING! No playfield detected, no goal estimation done")
    
def estimatePositionFromSquare(x1,y1,x2,y2):
    xCoordinate = (x1 + x2) / 2
    yCoordinate = (y1 + y2) / 2

    return (xCoordinate, yCoordinate)


def estimateCross(result, cap):
    boxes = result.boxes
    id_cross = 4
    cross_box = [x for x in boxes if x.cls == id_cross]
    
    id_orange = 1
    orange_boxes = [x for x in boxes if x.cls == id_orange]
    
    if len(cross_box) > 1:
        print("WARNING! ", len(cross_box), " crosses detected, expected 1")
    if (len(cross_box) == 1):
        box = cross_box[0]
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        scalepct=1
        x1, y1, x2, y2 = xyxy
        x1 = int(x1/100*(100-scalepct))
        y1 = int(y1/100*(100-scalepct))
        x2 = int(x2/100*(100+scalepct))
        y2 = int(y2/100*(100+scalepct))
        
        
        crop_frame = cap[y1:y2,x1:x2]
        #cv2.imshow("crop frame", crop_frame)
        
        #gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        red_channel = crop_frame[:, :, 2]
        threshold = 200 # Only keep red channel when R is over 200
        _, mask = cv2.threshold(red_channel, threshold, 255, cv2.THRESH_BINARY)
        red_thresh = cv2.bitwise_and(red_channel, red_channel, mask=mask)
        red_thresh = cv2.GaussianBlur(red_thresh, (5, 5), 0)
        

        edges = cv2.Canny(red_thresh, 200, 255) # Note: this is a 2d array of either 0 or 255 as an int
        scalepct=5
        for ball in orange_boxes:
            b_xyxy = ball.xyxy[0].cpu().numpy().astype(int)
            b_x1, b_y1, b_x2, b_y2 = b_xyxy
            b_x1 = int(max(b_x1 - x1, 0)/100*(100-scalepct))
            b_x2 = int(min( max(b_x2 - x1, 0) , edges.shape[0])/100*(100+scalepct))
            b_y2 = int(min( max(b_y2 - y1, 0), edges.shape[1])/100*(100+scalepct))
            b_y1 = int(max(b_y1 - y1, 0)/100*(100-scalepct))
            
            mask = np.ones_like(edges, dtype=np.uint8) * 255
            mask[b_y1:b_y2, b_x1:b_x2] = 0
            # Apply the mask
            edges = cv2.bitwise_and(edges, mask)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        all_points = np.vstack([cnt.reshape(-1, 2) for cnt in contours])

        # Apply PCA to the contour points
        mean, eigenvectors = cv2.PCACompute(all_points.astype(np.float32), mean=np.array([]))

        # The angle of the first principal component
        dx, dy = eigenvectors[0]
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # Normalize angle to [0, 180)
        angle_deg = angle_deg % 180

        print(f"Angle of cross (in degrees): {angle_deg:.2f}")

        # Optional: Draw PCA direction
        center = tuple(mean[0].astype(int))
        direction = (int(center[0] + dx*100), int(center[1] + dy*100))
        cv2.arrowedLine(crop_frame, center, direction, (0, 255, 0), 3)

        # Show
        cv2.imshow("Edges", edges)
        cv2.imshow("Red channel", red_thresh)
        cv2.imshow("Orientation", crop_frame)
        
        return
    else:
        print("WARNING! No cross detected, no angle detection done")