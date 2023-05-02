
import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt

# First, get the gray image and process GaussianBlur.

# img = cv2.imread('in/2022_02_23_12_48_53.jpg')

# cropped = img[2130:7850, 870:11000]
# cv2.imwrite("result_cropped.jpg", cropped)
cropped = cv2.imread('result_cropped.jpg')

# #img = cv2.imread('src.png')
# gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
# cv2.imwrite("result_gray.jpg", gray)

# contrast_value = 4
# brightness_value = 0
# contrast_gray = cv2.addWeighted(gray, contrast_value, gray, 0, brightness_value)
# cv2.imwrite("result_contrast_gray.jpg", contrast_gray)

# kernel_size = 3
# blur_gray = cv2.GaussianBlur(contrast_gray, (kernel_size, kernel_size), 0)
# cv2.imwrite("result_blur_gray.jpg", blur_gray)

# # Second, process edge detection use Canny.

# low_threshold = 50
# high_threshold = 150
# edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
# cv2.imwrite("result_edges.jpg", edges)

edges = cv2.imread('result_edges.jpg', 0)
# print(edges)

# Then, use HoughLinesP to get the lines. You can adjust the parameters for better performance.

rho = 1  # distance resolution in pixels of the Hough grid
theta = 5 * np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 200  # minimum number of pixels making up a line
max_line_gap = 200  # maximum gap in pixels between connectable line segments
line_image = np.copy(cropped) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

# Finally, draw the lines on your srcImage.

# Draw the lines on the  image
lines_edges = cv2.addWeighted(cropped, 0.8, line_image, 1, 0)

cv2.imwrite("result_lines_edges.jpg", lines_edges)
#cv2.imshow("res", lines_edges)
# cv2.waitKey(0)