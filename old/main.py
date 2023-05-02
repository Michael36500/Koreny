import cv2
import numpy as np
import os
import cannyED as ed
from tqdm import tqdm 

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

for actualf in tqdm(files):

# terminal output
    img_num = img_num + 1
    # print(img_num)
    # print("    ",actualf)

# img read + H,W
    img = cv2.imread("in/{}".format(actualf)).astype("float64") # 0 protože chci černobílý obrázek (pro krok úprava)
    h, w = img.shape[:2]

# crop obrázků
        # zmenšit, oříznout SD / ořiznout 10K
    zmensene = False 
    if zmensene == True:
        img = cv2.resize(img, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        img = img[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        img = img[1480 : 8000, 410 : 10700]        #crop velkých, originálů
    # cv2.imwrite("temp.png", img)
    # img = cv2.imread("temp.png")
    bake(False)
    cv2.imwrite("debug/1.zmenseny/{}".format(actualf), img)

# th efekt
    th_dos = 40
    th, img = cv2.threshold(img, th_dos, 255, cv2.THRESH_BINARY)
    bake(False)

# najdi kontury
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("debug/2.treshold/{}".format(actualf), img)
    # cnts = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #[-2]
    ocnts = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# filtruj kontury podle plochy
    s1 = 750
    cnts = []
    
    for cnt in ocnts:
        # osobně nevím, proč to takhle je, ale funguje to...
        cnt = list(cnt)
        cnt.pop(-1)
        for cn in cnt:
            # print(cn, "XXXXXXX")
            if s1<cv2.contourArea(cn):
                
                cnts.append(cn)
# filtrace kontur pomocí tvaru
    # filtrovat budu za pomoci větší strana/menší, pokud výsledek bude větší jak 3, tak je to kořen, jinak ne
    out_el = []
    out_cnt = []
    out_box = []
    for cnt in cnts:
        elps = cv2.fitEllipse(cnt)
        
        # print(elps)

        rot_rectangle = elps
        box = cv2.boxPoints(rot_rectangle) 
        box = np.int0(box) #Convert into integer values
        stra = elps [1][0]
        strb = elps [1][1]

        # teď budu dělit. protože čísla vycházejí stra menší než strb, tak nemusím dělat nějak velký ošklivý check, co by porovnal ty dvě čísla, a dělil větší menším.
        div = strb // stra
        if div < 1:
            print("error filtrace kontur, potřeba přidat check")
        if div > 3:
            out_el.append(elps)
            out_cnt.append(cnt)
            out_box.append(box)
            img = cv2.drawContours(img,[box],0,(255,255,255),10)
        # print(stra)
        # print(strb)

        # print()

        # vrací: ((pozice)(velikost)rotace)


    

    cv2.imwrite("debug/2.5.elps/{}".format(actualf), img)
    
        

# obtáhnutí vybraných kontur
    for cnt in out_cnt:
        for pix in cnt:
            for px in pix:
                i = int(px[1])
                j = int(px[0])
                # print(i, "           ", j)
                # print(img[i][j])
                img[i][j] = 255
    # print(cnts)

    timg = np.copy(img) * 0  # creating a blank to draw cnts on
    cv2.drawContours(timg, cnts, -1, (255, 255, 255), 3)
    cv2.imwrite("debug/3.kontury/{}".format(actualf), timg)



# najití čar

    # Then, use HoughLinesP to get the lines. You can adjust the parameters for better performance.

    # rho = 1  # distance resolution in pixels of the Hough grid
    # theta = 10 * np.pi / 180  # angular resolution in radians of the Hough grid
    # threshold = 140  # minimum number of votes (intersections in Hough grid cell)
    # min_line_length = 40  # minimum number of pixels making up a line
    # max_line_gap = 100  # maximum gap in pixels between connectable line segments

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    # lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    # print(lines)
# ztmavení obrázku
    # img = img // 5
    # bake(False)

# # filtrace čar
#     for line in lines:
#         print(line[0])

# zakreslení čar
    # !!!!!!!!!!!!!!!!!!!! limg = temp img na čáry, aby se dali uložit a nepřepsal se původní

    # limg = np.copy(img) * 0  # creating a blank to draw lines on
    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    #         cv2.line(limg,(x1,y1),(x2,y2),255,1)
    # bake(False)

# # úprava obrázku s čarami
#     blur = 10
#     limg = cv2.blur(limg, (blur, blur))
#     th, limg = cv2.threshold(limg, 1, 255, cv2.THRESH_BINARY)


# # najití čar podruhé

#     # Then, use HoughLinesP to get the lines. You can adjust the parameters for better performance.

#     rho = 10  # distance resolution in pixels of the Hough grid
#     theta = 5 * np.pi / 180  # angular resolution in radians of the Hough grid
#     threshold = 100  # minimum number of votes (intersections in Hough grid cell)
#     min_line_length = 100  # minimum number of pixels making up a line
#     max_line_gap = 40  # maximum gap in pixels between connectable line segments
#     limg = np.copy(img) * 0  # creating a blank to draw lines on

#     # Run Hough on edge detected image
#     # Output "lines" is an array containing endpoints of detected line segments
#     lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
#     # print(lines)
# # ztmavení obrázku
#     img = img // 5
#     bake(False)

# # # filtrace čar
# #     for line in lines:
# #         print(line[0])

# # zakreslení čar

#     for line in lines:
#         for x1,y1,x2,y2 in line:
#             cv2.line(limg,(x1,y1),(x2,y2),255,1)
#     bake(False)

# # úprava obrázku s čarami
#     # blur = 10
#     # limg = cv2.blur(limg, (blur, blur))
#     # th, limg = cv2.threshold(limg, 1, 255, cv2.THRESH_BINARY)


















# obtáhnutí vybraných kontur
    # for cnt in cnts:
    #     for pix in cnt:
    #         for px in pix:
    #             i = int(px[1])
    #             j = int(px[0])
    #             # print(i, "           ", j)
    #             # print(img[i][j])
    #             img[i][j] = 255
    # print(cnts)
    # cv2.drawContours(img, xcnts, -1, (0, 255, 0), 3)
# filtruj kontury podle elipsy





    # img = ed.Canny_detector(img, 70)

# ukládání debug
    # edged_img = cv2.putText(edged_img, str(sum(plocha)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2 , cv2.LINE_AA) 
    # cv2.imwrite("debug/debug.{}.{}.{}.png".format(actualf, min_x, len(xcnts)), edged_img)
    
# ukládání originálů
    # img = cv2.putText(img, str(min_cm), (0, 1000), cv2.FONT_HERSHEY_SIMPLEX, 40, (255, 255, 255), 40, cv2.LINE_AA)
    # img = cv2.putText(img, str(sum(plocha)), (0, 2000), cv2.FONT_HERSHEY_SIMPLEX, 40, (255, 255, 255), 40, cv2.LINE_AA)
    cv2.imwrite("out/{}".format(actualf), img)
    
    
    
    break 