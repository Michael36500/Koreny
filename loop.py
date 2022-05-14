import cv2
import numpy as np
import os
import cannyED as ed

# bake je funukce, co a) přepočítá obrázek b) uloží a znovu otevře obrázek
def bake(hard = None):
    global img
    if hard == True:
        cv2.imwrite("temp.png", img)
        img = cv2.imread("temp.png")
    else:
        img = img.astype(np.uint8)

files = os.listdir("in")
img_num = 0
th_dos = 11

for actualf in files:

# terminal output
    img_num = img_num + 1
    print(img_num)
    print("    ",actualf)

# img read + H,W
    img = cv2.imread("in/{}".format(actualf)).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    h, w = img.shape[:2]

# crop obrázků
        # zmenšit, oříznout SD / ořiznout 10K
    zmenseni = True
    if zmenseni == True:
        img = cv2.resize(img, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        img = img[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        img = img[1480 : 8000, 410 : 10700]        #crop velkých, originálů
    # cv2.imwrite("temp.png", img)
    # img = cv2.imread("temp.png")
    bake()
# efekty
    # th, img = cv2.threshold(img, th_dos, 255, cv2.THRESH_BINARY)




    img = ed.Canny_detector(img, 70)

































# ukládání debug
    # edged_img = cv2.putText(edged_img, str(sum(plocha)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2 , cv2.LINE_AA) 
    # cv2.imwrite("debug/debug.{}.{}.{}.png".format(actualf, min_x, len(xcnts)), edged_img)
    
# ukládání originálů
    # img = cv2.putText(img, str(min_cm), (0, 1000), cv2.FONT_HERSHEY_SIMPLEX, 40, (255, 255, 255), 40, cv2.LINE_AA)
    # img = cv2.putText(img, str(sum(plocha)), (0, 2000), cv2.FONT_HERSHEY_SIMPLEX, 40, (255, 255, 255), 40, cv2.LINE_AA)
    cv2.imwrite("out/{}.jpg".format(actualf), img)
    break