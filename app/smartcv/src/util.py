from __future__ import division, print_function, absolute_import

from math import sqrt, pow

def get_midpoint(bounding_box):
    x, y, w, h = bounding_box
    w = int(w/2)
    h = int(h/2)
    return (int(x) + int(w), int(y) + int(h))

def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    d1 = pow(x2-x1, 2)
    d2 = pow(y2-y1, 2)
    distance = sqrt(d1 + d2)
    return distance

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
    
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
	yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] + 1) * (boxA[3] + 1)
	boxBArea = (boxB[2] + 1) * (boxB[3] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

def _calculate_hypotenuse(base, perpendicular):
    return int(sqrt((base*base) + (perpendicular*perpendicular)))

def displacement(frame1, frame2):
    # assume width and height of two frames to be the same
    # if frame1[2] != frame2[2] or frame1[3] != frame2[3]:
    #     raise ValueError('Width and/or height of the two frames do not match.')
    frame1_mid = get_midpoint(frame1)
    frame2_mid = get_midpoint(frame2)
    f1x2 = frame1_mid[0]
    f1y2 = frame1_mid[1]
    f2x2 = frame2_mid[0]
    f2y2 = frame2_mid[1]
    # f1x2 = frame1[0] + frame1[2]
    # f1y2 = frame1[1] + frame1[3]
    # f2x2 = frame2[0] + frame2[2]
    # f2y2 = frame2[1] + frame2[3]
    disp_x = f2x2 - f1x2
    disp_y = f2y2 - f1y2
    disp = 0
    if disp_x == 0 and disp_y == 0:
        disp = 0
    elif disp_x == 0:
        disp = abs(disp_y)
    elif disp_y == 0:
        disp = abs(disp_x)
    else:
        disp = _calculate_hypotenuse(abs(disp_x), abs(disp_y))

    LR = 0
    UD = 0
    direction = 'None'
    if disp_y > 0:
        direction = 'South'
        UD = 0.01
    elif disp_y < 0:
        direction = 'North'
        UD = -0.01
    else:
        direction = 'None'
        UD = 0

    if disp_x > 0:
        LR = 0.01
        if direction == 'None':
            direction = 'East'
        else:
            direction += '-East'
    elif disp_x < 0:
        LR = -0.01
        if direction == 'None':
            direction = 'West'
        else:
            direction += '-West'
    return disp, direction, LR, UD
