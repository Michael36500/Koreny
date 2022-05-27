import cv2

def crop (source):

    zmensene = False 
    if zmensene == True:
        cropped = cv2.resize(source, (800, 600))                     # POZOR, ROZMĚRY SE NEPOČÍTAJÍ
        cropped = cropped[100 : 540, 70 : 700]        #crop malých, mnou zmenšeny
    else:
        cropped = source[1480 : 8000, 410 : 10700]        #crop velkých, originálů

        # zamalování loga UP
        cropped = cv2.rectangle(cropped, (8800, 0), (10290, 1409), (0, 0, 0), -1)
        cropped = cv2.rectangle(cropped, (0, 0), (1409, 1409), (0, 0, 0), -1)

    # cropped = source

    return cropped