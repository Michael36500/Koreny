import os
import shutil
import time

inputs_jpg = os.listdir("debug/")
for x in range(100):
    time.sleep(10/100)
    print("OPRAVDU CHCEŠ VŠECHNO VYMAZAT?")
    
for x in inputs_jpg:
    print(x)
    shutil.rmtree('debug/{}'.format(x))
    os.mkdir("debug/{}".format(x))

    # break