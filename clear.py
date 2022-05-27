import os

def clear():
    path = "debug/1.BW/"
    dele = os.listdir(path)
    for dlt in dele:
        print(dlt)
        dlt = str(path + dlt)
        os.remove(dlt)  

    path = "debug/2.cropped/"
    dele = os.listdir(path)
    for dlt in dele:
        print(dlt)
        dlt = str(path + dlt)
        os.remove(dlt)

    path = "debug/3.thresh/"
    dele = os.listdir(path)
    for dlt in dele:
        print(dlt)
        dlt = str(path + dlt)
        os.remove(dlt)

    path = "out/"
    dele = os.listdir(path)
    for dlt in dele:
        print(dlt)
        dlt = str(path + dlt)
        os.remove(dlt)


clear()