
# importy
###########
# importy #
###########

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
############
# příprava #
############

# najde všechny soubory v IN složce, aby se mohl loopnout
inputs_jpg = os.listdir("in/")
inputs = []
for a in inputs_jpg:
    if a[0] == "X":
        continue
    l = len(a)
    short = a[:l - 4]
    inputs.append(short)

# předpřipravím si loop
for actual_img in inputs:
    print(actual_img)
    print(inputs.index(actual_img))
    print()
    # actual_img = "2022_02_23_12_50_13"
    save_debug = False

    # loadnu obrázek
    ##################
    # loadnu obrázek #
    ##################

    # 1. načte BW obrázek
    bw = cv2.imread("in/{}.jpg".format(actual_img), 0) # 0 protože chci černobílý obrázek (pro krok úprava)

    # zamalování loga UP
    bw = cv2.rectangle(bw, (10000, 1211), (11800, 2100), (0), -1)
    bw = cv2.rectangle(bw, (0, 1100), (1200, 2800), (0), -1)

    # save
    if save_debug:
        cv2.imwrite("debug/1.BW/{}.png".format(actual_img), bw)

    # CROP
    ########
    # crop #
    ########
    # - může trvat trošku déle (v rozmezí sekund)

    # ZLEVA A ZPRAVA #


    #       |\---/|
    #       | o_o |
    #        \_^_/

    # sečtu sloupce zvrchu dolů pro hledání ořezu zleva a zprava
    suma_sloupec = np.array([])

    for sloupec in range(len(bw[0])):
        suma_sloupec = np.append(suma_sloupec, np.sum(bw[:, sloupec]))

    # plot
    # plt.plot(suma_sloupec.get())
    # plt.show()
    # hledám crop zleva a zprava
    med = np.median(suma_sloupec) # vytvořím proměnnou s mediánem všech sloupců
    med *= 1.25 # mírně posunu nahoru
    medlist = np.where(suma_sloupec < med)[0] # 1D list s číslem sloupců, co jsou pod "med" číslem
    ln = len(suma_sloupec) # získám šířku obrázku, IDK
    lnn = ln // 2


    h, w = bw.shape[:2]

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
    for radek in range(len(bw)):
        suma_radek = np.append(suma_radek, np.sum(bw[radek]))

    # plot
    # plt.plot(suma_radek.get())
    # plt.show()
    # hledám crop zvrchu a zespodu
    med = np.median(suma_radek) # proměnná s mediánem ze všech řádků
    med *= 1.25 # mírně posunu nahoru
    medlist = np.where(suma_radek < med)[0]# 1D list s číslem sloupců, co jsou pod "med" číslem

    # beru první a poslední hodnotu v medlist (list s indexy)
    ctop = medlist[0]
    cbot = medlist[-1]

    # vytisknul bych hodnoty cropu
    # print(ctop, cbot, clft, crgh)
    # cropne obrázky podle předchozích kroků
    margin = 0
    crp = bw[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]

    # save
    if save_debug:
        cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), crp)

    # LOAD ORIG img
    # načtu "orig"
    orig = cv2.imread("in/{}.jpg".format(actual_img)).astype("float64")

    orig = orig[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]

    # zamalování loga UP
    orig = cv2.rectangle(orig, (10000, 1211), (11800, 1930), (0), -1)
    orig = cv2.rectangle(orig, (0, 1100), (860, 2700), (0), -1)

    # OTSU
    ########
    # OTSU #
    ########

    # celkový nápad je, že vezmu 4 čtverce (mírně nahoře, mírně dolů, mírně doleva, mírně doprava od zhruba začátku kořenu) a u každého 4 velikosti (200x200, 400x400, 800x800, 1600x1600)

    # definuji funkci, která vezme obrázek a vrátí najitý threshold
    def find_otsu(img):
        threshold, _ = cv2.threshold(img, 255, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   
        return threshold

    # hlavní část loopu, která se mnohokrát opakovala, tak proto je ve funkci
    def najdi_otsu_thresh_ctverce():
        global base_h
        global base_w
        global check_otsu_crop
        global temp
        global start

        # hodnoty pro crop
        hst = (base_h - start) # hst je pro height start
        hen = (base_h + start) # hen je pro height end
        wst = (base_w - start) # wst je pro width start
        wen = (base_w + start) # wen je pro width end

        # checku jestli nejdu ven z obrázku
        hst = check_otsu_crop(hst, h)
        hen = check_otsu_crop(hen, h)
        wst = check_otsu_crop(wst, w)
        wen = check_otsu_crop(wen, w)

        # cropnu
        otsu_crp = crp[hst : hen, wst : wen]
        # appendnu najitý thresh do tempu
        temp.append(find_otsu(otsu_crp))
        # zvětším hledací čtverec
        start *= 2

    # malá funukce na otestování, jestli čtverec nezasahuje mimo obrázek, popř korekce
    def check_otsu_crop(value, thresh):
        if value >= thresh:
            value = thresh
        return value


    # deklarace listu kam budu appendovat najité thresholdy
    otsus = []

    # ______________________
    # první čtverec (napravo)

    temp = []   # dočasná proměnná kam budu zapisovat najíté threshe
    h, w = crp.shape[:2]
    base_h = int(h // 2) # height
    base_w = int(w * 6 // 7) # width
    start = 100 # je poloviční chtěné strany A u čtverce

    # loop co 4x zvětší a změěří čtverec
    for lp in range(4):
        najdi_otsu_thresh_ctverce()

    otsus.append(temp)


    # ______________________
    # druhý čtverec (nalevo)
    temp = []   # dočasná proměnná kam budu zapisovat najíté threshe
    h, w = crp.shape[:2]    
    base_h = int(h // 2) # height
    base_w = int(w * 5 // 7) # width
    start = 100 # je poloviční chtěné strany A u čtverce

    for lp in range(4):
        najdi_otsu_thresh_ctverce()
    otsus.append(temp)

    # ______________________
    # třetí čtverec (dole)
    temp = []
    h, w = crp.shape[:2]
    base_h = int(h * 3 // 4) # height
    base_w = int(w * 5.5 // 7) # width
    start = 100 # je poloviční

    for lp in range(4):
        najdi_otsu_thresh_ctverce()
    otsus.append(temp)

    # ______________________
    # čtvrtý čtverec(nahoře)
    temp = []
    h, w = crp.shape[:2]
    base_h = int(h * 1 // 4) # height
    base_w = int(w * 5.5 // 7) # width
    start = 100 # je poloviční

    for lp in range(4):
        najdi_otsu_thresh_ctverce()
    otsus.append(temp)

    # aplikace thresholdu
    otsus = np.array(otsus)
    otsus.max()

    # APLIKACE THRESHOLDU
    otsus = np.array(otsus)
    otsus.max()

    otsus = otsus.reshape((16))
    otsus = numpy.sort(otsus)[13:16]
    otsus = otsus.tolist()
    suma = 0
    for a in otsus:
        suma += a
    suma = suma / len(otsus)
        

    _, th_otsu = cv2.threshold(crp, suma, 255, cv2.THRESH_BINARY)

    th_otsu = np.uint8(th_otsu)

    # KONTURY
    ###########
    # KONTURY #
    ###########

    # generuji nefiltrované kontury
    raw_cnts = cv2.findContours(th_otsu, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]

    # SAVE RAW KONTURY
    # orig = cv2.drawContours(orig, raw_cnts, -1, (0, 0, 255), 15)
    if save_debug or True:
        cv2.imwrite("debug/4.okraje/{}.png".format(actual_img), cv2.drawContours(orig, raw_cnts, -1, (0, 0, 255), 15))


    # KRAJE
    #########
    # KRAJE #
    #########
    okraj = 300
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

        # break
    # print(nekraj_cnts)

    # SAVE KRAJE KONTURY
    if save_debug or True:
        cv2.imwrite("debug/4.okraje/{}.png".format(actual_img), cv2.drawContours(orig, nekraj_cnts, -1, (0, 0, 255), 15))





