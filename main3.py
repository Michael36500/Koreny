import imghdr
from multiprocessing.spawn import import_main_path
import cv2
import numpy as np
import os
# import cannyED
from tqdm import tqdm

# bake je funukce, co True) uloží a znovu otevře obrázek (pomalé) a False) přepočítá obrázek
import def_bake as bake

# smart crop
import def_crop as crop

# smart threshold
import def_threshold as thresh


# najde všechny soubory v IN složce, aby se mohl loopnout
inputs_jpg = os.listdir("in/")
inputs = []
for a in inputs_jpg:
    l = len(a)
    short = a[:l - 4]
    inputs.append(short)
# vynechávám img_num, protože ho nepotřebuji

for actual_img in tqdm(inputs):

    gray = cv2.imread("in/{}.jpg".format(actual_img), 0).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    # gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("debug/1.BW/{}.png".format(actual_img), gray)
    # print("1.BW")

    cropped = crop.crop (gray)
    cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), cropped)
    # print("2.cropped")

    # 10 je možno vyladit
    threshed = thresh.th(cropped, 10)
    cv2.imwrite("debug/3.thresh/{}.png".format(actual_img), threshed)
    # print("3.thresh")
    
    
    
    
    
    
    
    # break