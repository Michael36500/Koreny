import cv2
import numpy as np
from scipy import ndimg
import os

files = os.listdir("in")
img_num = 0

for actualf in files:

# terminal output
    img_num = img_num + 1
    print(img_num)
    print("    ",actualf)

# img read + H,W
    img = cv2.imread("in/{}".format(actualf), 0).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    h, w = img.shape[:2]

# crop obrázků
        # zmenšit, oříznout SD / ořiznout 10K
    zmenseni = True
    if zmenseni == True:
        img = cv2.resize(img, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        img = img[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        img = img[1480 : 8000, 410 : 10700]        #crop velkých, originálů

# ukládání debug
    # edged_img = cv2.putText(edged_img, str(sum(plocha)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2 , cv2.LINE_AA) 
    # cv2.imwrite("debug/debug.{}.{}.{}.png".format(actualf, min_x, len(xcnts)), edged_img)
    
# ukládání originálů
    # img = cv2.putText(img, str(min_cm), (0, 1000), cv2.FONT_HERSHEY_SIMPLEX, 40, (255, 255, 255), 40, cv2.LINE_AA)
    # img = cv2.putText(img, str(sum(plocha)), (0, 2000), cv2.FONT_HERSHEY_SIMPLEX, 40, (255, 255, 255), 40, cv2.LINE_AA)
    cv2.imwrite("out/{}.jpg".format(actualf), img)
    # break