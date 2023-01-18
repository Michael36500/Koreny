# a) naučit  se numpy
# b) furst
#     1) solidní crop na box uvnitř
#       2x - pro horizontální a vertikální crop
#         i) spočítat graf (funukcí, ne loope => rychlejší)
#         ii) medián - z listu čísel spočítat medián
#         iii) podle mediánu najít místo zleva a zprava:
#               zprava
                lst = "list hodnot"
                thresh = "najít"
                for x in range(len(lst)):
                    x = lst[x * -1]
                    if x > thresh:
                        print(x)
                        break
#         iv) cropnout podle hodnot
#     2) check, jestli crop je solidní (zprava jede dost tvrdě až po hlínu, nikde neblbne,..)
#     3) otsu
#         i) najdu 4 body (v patternu pluska, h střed pluska dynamicky [velikost], w od pravého kraje) / zkusit i mřížku
#         ii) napsat otsu_ctverec(x leftup rohu, y leftup rohu, x rightdwn rohu, y rightdwn rohu), co vrátí doporučenej threshold pro tuto oblast
#         iii) z bodů udělám otsu čtverce s zvětšující se velikostí (1 = 200x200, 2 = 400x400, 3 = 800x800, 4 = 1600x1600), returny do listu
#         iv) najít maximu v returnech otsu čtverců, podle něho thresholdnout celej box
#     4) nějaký třízení?