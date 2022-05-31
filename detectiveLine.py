import cv2
import numpy as np
import math


def make_points(image, line_parameters):
    height, width, _ = image.shape
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = 0.1, 0
    y1 = int(image.shape[0])
    y2 = int(y1*3/5)
    if slope == 0:
        slope = 0.01
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    height, width, _ = image.shape
    if lines is None:
        return None
    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        slope, intercept = math.inf, 0
        if x2-x1 == 0:
            continue
        else:
            slope = (y2-y1)/(x2-x1)
        intercept = y1 - slope * x1
        if slope < 0:
            if x1 < left_region_boundary and x2 < left_region_boundary:
                left_fit.append((slope, intercept))
        else:
            if x1 > right_region_boundary and x2 > right_region_boundary:
                right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)
    return np.array((left_line, right_line))


def CannyEdge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    cannyImage = cv2.Canny(blur, 200, 400)
    return cannyImage


def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    triangle = np.array(
        [[0, int(height*0.2)], [0, height], [width, int(height)],[width,int(height*0.2)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [triangle], 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def display_lines(image, lines):
    theta = []
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            theta = math.atan2((y2-y1),(x2-x1))
    return line_image, theta

