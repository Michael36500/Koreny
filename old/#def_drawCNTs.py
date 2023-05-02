import cv2
import numpy as np


def drawCNTs(cropped, area_cnts):

    cnt_cropped = np.copy(cropped) * 2  # creating a blank to draw cnts on
        # # obtáhnutí vybraných kontur
    for cnt in area_cnts:
        for pix in cnt:
            for px in pix:
                i = int(px[1])
                j = int(px[0])
                # print(i, "           ", j)
                # print(img[i][j])
                cnt_cropped[i][j] = 255
    return cnt_cropped