from src.lsystem import *

lsys = LSystem("F", {
    "F": "Y[++++++MF][-----NF][^^^^^OF][&&&&&PF]",
    "M": "Z-M",
    "N": "Z+N",
    "O": "Z&O",
    "P:": "Z^P",
    "Y": "Z-ZY+",
    "Z": "ZZ",
},)


for _ in range(3):
    lsys.step()
    print(lsys.axiom)
