import cv2
import numpy as np
import os

def filtrTvar(inCNS, img):
   # filtrovat budu za pomoci větší strana/menší, pokud výsledek bude větší jak 3, tak je to kořen, jinak ne
    out_el = []
    out_cnt = []
    out_box = []


    for cnt in inCNS:
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
        if div > 3:
            out_el.append(elps)
            out_cnt.append(cnt)
            out_box.append(box)

            elimg = cv2.drawContours(elimg,[box],0,(255,255,255),20)
            box = []

