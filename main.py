
from VMparser import Parser
from minimax import OMROT, minimax, fillOMROT
from math import ceil

osFiles = [
    "OS/Array",
    "OS/Keyboard",
    "OS/Math",
    "OS/Memory",
    # "OS/Output",
    "OS/Screen",
    "OS/String",
    # "OS/Sys",
]

def compileTTT():
    P = Parser()
    P.parseFile('TTT')
    P.writeFile('TTT')

def buildPerfect():
    minimax(0, 0)
    fillOMROT()

    final = [-1 for _ in range(3 ** 8)]
    mx = 0

    for i in range(len(OMROT) // 3):
        if OMROT[i * 3] == -1 and OMROT[i * 3 + 1] == -1 and OMROT[i * 3+ 2] == -1:
            continue

        final[i] = max(OMROT[i * 3], 0) + max(OMROT[i * 3 + 1], 0) * 2 ** 4 + max(OMROT[i * 3 + 2], 0) * 2 ** 8

    # mx1 = 0
    # for i in range(len(final)):
    #     if final[i] != -1:
    #         mx1 = i

    # final1 = final[0:mx1 + 1]

    # mx2 = 0
    # for i in range(len(final1) - 1):
    #     if final[i] != -1:
    #         mx2 = i

    # final2 = final1[0:mx2 + 1]

    # mx3 = 0
    # for i in range(len(final2) - 1):
    #     if final[i] != -1:
    #         mx3 = i

    # final3 = final2[0:mx3 + 1]

    # print(mx1, mx2, mx3)

    with open('Perfect.vm', 'w') as f:
        f.write("function Perfect.move 0\n")    
        f.write("push argument 0\n")
        f.write("pop jumptable 0\n")

        for x in final:
            f.write(f"push jumptable {x}\n")

        f.write("jumptable-end\n")
        f.write("return\n")

def link(files):
    with open('TTT.vm', 'w') as f:
        f.write("sp\ncall Memory.init 0\n call Math.init 0\n call Screen.init 0\n call Main.main 0\nep\n\n")
        
        for file in files:
            with open(file, 'r') as rf:
                f.write(rf.read())
                f.write('\n')

if __name__ == '__main__':
    buildPerfect()
    link([
        "src/Main.vm",
        "OS/Array.vm",
        "OS/Screen.vm",
        "OS/Math.vm",
        "OS/Memory.vm",
        "OS/Keyboard.vm",
        "src/Player.vm",
        "src/Game.vm",
        "src/ScreenUtil.vm",
        "Perfect.vm"
    ])
    compileTTT()


