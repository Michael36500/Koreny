import cv2
import os
from tqdm import tqdm 

infl = os.listdir("in")
outfl = os.listdir("out")

cv2.namedWindow("ini", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("outi", cv2.WINDOW_AUTOSIZE)

fil = 0

for fil in tqdm(range(len(infl))):
# for fil in range(len(infl)):
    # print(infl[fil])



    ini = cv2.imread("in/{}".format(infl[fil]))
    outi = cv2.imread("out/{}".format(outfl[fil]))
    # ini = cv2.imread('2022_02_23_12_45_14.jpg')
    # outi = cv2.imread("{}".format(outfl[fil]))
    # ini = cv2.imread("in\\2022_02_23_12_51_18.jpg")
    # outi = cv2.imread("out\\2022_02_23_12_51_18.jpg")


    ini = cv2.resize(ini, (800, 600))
    ini = ini[100 : 540, 70 : 700]

    cv2.imshow('ini', ini)
    cv2.imshow('outi', outi)
    cv2.waitKey(0)

    # print(fil)

    

