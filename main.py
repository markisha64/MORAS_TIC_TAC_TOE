
from VMparser import Parser
from minimax import OMROT, minimax, fillOMROT
import re

def compileTTT():
    P = Parser()
    P.parseFile('TTT')
    P.writeFile('TTT')

    with open('TTT.asm') as file:
        b = file.read()

    stripped = [x for x in b.split('\n') if not re.search(r"^//.*", x) and not re.search(r"\(.*\)", x) ]

    with open('TTT_stripped.asm', 'w') as file:
        for line in stripped:
            file.write(f"{line}\n")

    print(len(stripped))

def buildSwaps():
    swaps = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    
    with open("Swaps.vm", "w") as f:
        f.write("function Swaps.get 0\n")    
        f.write("push argument 0\n")
        f.write("pop jumptable 0\n")

        for swap in swaps:
            f.write(f"push jumptable {swap}\n")

        f.write("jumptable-end\n")
        f.write("return\n")
        

optimize_end = 39

def buildPerfect():
    minimax(0, 0)
    fillOMROT()

    final = [-1 for _ in range(3 ** 8)]

    for i in range(len(OMROT) // 3):
        if OMROT[i * 3] == -1 and OMROT[i * 3 + 1] == -1 and OMROT[i * 3+ 2] == -1:
            continue

        final[i] = max(OMROT[i * 3], 0) + max(OMROT[i * 3 + 1], 0) * 2 ** 4 + max(OMROT[i * 3 + 2], 0) * 2 ** 8
    
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

    grouped = {}
    for (i, v) in optim_values:
        if v not in grouped:
            grouped[v] = []

        grouped[v].append(i)

    ncounter = 0
    
    with open('Perfect.vm', 'w') as f:
        f.write("function Perfect.move 0\n")    

        for k, v in grouped.items():           
            f.write("push argument 0\n")
            f.write(f"push constant {v[0]}\n")
            f.write("eq\n")

            for i in range(1, len(v)):
                f.write("push argument 0\n")
                f.write(f"push constant {v[i]}\n")
                f.write("eq\n")
                f.write("or\n")

            f.write("not\n")
            f.write(f"if-goto NEXT_{ncounter}\n")
            f.write(f"push constant {k}\n")
            f.write("return\n")
            f.write(f"label NEXT_{ncounter}\n")

            ncounter = ncounter + 1

        f.write("push argument 0\n")
        f.write("pop jumptable 0\n")
           
        for x in final:
            f.write(f"push jumptable {max(x, 0)}\n")

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
    buildSwaps()
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
        "Perfect.vm",
        "Swaps.vm"
    ])
    compileTTT()


