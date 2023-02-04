
# importy

# try:
#     import numpy as np # dá se naimportovat i cupy pro nvidia GPU
# except:
import cv2
import numpy as np
import numpy
import os
from matplotlib import pyplot as plt
from tqdm import tqdm
import time


# příprava

# najde všechny soubory v IN složce, aby se mohl loopnout
inputs_jpg = os.listdir("in/")
inputs = []

# vynechám ty s X
for a in inputs_jpg:
    if a[0] == "X":
        continue
    l = len(a)
    # odstraním .jpg
    short = a[:l - 4]
    inputs.append(short)

# předpřipravím si loop
for actual_img in tqdm(inputs):
    save_debug = False


    # loadnu originální obrázek + zamaluju ligi

    # 1. načte BW obrázek
    orig_bw = cv2.imread("in/{}.jpg".format(actual_img), 0) # 0 protože chci černobílý obrázek (pro krok úprava)

    # zamalování loga UP
    orig_bw = cv2.rectangle(orig_bw, (10000, 1211), (11800, 2100), (0), -1)
    orig_bw = cv2.rectangle(orig_bw, (0, 1100), (1200, 2800), (0), -1)

    # save
    if save_debug:
        cv2.imwrite("debug/1.BW/{}.png".format(actual_img), orig_bw)


    # crop

    # ZLEVA A ZPRAVA 
    # sečtu sloupce zvrchu dolů pro hledání ořezu zleva a zprava
    suma_sloupec = np.array([])

    for sloupec in range(len(orig_bw[0])):
        suma_sloupec = np.append(suma_sloupec, np.sum(orig_bw[:, sloupec]))

    # hledám crop zleva a zprava
    med = np.median(suma_sloupec) # vytvořím proměnnou s mediánem všech sloupců
    med *= 1.25 # mírně posunu nahoru
    medlist = np.where(suma_sloupec < med)[0] # 1D list s číslem sloupců, co jsou pod "med" číslem
    ln = len(suma_sloupec) # získám šířku obrázku, IDK
    lnn = ln // 2

    h, w = orig_bw.shape[:2]

    # vezmu první a poslední hodnotu v medlistu 
    clft = medlist[0]
    crgh = medlist[-1]

    # pro pravý okraj speciálně dělám "pokročilejší" crop
    # jinými slovy, najdu místo, kde je pár dalších směrem k centru pod mediánem
    for x in range(0, w, 10):
        tmp = numpy.array([])
        for y in range(w//20):
            if suma_sloupec[-y - x] <= med:
                tmp = numpy.append(tmp, y)
        if len(tmp) > w // 20 // 1.5:
            crgh = w - x
            break
            



    # ZVRCHU A ZESPODU #
    # hledám crop zvrchu a zespodu
    suma_radek = np.array([])

    # sčítám řádky
    for radek in range(len(orig_bw)):
        suma_radek = np.append(suma_radek, np.sum(orig_bw[radek]))

    # hledám crop zvrchu a zespodu
    med = np.median(suma_radek) # proměnná s mediánem ze všech řádků
    med *= 1.25 # mírně posunu nahoru
    medlist = np.where(suma_radek < med)[0]# 1D list s číslem sloupců, co jsou pod "med" číslem

    # beru první a poslední hodnotu v medlist (list s indexy)
    ctop = medlist[0]
    cbot = medlist[-1]

    # cropne obrázky podle předchozích kroků
    margin = 0
    crp = orig_bw[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]
    orig_bw = crp
    # save
    if save_debug:
        cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), crp)


    # OTSU

    # celkový nápad je, že vezmu 4 čtverce (mírně nahoře, mírně dolů, mírně doleva, mírně doprava od zhruba začátku kořenu) a u každého 4 velikosti (200x200, 400x400, 800x800, 1600x1600)

    # definuji funkci, která vezme obrázek a vrátí najitý threshold
    def find_otsu(img):
        threshold, _ = cv2.threshold(img, 255, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   
        return threshold
    # malá funukce na otestování, jestli čtverec nezasahuje mimo obrázek, popř korekce
    def check_otsu_crop(value, thresh):
        if thresh != 0:
            if value >= thresh:
                value = thresh
            return value
        elif thresh == 0:
            if value <= thresh:
                value = thresh
            return value
        else:
            print("you're fucked up")

    # hlavní část loopu, která se mnohokrát opakovala, tak proto je ve funkci
    def najdi_otsu_thresh_ctverce(x, y, strana, ukaz= False):
        # x a y beru jako zlomky
        x = int(w * x)
        y = int(h * y)

        # hodnoty pro crop
        hst = (y - strana) # hst je pro height start
        hen = (y + strana) # hen je pro height end
        wst = (x - strana) # wst je pro width start
        wen = (x + strana) # wen je pro width end

        # checku jestli nejdu ven z obrázku
        hst = check_otsu_crop(hst, 0)
        hen = check_otsu_crop(hen, h)
        wst = check_otsu_crop(wst, 0)
        wen = check_otsu_crop(wen, w)
        # print(hst, hen, wst, wen)
        
        otsu_crp = crp[hst : hen, wst : wen]
        if ukaz:
            plt.imshow(otsu_crp)
        return find_otsu(otsu_crp)

    h, w = crp.shape[:2]
    otsus = []

    pole_ctvercu = [
        [0.7, 0.5, 2000],
        [0.7, 0.5, 1000],
        [0.7, 0.6, 2000],
        [0.7, 0.6, 1000],
        [0.7, 0.4, 2000],
        [0.7, 0.4, 1000],
        [0.6, 0.5, 2000],
        [0.6, 0.5, 1000]
    ]


    for ctverec in pole_ctvercu:
        otsus.append(najdi_otsu_thresh_ctverce(ctverec[0], ctverec[1], ctverec[2], ukaz=False))
    # otsus je pole najitých hodnot otsuem

    # APLIKACE THRESHOLDU
    otsus = np.array(otsus)
    # zjistím chytrej průměr
    ln = len(otsus)
    top_x_cisel = 0.6
    otsus_sort = np.sort(otsus)[int(top_x_cisel*ln):ln]
    avg = np.median(otsus_sort) * 0.8
    # print(otsus)
    # print(avg)
    _, th_otsu = cv2.threshold(crp, avg, 255, cv2.THRESH_BINARY)

    th_otsu = np.uint8(th_otsu)


    # KONTURY + SAVE
    raw_cnts = cv2.findContours(th_otsu, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    if True:
        cv2.imwrite("debug/3.Otsu/{}.png".format(actual_img), cv2.drawContours(orig_bw, raw_cnts, -1, (255, 0, 255), 5))


    # KRAJE
    okraj = w * 0.0280373832
    height, width = th_otsu.shape[:2]
    okraje = [okraj, okraj, height - okraj, width - okraj]
    nekraj_cnts = []
    def is_inside(cnt):
        global height, width
        x,y,w,h = cv2.boundingRect(cnt)
        if x < okraj or y < okraj or x + w > width - okraj or y + h > height  - okraj:
            return False
        else:
            return True
        
    for cnt in raw_cnts:
        if is_inside(cnt):
            nekraj_cnts.append(cnt)

    if save_debug:
        cv2.imwrite("debug/4.okraje/{}.png".format(actual_img), cv2.drawContours(orig_bw, nekraj_cnts, -1, (255, 0, 0), 10))
        # break
    # print(nekraj_cnts)


    # super malý + saVe
    thresh = 10
    smaly_nekraj_cnts = []

    for cnt in nekraj_cnts:
        if cv2.contourArea(cnt) > thresh:
            smaly_nekraj_cnts.append(cnt)


    if True:
        save = cv2.drawContours(orig_bw, smaly_nekraj_cnts, -1, (255, 0, 0), -1)
        cv2.imwrite("debug/5.smaly/{}.png".format(actual_img), save)





