import cv2
from ultralytics import YOLO
import numpy as np
import math
from robotMovement.tools import tuple_toint

windowsize = (1280,720)
class CrossInfo:
    robot_gap: int
    middle_point: tuple
    size: int
    angle_rad: float
    robot_intermediary_corners: list

def estimateGoals(playarea: list[np.ndarray], cap, frame):
    if playarea is not None:        
        playarea
        leftGoal = (playarea[0] + playarea[3]) / 2
        rightGoal = (playarea[1] + playarea[2]) / 2
        cv2.circle(frame, tuple(map(int, leftGoal)), 30, (200, 150, 0), 3)
        cv2.circle(frame, tuple(map(int, rightGoal)), 30, (200, 150, 0), 3)
        return [leftGoal, rightGoal]
    else:
        pass
        # print("WARNING! No playfield detected, no goal estimation done")
    
def estimatePositionFromSquare(x1,y1,x2,y2):
    xCoordinate = (x1 + x2) / 2
    yCoordinate = (y1 + y2) / 2

    return (xCoordinate, yCoordinate)


def estimateCross(result, cap, frame) -> CrossInfo:
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
        x1_abs, y1_abs, x2_abs, y2_abs = xyxy
        # TODO Scale the pct so it is a constant px upscale probably (rn scaled differently with bigger numbers as it is pct)
        x1_abs = int(x1_abs/100*(100-scalepct))
        y1_abs = int(y1_abs/100*(100-scalepct))
        y2_abs = int(y2_abs/100*(100+scalepct))
        x2_abs = int(x2_abs/100*(100+scalepct))
        
        
        crop_cap = cap[y1_abs:y2_abs,x1_abs:x2_abs]
        crop_frame = frame[y1_abs:y2_abs,x1_abs:x2_abs]
        #cv2.imshow("crop frame", crop_frame)
        
        #gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        b = crop_cap[:, :, 0].astype(np.float32)
        g = crop_cap[:, :, 1].astype(np.float32)
        r = crop_cap[:, :, 2].astype(np.float32)
        # Create a mask where red is strong and green/blue are weak relative to red
        red_mask = ((r > 115) & (g < r / 1.8) & (b < r / 1.8)).astype(np.uint8) * 255
        red_thresh = cv2.GaussianBlur(red_mask, (5, 5), 0)
        

        edges = cv2.Canny(red_thresh, 60, 255) # Note: this is a 2d array of either 0 or 255 as an int
        scalepct=5
        for ball in orange_boxes:
            b_xyxy = ball.xyxy[0].cpu().numpy().astype(int)
            b_x1, b_y1, b_x2, b_y2 = b_xyxy
            b_x1 = int(max(b_x1 - x1_abs, 0)/100*(100-scalepct))
            b_x2 = int(min( max(b_x2 - x1_abs, 0) , edges.shape[0])/100*(100+scalepct))
            b_y2 = int(min( max(b_y2 - y1_abs, 0), edges.shape[1])/100*(100+scalepct))
            b_y1 = int(max(b_y1 - y1_abs, 0)/100*(100-scalepct))
            
            mask = np.ones_like(edges, dtype=np.uint8) * 255
            mask[b_y1:b_y2, b_x1:b_x2] = 0
            # Apply the mask
            edges = cv2.bitwise_and(edges, mask)
        
        contours, _ = cv2.findContours(red_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # WARNING: Perhaps use red_thresh instead of edges here?
        if contours == None:
            print("No contours found for cross")
            return
        largest_contour = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(largest_contour)
        angle_deg = rect[2]+45 # Always 45 degrees rotatated?

        #print(f"Angle of cross (in degrees): {angle_deg:.2f}")

        center = rect[0]
        info: CrossInfo = CrossInfo()
        angle_rad = math.radians(angle_deg)
        info.angle_rad = angle_rad
        length = 75
        x0, y0 = int(center[0]), int(center[1])
        x1 = int(x0 + length * math.cos(angle_rad))
        y1 = int(y0 + length * math.sin(angle_rad))

        cv2.arrowedLine(crop_frame, (x0, y0), (x1, y1), (200, 150, 0), 2, tipLength=0.2)
        
        mid_x = (x1_abs+x2_abs)/2
        mid_y = (y1_abs+y2_abs)/2
        info.robot_gap = 225
        info.robot_intermediary_corners = [ # Calculate all four corners so that the car can travel to them as intermediary
            # (Radians, gap position)
            ( (math.pi/4+angle_rad)%(math.pi*2)-math.pi, (math.cos(math.pi/4+angle_rad)*info.robot_gap + mid_x, math.sin(math.pi/4+angle_rad)*info.robot_gap + mid_y) ),
            ( (math.pi/4+angle_rad+math.pi/2)%(math.pi*2)-math.pi, (math.cos(math.pi/4+angle_rad+math.pi/2)*info.robot_gap + mid_x, math.sin(math.pi/4+angle_rad+math.pi/2)*info.robot_gap + mid_y)),
            ( (math.pi/4+angle_rad+math.pi)%(math.pi*2)-math.pi, (math.cos(math.pi/4+angle_rad+math.pi)*info.robot_gap + mid_x, math.sin(math.pi/4+angle_rad+math.pi)*info.robot_gap + mid_y)),
            ( (math.pi/4+angle_rad+math.pi/2*3)%(math.pi*2)-math.pi, (math.cos(math.pi/4+angle_rad+math.pi/2*3)*info.robot_gap + mid_x, math.sin(math.pi/4+angle_rad+math.pi/2*3)*info.robot_gap + mid_y))
        ]
        
        
        # Draw circle in cross
        info.middle_point = ( int(mid_x), int(mid_y) )
        info.size = int((x2_abs-x1_abs)/2)
        cv2.circle(frame, info.middle_point, info.size, (100,100,100), 2)
        cv2.circle(frame, info.middle_point, info.robot_gap, (130,130,130), 2)
        for im in info.robot_intermediary_corners:
            cv2.circle(frame, tuple_toint(im[1]), 2, (200,50,500), 2)
        #cv2.putText(cap, "Obstacle", (x1_abs, y1_abs), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,100,100), 2, cv2.LINE_AA)
    
        # Show
        # cv2.imshow("Edges", edges)
        # cv2.imshow("Red channel", red_thresh)
        # cv2.imshow("Orientation", crop_frame)
        
        return info
    else:
        pass
        # print("WARNING! No cross detected, no angle detection done")
        
        
def findIntermediatyCrossPoint(ball, cross_middle_point, robot_gap, cross_int_corners):
    angle_ball = math.atan2(cross_middle_point[1]-ball[1], cross_middle_point[0]-ball[0]) # Adjust with plus pi, since that is how corners are stored
    closest = (math.inf, None)
    for corner in cross_int_corners:
        if abs(corner[0] - angle_ball) < abs(closest[0] - angle_ball):
            closest = corner
    return closest[1]
        



def intersection_from_2pts_np(p1, p2, p3, p4):
    p1, p2, p3, p4 = map(np.array, [p1, p2, p3, p4])
    d1 = p2 - p1
    d2 = p4 - p3
    A = np.array([d1, -d2]).T
    b = p3 - p1

    if np.linalg.matrix_rank(A) < 2:
        return None

    try:
        t_s = np.linalg.solve(A, b)
        intersection = p1 + t_s[0] * d1
        return intersection
        #return tuple(map(int, intersection))
    except np.linalg.LinAlgError:
        return None

def estimatePlayArea(result, cap, frame) -> list[np.ndarray]:
    h, w = cap.shape[:2]
    cx, cy = w // 2, h // 2
    w8, h8 = w // 8, h // 8

    # Red pixel mask
    b, g, r = cap[:, :, 0], cap[:, :, 1], cap[:, :, 2]
    red_mask = ((r > 115) & (g < r / 1.8) & (b < r / 1.8)).astype(np.uint8) * 255
    red_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)
    
    # Show
    cv2.imshow("Red channel", cv2.resize(red_mask, (1280,720)))

    # Contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours")
        return
    points = np.vstack(contours).squeeze()

    # 8-point selection with stricter bounds
    def filter_and_pick(condition_fn, sort_key_fn, reverse=False):
        filtered = [p for p in points if condition_fn(p)]
        if not filtered:
            return None
        return sorted(filtered, key=sort_key_fn, reverse=reverse)[0]

    # 8 extreme points (2 per corner)
    # top-left
    tl_top  = filter_and_pick(lambda p: p[0] < w8*2 and p[1] < h8*2, lambda p: p[1])     # topmost
    tl_left = filter_and_pick(lambda p: p[0] < w8*2 and p[1] < h8*2, lambda p: p[0])     # leftmost

    # top-right
    tr_top   = filter_and_pick(lambda p: p[0] > w*6//8 and p[1] < h8*2, lambda p: p[1])
    tr_right = filter_and_pick(lambda p: p[0] > w*6//8 and p[1] < h8*2, lambda p: p[0], reverse=True)

    # bottom-right
    br_bottom = filter_and_pick(lambda p: p[0] > w*6//8 and p[1] > h*6//8, lambda p: p[1], reverse=True)
    br_right  = filter_and_pick(lambda p: p[0] > w*6//8 and p[1] > h*6//8, lambda p: p[0], reverse=True)

    # bottom-left
    bl_bottom = filter_and_pick(lambda p: p[0] < w8*2 and p[1] > h*6//8, lambda p: p[1], reverse=True)
    bl_left   = filter_and_pick(lambda p: p[0] < w8*2 and p[1] > h*6//8, lambda p: p[0])


    
    # Unpack for clarity
    # tl_top, tl_left, tr_top, tr_right, br_bottom, br_right, bl_bottom, bl_left = extremities

    # Define correct corner lines
    corner_lines = [
        # Top-left corner
        ((tl_left, tr_right), (tl_top, bl_bottom)),

        # Top-right corner
        ((tl_left, tr_right), (br_bottom, tr_top)),

        # Bottom-right corner
        ((br_right, bl_left), (br_bottom, tr_top)),

        # Bottom-left corner
        ((bl_left, br_right), (bl_bottom, tl_top)),
    ]
    #print(corner_lines)
    
    extremities = [tl_top, tl_left, tr_top, tr_right, br_bottom, br_right, bl_bottom, bl_left]
    # Draw points before checking for none (with try catch)
    for i, pt in enumerate(extremities):
        try:
            pt = tuple(map(int, pt))
            cv2.circle(frame, pt, 3, (0, 255, 255), -1)
        except:
            pass
    
    if any([extremitie is None for extremitie in extremities]):
        print("WARNING! at least one point in play area not found (est playarea)")
        return None


    # Compute actual corner points
    corner_points = []
    for (line1, line2) in corner_lines:
        if line1 is None or line2 is None:
            print("Error! missing corner_lines element")
            return None
        pt = intersection_from_2pts_np(*line1, *line2)
        if pt is not None:
            corner_points.append(pt)

    if any(p is None for p in extremities):
        print("Some points were not found in their 1/8 zones.")
        return

    # Compute intersections of each side
    # Sides: top, right, bottom, left
    pairs = [
        (tl_top, tl_left, tr_top, tr_right),       # top-left and top-right
        (tr_top, tr_right, br_bottom, br_right),   # top-right and bottom-right
        (br_bottom, br_right, bl_bottom, bl_left), # bottom-right and bottom-left
        (bl_bottom, bl_left, tl_top, tl_left),     # bottom-left and top-left
    ]
    corners = []
    for p1, p2, p3, p4 in pairs:
        pt = intersection_from_2pts_np(p1, p2, p3, p4)
        if pt is not None:
            corners.append(pt)

    # Draw result
    # output = cap.copy()
    # for i, pt in enumerate(corners):
    #     cv2.circle(output, pt, 10, (0, 255, 0), -1)
    #     cv2.putText(output, str(i), pt, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # for i, pt in enumerate(extremities):
    #     cv2.circle(output, pt, 5, (0, 0, 255), -1)
    
    # Draw corners
    for i, pt in enumerate(corner_points):
        pt = tuple(map(int, pt))
        cv2.circle(frame, pt, 10, (0, 255, 255), -1)
        cv2.putText(frame, f"Corner {i}", (pt[0] + 5, pt[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # # Draw lines
    # print(corner_points)
    # for (p1, p2) in [l for pair in corner_lines for l in pair]:
    #     cv2.line(output, p1, p2, (255, 0, 0), 1)


    # cv2.imshow("Play Area - Refined 8 Region Extremes", cv2.resize(output, (640, 480)))
    return corner_points


def np_int(t):
    return np.round(t).astype(int)

def estimatePlayAreaIntermediate(result, playarea, frame):
    margin = 150

    #playarea = np.array(playarea)
    if playarea is None:
        print("WARNING! Play area is none, returning (est intermediate)")
        return None
    
    tl = offset_vertex(playarea[0], playarea[1], playarea[3], margin)
    tr = offset_vertex(playarea[1], playarea[2], playarea[0], margin)
    br = offset_vertex(playarea[2], playarea[3], playarea[1], margin)
    bl = offset_vertex(playarea[3], playarea[0], playarea[2], margin)

    cv2.line(frame, np_int(tl), np_int(bl), (0, 255, 255), 2)
    cv2.line(frame, np_int(tl), np_int(tr), (0, 255, 255), 2)
    cv2.line(frame, np_int(br), np_int(tr), (0, 255, 255), 2)
    cv2.line(frame, np_int(br), np_int(bl), (0, 255, 255), 2)

    return (tl, tr, br, bl)

def offset_vertex(p1, p2, p3, distance):
    """Offsets the vertex p1 by distance inwards. p2 is the adjacent vertex in the clockwise direction, and opposite for p3."""
    # The vectors from the vertex to the adjacent vertices, rotated by 90°
    v1 = np.array((p1[1] - p2[1], p2[0] - p1[0]), float)
    v2 = np.array((p3[1] - p1[1], p1[0] - p3[0]), float)
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    v3 = v1 + v2
    v3 *= distance / np.linalg.norm(v3) / np.sqrt((1 + np.dot(v1, v2)) / 2)
    return p1 + v3

def is_point_in_polygon(point, polygon):
    """Ray casting algorithm to determine if the point is inside the polygon."""
    point = np.array(point)
    x, y = point
    n = len(polygon)
    inside = False

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        x1, y1 = p1
        x2, y2 = p2

        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xints = (y - y1) * (x2 - x1) / (y2 - y1 + 1e-12) + x1
                    if x1 == x2 or x <= xints:
                        inside = not inside
    return inside

def closest_point_on_segment(p, a, b):
    """Returns the closest point on segment ab to point p using NumPy."""
    p = np.array(p)
    a = np.array(a)
    b = np.array(b)
    ab = b - a
    t = np.dot(p - a, ab) / (np.dot(ab, ab) + 1e-12)
    t = np.clip(t, 0, 1)
    return a + t * ab

def closest_point_to_polygon(point, polygon):
    """Finds closest point on polygon edges to the given point using NumPy."""
    point = np.array(point)
    closest = None
    min_dist = float('inf')
    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]
        cp = closest_point_on_segment(point, a, b)
        dist = np.linalg.norm(cp - point)
        if dist < min_dist:
            min_dist = dist
            closest = cp
    return closest

def analyze_point_with_polygon(point, polygon):
    """
    Returns (inside: bool, closest_point: np.array)
    """
    inside = is_point_in_polygon(point, polygon)
    if inside:
        return True, np.array(point)
    else:
        closest = closest_point_to_polygon(point, polygon)
        return False, closest
