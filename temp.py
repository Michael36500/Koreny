for x in range(11):
    x /= 10
    for y in range(11):
        y /= 10
        for z in range(10):
            z += 1
            z *= 100
            print("[", [x], ", ", [y], ", ", [z], "]", ", ", sep="")