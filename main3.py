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
inputs = os.listdir("in/")
# vynechávám img_num, protože ho nepotřebuji

for actual_img in tqdm(inputs):

    gray = cv2.imread("in/{}".format(actual_img), 0).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    # gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("debug/1.BW/{}".format(actual_img), gray)

    cropped = crop.crop (gray)
    cv2.imwrite("debug/2.cropped/{}".format(actual_img), cropped)

    # 10 je možno vyladit
    threshed = thresh.th(cropped, 10)
    cv2.imwrite("debug/3.thresh/{}".format(actual_img), threshed)
    
    
    
    
    
    
    
    
    break