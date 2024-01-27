
from VMparser import Parser

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

def link(files):
    with open('TTT.vm', 'w') as f:
        f.write("sp\ncall Memory.init 0\n call Math.init 0\n call Screen.init 0\n call Main.main 0\nep\n\n")
        
        for file in files:
            with open(file, 'r') as rf:
                f.write(rf.read())
                f.write('\n')

if __name__ == '__main__':
    link([
        "Main.vm",
        "OS/Array.vm",
        "OS/Screen.vm",
        "OS/Math.vm",
        "OS/Memory.vm",
        "OS/Keyboard.vm",
    ])
    compileTTT()


