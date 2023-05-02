import os


def clear():
    def delete(path):
        # path = "debug/3.thresh/"
        dele = os.listdir(path)
        for dlt in dele:
            print(dlt)
            dlt = str(path + dlt)
            os.remove(dlt)
    delete("debug/1.BW/")
    delete("debug/2.cropped/")
    delete("debug/3.thresh/")
    delete("debug/4.CNTs/")
    delete("out/")

clear()