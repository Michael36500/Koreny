# %%
# importy
import cv2
import cupy as np
import numpy
import os
from tqdm import tqdm
import time

# %%
# najde všechny soubory v IN složce, aby se mohl loopnout
inputs_jpg = os.listdir("in/")
inputs = []
for a in inputs_jpg:
    if a[0] == "X":
        continue
    l = len(a)
    short = a[:l - 4]
    inputs.append(short)


# %%
# příprava loopu
for actual_img in tqdm(inputs):
    # break
# print(actual_img)

    # %%
    # načte BW obrázek
    bw = cv2.imread("in/{}.jpg".format(actual_img), 0) # 0 protože chci černobílý obrázek (pro krok úprava)

    # %%
    # zamalování loga UP
    bw = cv2.rectangle(bw, (10000, 1211), (11800, 1930), (0), -1)
    bw = cv2.rectangle(bw, (0, 1100), (860, 2700), (0), -1)

    # save
    # cv2.imwrite("debug/1.BW/{}.png".format(actual_img), bw)

    # %%
    # jedu sloupce (zvrch dolů)
    suma_sloupec = np.array([])

    for sloupec in range(len(bw[0])):
        suma_sloupec = np.append(suma_sloupec, np.sum(bw[:, sloupec]))
    # print(suma_sloupec)

    # plot
    range_sloupce = range(len(suma_sloupec))


    # %%
    # find optimal cut
    med = np.median(suma_sloupec)
    med = np.where(suma_sloupec < med)

    ctop = (med[0][0])
    cbot = (med[0][-1])

    # %%
    # jedu řádky (zleva do prava)
    suma_radek = np.array([])

    for radek in range(len(bw)):
        suma_radek = np.append(suma_radek, np.sum(bw[radek]))
    # print(suma_radek)

    # plot
    range_radek = range(len(suma_radek))


    # %%
    # find optimal cut
    med = np.median(suma_radek)
    med = np.where(suma_radek < med)

    clft = (med[0][0])
    crgh = (med[0][-1])

    # %%
    # cropne obrázky podle předchozích kroků
    margin = 0
    crp = bw[int(clft+margin) : int(crgh-margin), int(ctop+margin) : int(cbot-margin)]
    print(ctop, cbot, clft, crgh)
    # print(crp)

    # print(crp)

    cv2.imwrite("debug/2.cropped/{}.png".format(actual_img), crp)

    # %%



