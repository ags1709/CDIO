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
        # TODO Scale the pct so it is a constant px upscale probably (rn scaled differently with bigger numbers as it is pct)
        x1 = int(x1/100*(100-scalepct))
        y1 = int(y1/100*(100-scalepct))
        x2 = int(x2/100*(100+scalepct))
        y2 = int(y2/100*(100+scalepct))
        
        
        crop_frame = cap[y1:y2,x1:x2]
        #cv2.imshow("crop frame", crop_frame)
        
        #gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        b = crop_frame[:, :, 0].astype(np.float32)
        g = crop_frame[:, :, 1].astype(np.float32)
        r = crop_frame[:, :, 2].astype(np.float32)
        # Create a mask where red is strong and green/blue are weak relative to red
        condition = (r > 110) & (g < r / 1.6) & (b < r / 1.6)
        red_thresh = condition.astype(np.uint8) * 255  # Convert to binary mask
        # Apply the mask to keep only the red pixels
        # red_thresh = cv2.bitwise_and(crop_frame, crop_frame, mask=mask)
        # red_thresh = cv2.cvtColor(red_thresh, cv2.COLOR_BGR2GRAY)
        red_thresh = cv2.GaussianBlur(red_thresh, (5, 5), 0)
        

        edges = cv2.Canny(red_thresh, 60, 255) # Note: this is a 2d array of either 0 or 255 as an int
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

        # # Apply PCA to the contour points
        # mean, eigenvectors = cv2.PCACompute(all_points.astype(np.float32), mean=np.array([]))
        
        # # The angle of the first principal component
        # dx, dy = eigenvectors[0]
        # angle_rad = math.atan2(dy, dx)
        # angle_deg = math.degrees(angle_rad)

        # # Normalize angle to [0, 180)
        # angle_deg = (angle_deg+45) % 90
        
        # # Optional: Draw PCA direction
        # center = tuple(mean[0].astype(int))
        # direction = (int(center[0] + dx*100), int(center[1] + dy*100))
        # cv2.arrowedLine(crop_frame, center, direction, (0, 255, 0), 3)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours == None:
            print("No contours found for cross")
            return
        largest_contour = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(largest_contour)
        angle_deg = rect[2]+45 # Always 45 degrees rotatated?

        print(f"Angle of cross (in degrees): {angle_deg:.2f}")

        center = rect[0]
        angle_rad = math.radians(angle_deg)
        length = 75
        x0, y0 = int(center[0]), int(center[1])
        x1 = int(x0 + length * math.cos(angle_rad))
        y1 = int(y0 + length * math.sin(angle_rad))

        # Draw arrowed line
        cv2.arrowedLine(crop_frame, (x0, y0), (x1, y1), (200, 150, 0), 2, tipLength=0.2)
    
        # Show
        cv2.imshow("Edges", edges)
        cv2.imshow("Red channel", red_thresh)
        cv2.imshow("Orientation", crop_frame)
        
        return
    else:
        print("WARNING! No cross detected, no angle detection done")