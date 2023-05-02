
# importy
import cv2
import cupy as np
import numpy
import os
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
    bw = cv2.rectangle(bw, (0, 1100), (1200, 2800), (0), -1)

    # save
    cv2.imwrite("debug/1.BW/{}.png".format(actual_img), bw)


    # jedu sloupce (zvrch dolů), cut lft rgh
    suma_sloupec = np.array([])

    for sloupec in range(len(bw[0])):
        suma_sloupec = np.append(suma_sloupec, np.sum(bw[:, sloupec]))

    # plot


    # find optimal cut
    med = np.median(suma_sloupec)
    med *= 1.25
    # medlist = np.where(suma_sloupec < med)[0]
    ln = len(suma_sloupec)
    lnn = ln // 2

    for a in range(lnn, ln):
        if suma_sloupec[a] > med:
            crgh = a 
            break
    for a in range(0, lnn):
        if suma_sloupec[a] > med:
            clft = a 
            # break

    # for md in medlist:
    #     md *= -1
    #     if suma_sloupec[md - 250] < med:
    #         crgh = (medlist[md])
    #         break
    #     if md == medlist[-1]:
    # crgh = medlist[-1]


    # for md in medlist:
    #     if suma_sloupec[md + 250] < med:
    #         clft = (medlist[md])
    #         break
    #     if md == medlist[-1]:
    # clft = medlist[0]    


    # jedu řádky (zleva do prava)
    suma_radek = np.array([])

    for radek in range(len(bw)):
        suma_radek = np.append(suma_radek, np.sum(bw[radek]))

    # plot
    range_radek = range(len(suma_radek))



    # find optimal cut
    med = np.median(suma_radek)
    med *= 2
    # medlist = np.where(suma_radek < med)[0]
    ln = len(suma_radek)
    lnn = ln // 2

    for a in range(lnn, ln):
        if suma_radek[a] > med:
            cbot = a 
            break
    for a in range(0, lnn):
        if suma_radek[a] > med:
            ctop = a 
            # break



    # # find optimal cut
    # med = np.median(suma_radek)
    # medlist = np.where(suma_radek < med)[0]

    # cbot = medlist[-1]

    # # for md in medlist:
    # #     if suma_radek[md - 250] < med:
    # #         cbot = (medlist[md])
    # #         break
    # #     if md == medlist[-1] * -1:
    # #         cbot = medlist[-1]


    # # for md in medlist:
    # #     if suma_radek[md + 250] < med:
    # #         ctop = (medlist[md])
    # #         break
    # #     if md == medlist[-1]:
    # ctop = medlist[0]
    # #         ctop = medlist[0]




    # cropne obrázky podle předchozích kroků
    margin = 0
    crp = bw[int(ctop+margin) : int(cbot-margin), int(clft+margin) : int(crgh-margin)]


    cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), crp)
