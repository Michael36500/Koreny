import cv2
from cv2 import waitKey
import numpy

def th (source, times):
    sum = 0
    h, w = source.shape[:2]

    for a in source:
        for b in a:
            sum = sum + b
    avg = sum / (h*w)

    much = avg * times

    _, th = cv2.threshold(source, much, 255, cv2.THRESH_BINARY)
    return th



# img = cv2.imread("debug/2.cropped/2022_02_23_12_45_14.png", 0)
# cv2.namedWindow("opencv", cv2.WINDOW_AUTOSIZE)

# img = cv2.resize(img, (800, 600))

# # for a in range(50):
#     # print(a)
# thr = th(img, 10)
# cv2.imshow("opencv", thr)
# cv2.waitKey(0)


