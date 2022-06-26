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

# import kontur funukce
import def_findCNTs as findCNTs

# smart threshold
import def_threshold as thresh

# filtrace kontur pomocí plochy
import def_filtrArea as filtrArea

# nakreslí na 1. parametr pixelly/contours z 2. parametru
# import def_drawCNTs as drawCNTs

# importuje filtr tvary
import def_filtrTvar as filtrTvar

show_imgs = False
os.system('cls')

# najde všechny soubory v IN složce, aby se mohl loopnout
inputs_jpg = os.listdir("in/")
inputs = []
for a in inputs_jpg:
    l = len(a)
    short = a[:l - 4]
    inputs.append(short)
# vynechávám img_num, protože ho nepotřebuji
if show_imgs == True:
    cv2.namedWindow("win", cv2.WINDOW_AUTOSIZE)

# for actual_img in tqdm(inputs):
for actual_img in inputs:
    print(actual_img)
    # load
    bw = cv2.imread("in/{}.jpg".format(actual_img), 0).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    # bw = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("debug/1.BW/{}.png".format(actual_img), bw)

    # also load original image to write on later
    original = cv2.imread("in/{}.jpg".format(actual_img))
    original = crop.crop(original)

    # print("BW")
    if show_imgs == True:
        frame = cv2.resize(bw, (979, 652))
        cv2.imshow('win', frame)
        cv2.waitKey(200)
    

    # criop
    cropped = crop.crop (bw)
    cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), cropped)
    
    # print("cropped")
    if show_imgs == True:
        frame = cv2.resize(cropped, (979, 652))
        cv2.imshow('win', frame)
        cv2.waitKey(200)

    # threshold
    threshed = thresh.th(cropped, 10)
    # 10 je možno vyladit
    cv2.imwrite("debug/3.thresh/{}.png".format(actual_img), threshed)

    # print("threshed")
    if show_imgs == True:
        frame = cv2.resize(threshed, (979, 652))
        cv2.imshow('win', frame)
        cv2.waitKey(200)

    # raw CNTs
        # musim bejknout
    # threshed = bake.bake(threshed, False)
    # print(threshed)
    # raw_cnts = findCNTs.findCNTs(actual_img)
    # source = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # print(source)
    # bw = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # bake.bake(source)
    raw_cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    # write = open("cnts.txt", "w")
    # write.write(str(cnts))
    # print(cnts)


    # print(raw_cnts)
    
    # area  
    print(raw_cnts[2])
    area_cnts = filtrArea.filtrArea(raw_cnts)  

    # cv2.drawContours( area_cnts, -1, (255, 255, 255), 3)
    area_img = cv2.drawContours(original, area_cnts, -1, (255, 255,255), 3)

    cv2.imwrite("debug/4.CNTs/{}.png".format(actual_img), area_img)

    # if show_imgs == True: x   
    #     frame = cv2.resize((area_img), (979, 652))
    #     cv2.imshow('win', frame)
    #     cv2.waitKey(200)
    # # tvar filtr
    # tvar_area_cnts = filtrTvar.filtrTvar(area_cnts, threshed)

    # # chybí excentricitou

    # cnt_cropped = drawCNTs.drawCNTs(cropped, area_cnts)
    # # print(cnts)






    
    break