
# importy
import cv2
import cupy as np
import os
from matplotlib import pyplot as plt
from tqdm import tqdm
import time

# najde všechny soubory v IN složce, aby se mohl loopnout
inputs_jpg = os.listdir("in/")
inputs = []
for a in inputs_jpg:
    if a[0] == "X":
        continue
    l = len(a)
    short = a[:l - 4]
    inputs.append(short)


# příprava loopu
for actual_img in tqdm(inputs):

    # načte BW obrázek
    bw = cv2.imread("in/{}.jpg".format(actual_img), 0) # 0 protože chci černobílý obrázek (pro krok úprava)

    # zamalování loga UP
    bw = cv2.rectangle(bw, (10000, 1211), (11800, 2100), (0), -1)
    bw = cv2.rectangle(bw, (0, 1100), (1050, 2800), (0), -1)

    h, w = bw.shape[:2]
    resize_w = 400
    ratio = resize_w / w
    dim = (resize_w, int(h * ratio))
    bw = cv2.resize(bw, dim)

    # save
    cv2.imwrite("debug/1.BW/{}.png".format(actual_img), bw)



