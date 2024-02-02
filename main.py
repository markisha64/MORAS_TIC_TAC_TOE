
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

    mx = 0
    for index, value in enumerate(OMROT):
        if OMROT[index] != -1:
            mx = max(mx, index)

    mx1 = 0
    for index, value in enumerate(OMROT[:mx]):
        if OMROT[index] != -1:
            mx1 = max(mx1, index)

    final = [0 for _ in range(ceil(mx1 / 3))]

    for i in range(mx1 + 1):
        v = max(OMROT[i], 0)

        final[i // 3] += v * 32 ** (i % 3)

    with open('Perfect.vm', 'w') as f:
        f.write("function Perfect.move 0\n")    
        f.write("push argument 0\n")
        f.write(f"push constant {mx}\n")
        f.write("eq\n")
        f.write("neg\n")
        f.write("if-goto jt\n")
        f.write(f"push constant {OMROT[mx]}\n")
        f.write("return\n")
        f.write("label jt\n")
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
        "Main.vm",
        "OS/Array.vm",
        "OS/Screen.vm",
        "OS/Math.vm",
        "OS/Memory.vm",
        "OS/Keyboard.vm",
        "Perfect.vm"
    ])
    compileTTT()


