import cv2
import numpy as np

def contour_centroid(contour):
    """ 
    find the centroid (center of mass) of contour, source https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
​
    contour: list contour
    return: centroid coordinate x and y
    """
    
    M = cv2.moments(contour_to_cv2arr(contour))
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    return cX, cY
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin. source https://stackoverflow.com/a/34374437
​
    origin: centroid of contour (ox,oy)
    point: the point to rotate
    angle: radians angle
​
    return: rotated point coordinate x, y
    """
    ox, oy = origin
    px, py = point
    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return int(qx), int(qy)
def rotate_contour(contour, angle):
    ''' 
    rotate every point on the contour counterclockwise
    
    contour: list contour
    angle: radians
​
    return: list contour after rotation
    '''
    cx, cy = contour_centroid(contour)
    return [rotate((cx, cy), (x, y), angle) for x, y in contour]
def recenter_contour(contour, new_center):
    ''' 
    translate every point on contour and reset its centroid
​
    contour: list contour
    new_center: the destination centroid point
​
    return: list contour after translation
    '''
    nx, ny = new_center
    cx, cy = contour_centroid(contour)
    return [(x - cx + nx, y - cy + ny) for x, y in contour]

def scale_contour(contour,scaleFactor):
    cx,cy=contour_centroid(contour)
    cnt=contour_to_cv2arr(contour)
    cnt_norm=cnt-[cx,cy]
    cnt_scaled=cnt_norm*scaleFactor
    cnt_scaled=cnt_scaled+[cx,cy]
    cnt_scaled=cnt_scaled.astype(np.int32)
    return contour_from_cv2arr(cnt_scaled)

def contour_to_cv2arr(contour):
    '''
    convert list contour to cv2 ndarray, which can be applied into cv2 functions directly
    
    contour: list contour
    return: cv2 ndarray, dim: (|n points|, 1, 2)
    '''
    return np.array(contour)[:, None, :]
def contour_from_cv2arr(contour_arr):
    '''
    convert cv2 ndarray to list contour
​
    contour_arr: cv2 ndarray, dim: (|n points|, 1, 2)
    return: list contour
    '''
    return contour_arr[:, 0, :].tolist()
