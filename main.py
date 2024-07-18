
from VMparser import Parser
from minimax import OMROT, minimax, fillOMROT
from math import ceil

def compileTTT():
    P = Parser()
    P.parseFile('TTT')
    P.writeFile('TTT')

optimize_end = 24

def buildPerfect():
    minimax(0, 0)
    fillOMROT()

    final = [-1 for _ in range(3 ** 8)]

    for i in range(len(OMROT) // 3):
        if OMROT[i * 3] == -1 and OMROT[i * 3 + 1] == -1 and OMROT[i * 3+ 2] == -1:
            continue

        final[i] = max(OMROT[i * 3], 0) + max(OMROT[i * 3 + 1], 0) * 2 ** 4 + max(OMROT[i * 3 + 2], 0) * 2 ** 8

    ff = [x for x in final]
    
    optim_values = []
    for _ in range(optimize_end):
        mx = 0
        for i in range(len(final)):
            if final[i] != -1:
                mx = i

        optim_values.append((mx, final[mx]))
        final = final[:mx]

    mx = 0
    for i in range(len(final)):
        if final[i] != -1:
            mx = i

    final = final[:mx + 1]
    
    with open('Perfect.vm', 'w') as f:
        f.write("function Perfect.move 0\n")    

        for (i, v) in optim_values:
            f.write("push argument 0\n")
            f.write(f"push constant {i}\n")
            f.write("eq\n")
            f.write("not\n")
            f.write("if-goto PERFECT_START\n")
            f.write(f"push constant {v}\n")
            f.write("return\n")

        f.write("label PERFECT_START\n")
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


