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

def estimateGoals(playarea: list[np.ndarray], frame):
    if playarea is not None:
        leftGoal = (playarea[0] + playarea[3]) / 2
        leftGoal[1] -= 10
        # print(f"play area 0 type: {type(playarea[0])}")
        # print(f"play area 0: {playarea[0]}")
        # print(f"play area 3: {playarea[3]}")
        rightGoal = (playarea[1] + playarea[2]) / 2
        cv2.circle(frame, tuple(map(int, leftGoal)), 30, (200, 150, 0), 3)
        cv2.circle(frame, tuple(map(int, rightGoal)), 30, (200, 150, 0), 3)
        return [leftGoal, rightGoal]
    else:
        pass
        # print("WARNING! No playfield detected, no goal estimation done")

def estimateGoalNormals(playarea: list[np.ndarray], frame):
    leftGoalNormal = edge_normal(playarea[3], playarea[0])
    rightGoalNormal = edge_normal(playarea[1], playarea[2])
    return [leftGoalNormal, rightGoalNormal]

def estimatePositionFromSquare(x1,y1,x2,y2):
    xCoordinate = (x1 + x2) / 2
    yCoordinate = (y1 + y2) / 2

    return (xCoordinate, yCoordinate)


def estimateCross(result, cap, frame, id_cross) -> CrossInfo:
    boxes = result.boxes
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
        if contours == None or contours == ():
            print("No contours found for cross")
            return None
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

def score_point(p, ideal_x, ideal_y, weight_x=1.0, weight_y=1.0):
    # Lower score is better (closer to corner)
    return weight_x * abs(p[0] - ideal_x) + weight_y * abs(p[1] - ideal_y)


def estimatePlayArea(result, cap, frame) -> list[np.ndarray]:
    h, w = cap.shape[:2]
    cx, cy = w // 2, h // 2

    # Red pixel mask
    b, g, r = cap[:, :, 0], cap[:, :, 1], cap[:, :, 2]
    red_mask = ((r > 115) & (g < r / 1.8) & (b < r / 1.8)).astype(np.uint8) * 255
    red_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)

    #cv2.imshow("Red channel", cv2.resize(red_mask, (1280, 720)))

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found.")
        return None

    points = np.vstack(contours).squeeze()
    if points.ndim != 2 or points.shape[1] != 2:
        print("Invalid points shape.")
        return None

    # Scoring helper (weights prioritize vertical bias for top corners)
    def find_best(points, ideal_x, ideal_y, weight_x=1.0, weight_y=2.0):
        scores = [weight_x * abs(p[0] - ideal_x) + weight_y * abs(p[1] - ideal_y) for p in points]
        return points[np.argmin(scores)]

    # Pick 8 key edge points (2 per corner)
    tl_top     = find_best(points, 0, 0)
    tl_left    = find_best(points, 0, 0, weight_x=2.0, weight_y=1.0)

    tr_top     = find_best(points, w, 0)
    tr_right   = find_best(points, w, 0, weight_x=2.0, weight_y=1.0)

    br_bottom  = find_best(points, w, h)
    br_right   = find_best(points, w, h, weight_x=2.0, weight_y=1.0)

    bl_bottom  = find_best(points, 0, h)
    bl_left    = find_best(points, 0, h, weight_x=2.0, weight_y=1.0)

    extremities = [tl_top, tl_left, tr_top, tr_right, br_bottom, br_right, bl_bottom, bl_left]
    for pt in extremities:
        if pt is not None:
            cv2.circle(frame, tuple(pt), 4, (0, 255, 255), -1)

    if any(p is None for p in extremities):
        print("Missing extremity points")
        return None

    # Your updated line intersection logic
    pairs = [
        (tl_top, bl_bottom, tl_left, tr_right),
        (tr_top, br_bottom, tr_right, tl_left),
        (br_bottom, tr_top, br_right, bl_left),
        (bl_bottom, tl_top, bl_left, br_right),
    ]

    def intersection_from_2pts_np(p1, p2, p3, p4):
        p1, p2, p3, p4 = map(np.asarray, [p1, p2, p3, p4])
        a1 = p2 - p1
        a2 = p4 - p3
        A = np.array([a1, -a2]).T
        b = p3 - p1
        if np.linalg.matrix_rank(A) < 2:
            return None
        t = np.linalg.solve(A, b)
        return p1 + t[0] * a1

    corners = []
    for p1, p2, p3, p4 in pairs:
        pt = intersection_from_2pts_np(p1, p2, p3, p4)
        if pt is not None:
            corners.append(pt)
            cv2.circle(frame, tuple(np.int32(pt)), 10, (0, 255, 255), -1)
        else:
            print("Failed to compute intersection.")
            return None

    return corners



def np_int(t):
    return np.round(t).astype(int)

def estimatePlayAreaIntermediate(result, playarea, frame, margin):
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

def edge_normal(p1, p2):
    """Calculates the normal vector to the edge from p1 to p2, on the right side."""
    normal = np.array((p1[1] - p2[1], p2[0] - p1[0]), float)
    return normal / np.linalg.norm(normal)

def offset_vertex(p1, p2, p3, distance):
    """Offsets the vertex p1 by distance inwards. p2 is the adjacent vertex in the clockwise direction, and opposite for p3."""
    # The vectors from the vertex to the adjacent vertices, rotated by 90°
    v1 = edge_normal(p1, p2)
    v2 = edge_normal(p3, p1)
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