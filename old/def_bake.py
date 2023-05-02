import cv2
import numpy as np


# bake je funukce, co True) uloží a znovu otevře obrázek (pomalé) a False) přepočítá obrázek
def bake(bake_img, hard = None):
    # global bake_img
    if hard == True:
        cv2.imwrite("temp.png", bake_img)
        return cv2.imread("temp.png")
    else:
        return bake_img.astype(np.uint8)
