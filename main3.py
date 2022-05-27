import imghdr
from multiprocessing.spawn import import_main_path
import cv2
import numpy as np
import os
import cannyED
from tqdm import tqdm

# bake je funukce, co True) uloží a znovu otevře obrázek (pomalé) a False) přepočítá obrázek
def bake(bake_img, hard = None):
    # global bake_img
    if hard == True:
        cv2.imwrite("temp.png", bake_img)
        return cv2.imread("temp.png")
    else:
        return bake_img.astype(np.uint8)

# najde všechny soubory v IN složce, aby se mohl loopnout
inputs = os.listdir("in")
# vynechávám img_num, protože ho nepotřebuji

for actual_img