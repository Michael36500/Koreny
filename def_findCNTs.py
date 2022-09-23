import cv2
import numpy
import def_bake as bake

def findCNTs(actual_img):
    source = cv2.imread("debug/3.thresh/{}.png".format(actual_img), 0)
    # source = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # print(source)
    # bw = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # bake.bake(source)
    cnts = cv2.findContours(source, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    # write = open("cnts.txt", "w")
    # write.write(str(cnts))
    # print(cnts)

    return cnts
