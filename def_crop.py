import cv2

def crop (source):
    for a in source:
        print(a)



    zmensene = False 
    if zmensene == True:
        cropped = cv2.resize(source, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        cropped = cropped[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        cropped = source[1480 : 8000, 410 : right]        #crop velkých, originálů

        # zamalování loga UP
        cropped = cv2.rectangle(cropped, (8800, 0), (10290, 1409), (0, 0, 0), -1)
        cropped = cv2.rectangle(cropped, (0, 0), (1409, 1409), (0, 0, 0), -1)

    # cropped = source

    return cropped


img = cv2.imread("debug/2.cropped/2022_02_23_12_45_14.jpg", 0)
cv2.namedWindow("opencv", cv2.WINDOW_AUTOSIZE)

img = cv2.resize(img, (1920, 1080))

# for a in range(50):
    # print(a)
thr = crop(img, 10)
cv2.imshow("opencv", thr)
cv2.waitKey(0)

