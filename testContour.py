import cv2
import numpy as np
from detectiveLine import *
import time
from MotorControl import *


def MiddlePoint(edge,height,width):
    start_height = height - 10
    middleWidth = width / 2
    point = []
    while start_height > 0:
        right = 0
        left = 0
        countl = 0
        countr=0
        i=0
        for i in range(width -1):
            if edge[start_height][i]:
                if i < middleWidth :
                    left = left +(i)
                    countl+=1
                else:
                    right=right+i
                    countr+=1
        
        if countr!=0:
            right = right/countr
            cv2.circle(edge, (int(right), start_height), 2, (255,0,0), -1)
        if countl!=0:
            left = left/countl
            cv2.circle(edge, (int(left), start_height), 2, (255,0,0), -1)
        middle = 0
        if left and right:
            middle = (left + right)/2
        elif left:
            middle = (width - (middleWidth - left) + left)/2
        elif right:
            middle = (( right - middleWidth) + right)/2
        if middle:
            point.append([middle,start_height])
            cv2.circle(edge, (int(middle), start_height), 2, (255,0,0), -1)
        start_height = start_height - 50
        
    return point[0]
    
                
Speed = 50
MidWidth = 320
image = cv2.imread("trai1.jpg")
base = 5
while True:
    canny = CannyEdge(image)
    canny = region_of_interest(canny)
    mid = MiddlePoint(canny,canny.shape[0],canny.shape[1])
    if mid is not None:
        if GetSpeed() == 0: # if is stopped but finds a line
            BaseSpeed(Speed)
        print(int((mid-320)/base))
        Direction(int((mid - 320)/base))