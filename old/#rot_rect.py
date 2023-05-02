import cv2 
import numpy as np
#cv2 is used for OpenCV library

image = cv2.imread("full_black.png")
#imread is use to read an image from a location

rot_rectangle = ((320, 200), (300, 150), 0)
#rot_rectangle = ((STŘED ROTACE), (šířka, výška obdélníku), rotace po směru ručiček)

box = cv2.boxPoints(rot_rectangle) 
box = np.int0(box) #Convert into integer values

rectangle = cv2.drawContours(image,[box],0,(0,0,255),1)

cv2.imshow("Rotated Rectangle",rectangle)

cv2.waitKey(0)
cv2.destroyAllWindows()