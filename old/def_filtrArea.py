import cv2
import numpy


def filtrArea (cnts):

    # filtruj kontury podle plochy
    def TrueFilter(cnts, s1):
        
        area_cnts = []
        for cnt in cnts:    
            print(cnt)
            # print(cnt)
        # osobně nevím, proč to takhle je, ale funguje to...
            cnt = list(cnt)
            # cnt.pop(-1)
            # for cn in cnt:
            print("HERE", cnt)
            # print(cn, "XXXXXXX")
            # print(cv2.contourArea(cn))
            # cn = cn.astype("float32")

            # print(cn)
            # print(cv2.contourArea(cn))
            if s1<cv2.contourArea(cnt):
                print("CHOSEN")
                
                area_cnts.append(cnt)
        return area_cnts

    # while True najde dynamicky ideální tresh plochy

    # s1 -> základ thresholdu, a od něj jdu po 10 nahoru, dokud se nedostanu k THRESH (max. počet objektů, pokud jich je +THRESH, tak zvýším S1 o 10, znovu)
    s1 = 10
    thresh = 250
    # print(len(cnts))
    while True:
        temp = TrueFilter(cnts, s1)
        s1 = s1 + 10
        # print(s1)
        if len(temp) < thresh:
            return temp
            


    

                

    return area_cnts

