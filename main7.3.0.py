
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
for actual_img in tqdm(inputs):
    # actual_img = "2022_02_23_12_50_13"
    save_debug = True


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


    # crop
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
    # cropne obrázky podle předchozích kroků
    margin = 0
    crp = bw[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]

    # save
    if save_debug:
        cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), crp)


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
    _, th_otsu = cv2.threshold(crp, int(otsus.max()), 255, cv2.THRESH_BINARY)
    cv2.imwrite("debug/3.Otsu/{}.png".format(actual_img), th_otsu)

    th_otsu = np.uint8(th_otsu)


    # kontury
    ###########
    # KONTURY #
    ###########

    # generuji nefiltrované kontury
    raw_cnts = cv2.findContours(th_otsu, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # filtrace plochu
    ####################
    # FILTRACE PLOCHOU # 
    ####################

    # funkce, na vstupu mám contury a threshold, vrátí všechny větší threshu
    def filtrAreaDumb(raw_cnts, thresh):
        out = []
        for cnt in raw_cnts[0]:
            area = cv2.contourArea(cnt)
            if area > thresh:   
                out.append(cnt)
        return out
        
    # # "chytřejší", najde top 1000. netuším, proč to dělám tímhle způsobem, ale jak někdo řekl: "když kód funguje, nešahej na něho". Stejnak to nebudu používat, protože prý je lepší mít bulharsky konstantu
    # def filtrAreaSmart (cnts):
    #     thresh = 10
    #     numbr = 100
    #     while True:
    #         temp = filtrAreaDumb(cnts, thresh)
    #         thresh += 10
    #         if len(temp) < numbr:
    #             return temp

    area_cnts = filtrAreaDumb(raw_cnts, 100)


    # ______________
    # load + zápis plochou vyfiltrovaných kontur 

    orig = cv2.imread("in/{}.jpg".format(actual_img)).astype("float64")

    orig = orig[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]

    # zamalování loga UP
    orig = cv2.rectangle(orig, (10000, 1211), (11800, 1930), (0), -1)
    orig = cv2.rectangle(orig, (0, 1100), (860, 2700), (0), -1)

    # modře ty, co jsou vyfiltrovaný ven
    orig = cv2.drawContours(orig, raw_cnts[0], -1, (255, 0, 0), 10)
    # červeně co zůstaly
    orig = cv2.drawContours(orig, area_cnts, -1, (0, 0, 255), 20)

    cv2.imwrite("debug/4.area_filtr/{}.png".format(actual_img), orig)


    #################
    # VÝŠKA / ŠÍŘKA # 
    #################

    hw_area_cnts = []
    lst = []

    for cnt in area_cnts:
        # find the minimum area rectangle
        rect = cv2.minAreaRect(cnt)

        # compare rect
        adivid = rect[1][0] / rect[1][1]
        bdivid = rect[1][1] / rect[1][0]
        if adivid < bdivid:
            divid = bdivid
        else:
            divid = adivid
        
        if divid > 1.5:
            hw_area_cnts.append(cnt)

        lst.append(divid)


    #########
    # KRAJE #
    #########


    k_hw_area_cnts = []
    thresh = 100
    for cnt in hw_area_cnts:
        # print(cnt[:, 0, 0], w)
        if (cnt[:, 0, 0] < thresh).any() or (cnt[:, 0, 0] > w - thresh).any():
            pass
        else:
            k_hw_area_cnts.append(cnt)
        


    # load + zápis plochou vyfiltrovaných kontur 

    orig = cv2.imread("in/{}.jpg".format(actual_img)).astype("float64")

    orig = orig[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]

    # zamalování loga UP
    orig = cv2.rectangle(orig, (10000, 1211), (11800, 1930), (0), -1)
    orig = cv2.rectangle(orig, (0, 1100), (860, 2700), (0), -1)

    # # modře ty, co jsou vyfiltrovaný ven
    # orig = cv2.drawContours(orig, raw_cnts[0], -1, (0, 255, 0), 5)
    # # modře ty, co jsou vyfiltrovaný ven
    # orig = cv2.drawContours(orig, hw_area_cnts, -1, (255, 0, 0), 10)
    # červeně co zůstaly
    orig = cv2.drawContours(orig, k_hw_area_cnts, -1, (0, 0, 255), 15)

    cv2.imwrite("debug/5.hw_area_filtr copy/{}.png".format(actual_img), orig)





