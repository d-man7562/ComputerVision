import numpy as np
import cv2 as cv
import random
# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN  or event == cv.EVENT_LBUTTONUP or event == cv.EVENT_MOUSEMOVE:
        r1  = random.randint(0,255) 
        r2 = random.randint(0,255)
        r3 = random.randint(0,255)
        cv.circle(img,(x,y),100,(r1,r2,r3),-1)
 
# Create a black image, a window and bind the function to window
img = np.zeros((480,480,3), np.uint8)
cv.namedWindow('I LOVE COLORS!!!!  :DDDD')
cv.setMouseCallback('I LOVE COLORS!!!!  :DDDD',draw_circle)
 
while(1):
    cv.imshow('I LOVE COLORS!!!!  :DDDD',img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()