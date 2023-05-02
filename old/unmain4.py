# %%
from multiprocessing.spawn import import_main_path
import cv2
import numpy as np
import os
# import cannyED
from tqdm import tqdm
import time

# %%
def crop (in_img):
    # import cv2
    zmensene = False #!!! můžou fungovat lépe aneb když programátor nepřizná, že mu to prostě nefunguje
    if zmensene == True:
        cropped = in_img
        # cropped = cv2.resize(source, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        # cropped = cropped[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        # cropped = source[1480 : 8000, 410 : right]        #crop velkých, originálů
        cropped = in_img[1480 : 8000, 410 : 10200]        #crop velkých, originálů

        # zamalování loga UP
        cropped = cv2.rectangle(cropped, (8800, 0), (10290, 1409), (0, 0, 0), -1)
        cropped = cv2.rectangle(cropped, (0, 0), (1409, 1409), (0, 0, 0), -1)
    # cropped = source

    return cropped

# %%
def thresholdit (source, times):
    sum = 0
    h, w = source.shape[:2]

    for a in source:
        for b in a:
            sum = sum + b
    avg = sum / (h*w)

    much = avg * times

    _, th = cv2.threshold(source, much, 255, cv2.THRESH_BINARY)
    return th

# %%
def bake(bake_img, hard = None):
    # global bake_img
    if hard == True:
        cv2.imwrite("temp.png", bake_img)
        return cv2.imread("temp.png")
    else:
        return bake_img.astype(np.uint8)

# %%
show_imgs = False
os.system('cls')

# %%
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

# %% [markdown]
# # Další by mělo být v for inputs
# ale protože jupyter(a rozhodně ne že já ho neumím): neloopuju se, ale jedu jenom 1 obrázek

# %%
# actual_img = "2022_02_23_12_45_14"
for actual_img in tqdm(inputs):
    # %%
    # načte BW obrázek
    bw = cv2.imread("in/{}.jpg".format(actual_img), 0).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    # bw = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("debug/1.BW/{}.png".format(actual_img), bw)

    if show_imgs == True:
        frame = cv2.resize(bw, (979, 652))
        cv2.imshow('win', frame)
        cv2.waitKey(200)

    # %%
    # also load original image to write on later IT IS RGB
    original = cv2.imread("in/{}.jpg".format(actual_img))
    original = crop(original)

    # %%
    cropped = crop (bw)
    cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), cropped)

    if show_imgs == True:
        frame = cv2.resize(cropped, (979, 652))
        cv2.imshow('win', frame)
        cv2.waitKey(200)


    # %%
    # threshold
    threshed = thresholdit (cropped, 10)
    # 10 je možno vyladit
    cv2.imwrite("debug/3.thresh/{}.png".format(actual_img), threshed)

    if show_imgs == True:
        frame = cv2.resize(threshed, (979, 652))
        cv2.imshow('win', frame)
        cv2.waitKey(200)

    # %%
    threshed = thresholdit(cropped, 10)
    # threshed = bake(threshed, True)
    threshed = np.uint8(threshed)

    # %%
    raw_cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # %%
    def filtrAreaDumb(raw_cnts, thresh):
        out = []
        for cnt in raw_cnts[0]:
            # print(cnt)
            area = cv2.contourArea(cnt)
            if area > thresh:
                out.append(cnt)
        # print(out)
        return out

    # %%
    def filtrAreaSmart (cnts):
        thresh = 10
        numbr = 100
        while True:
            # temp = 280
            temp = filtrAreaDumb(cnts, thresh)
            thresh += 10
            if len(temp) < numbr:
                return temp

    # %%
    # area_smart_cnts = filtrAreaSmart(raw_cnts)
    area_cnts = filtrAreaSmart(raw_cnts)
    # area_cnts = filtrAreaDumb(area_smart_cnts, 1500)
    # img_filtr = np.copy(original)
    # img_filtr = cv2.drawContours(img_filtr, area_cnts, -1, (255, 255, 255), 3)
    # cv2.imwrite("debug/4.CNTs/{}.png".format(actual_img), img_filtr)
    # # print(area_cnts)

    # %%
    def filtrTvar(inCNS, img):
    # filtrovat budu za pomoci větší strana/menší, pokud výsledek bude větší jak 3, tak je to kořen, jinak ne
        out_el = []
        out_cnt = []
        out_box = []


        # print("debug is fun")
        # for cnt in inCNS:
        for cnt in tqdm(inCNS):
            elps = cv2.fitEllipse(cnt)
            elimg = np.copy(img) * 0  # creating a blank to draw lines on
            # print(elps)
            
            stra = elps [1][0]
            strb = elps [1][1]

            div = strb // stra

            # nastaví šířku 1 => čáry
            
            box = cv2.boxPoints(tuple(elps)) 
            box = np.int0(box) #Convert into integer values

            # print(stra)
            # print(strb)
            # print()

            # teď budu dělit. protože čísla vycházejí stra menší než strb, tak nemusím dělat nějak velký ošklivý check, co by porovnal ty dvě čísla, a dělil větší menším.
            if div < 1:
                print("error filtrace kontur, potřebuješ přidat check na řádku 99, viz main2.py")
            # tady threshold
            if div > 1.8:
                # print(div)
                out_el.append(elps)
                out_cnt.append(cnt)
                out_box.append(box)

                # elimg = cv2.drawContours(elimg,[box],0,(255,255,255),20)
                box = []
        # print(out_el)
        # print(out_cnt)
        # print(out_box)
        return out_el, out_cnt, out_box

    # %%
    tvar_el, tvar_cnt, tvar_box = filtrTvar(area_cnts, original)
    # print(len(tvar_area_cnts)

    # %%
    # print(tvar_cnt)
    # tvar_cnt = filtrAreaDumb(tvar_cnt, 10)

    # %% [markdown]
    # tvar_el = středy čtverců
    # tvar_cnt = kontury 
    # tvar_box = čtverec

    # %%
    img_filtr = np.copy(original)
    # for a in tvar_cnt:
    #     for b in a:
    #         # print(b)
    #         y = b[0][0]
    #         x = b[0][1]
    #         img_filtr [x] [y] = 255, 255, 255

    #     # print(img_filtr)
    #     os.system('cls')
    img_filtr = cv2.drawContours(img_filtr, tvar_cnt, -1, (255, 255, 255), 3)
    img_filtr = cv2.drawContours(img_filtr, tvar_box, -1, (0, 0, 255), 3)

    cv2.imwrite("debug/4.CNTs/{}.png".format(actual_img), img_filtr)

    # %%


    # %%



