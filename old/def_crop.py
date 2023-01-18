import cv2
from tqdm import tqdm
from matplotlib import pyplot as plt

def crop (source):
    #########################
    # inteligentní crop nevyšel, protože by to nálepka rušila, a kdybych ji zamaloval, tak na průměr má moc velkej vliv, a taky je Míša línej


    # h, w = img.shape[:2]
    # # for a in tqdm(range(w)):
    # #     suma = 0
    # #     for b in range(h):
    # #         suma = suma + source[b][a]
    # #     cols.append(suma)
    # # print(cols)
    # width = []
    # for a in range(w):
    #     a = a + 1
    #     # print(a)
    #     width.append(a)

    # cols = []

    # rotated = cv2.rotate(source, cv2.cv2.ROTATE_90_CLOCKWISE)
    # for a in rotated:
    #     suma = 0
    #     for b in a:
    #         suma = suma + b
    #     cols.append(suma)

    # print(width)
    # print(cols)


    # plt.plot(width, cols)
    # plt.show()

    zmensene = False 
    if zmensene == True:
        cropped = source
        # cropped = cv2.resize(source, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        # cropped = cropped[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        # cropped = source[1480 : 8000, 410 : right]        #crop velkých, originálů
        cropped = source[1480 : 8000, 410 : 10200]        #crop velkých, originálů

        # zamalování loga UP
        cropped = cv2.rectangle(cropped, (8800, 0), (10290, 1409), (0, 0, 0), -1)
        cropped = cv2.rectangle(cropped, (0, 0), (1409, 1409), (0, 0, 0), -1)
    # cropped = source

    return cropped


# img = cv2.imread("debug/2.cropped/2022_02_23_12_45_14.png", 0)
# cv2.namedWindow("opencv", cv2.WINDOW_AUTOSIZE)

# img = cv2.resize(img, (266, 200))
# # print(img)

# # for a in range(50):
#     # print(a)
# thr = crop(img)
# print(thr)
# cv2.imshow("opencv", thr)
# cv2.waitKey(0)

