
tmap = [' ', 'x', 'o']

def intToBoard(a):
    r = []

    while a:
        o = a % 3        
        a = a // 3

        r.append(o)

    r.extend([0 for _ in range(9 - len(r))])

    return r

def boardToInt(board):
    return sum([board[i] * (3 ** i) for i in range(9)])

def minRotBoard(board):
    r = sum([board[i] * (3 ** i) for i in range(9)])

    c = [x for x in board]
    for _ in range(3):
        c[0], c[2], c[6], c[8] = c[2], c[6], c[8], c[0]
        c[1], c[3], c[5], c[7] = c[3], c[5], c[7], c[1]
        r = min(r, sum([c[i] * (3 ** i) for i in range(9)]))

    return r


def printBoard(board):
    for i in range(3):
        print('|'.join(map(lambda x: tmap[x],board[i*3:(i + 1)*3])))

        if i < 2:
            print('-+-+-')
    
DP = [-1 for i in range(3**9)]
OM = [-1 for i in range(3**9)]
OMROT = [-1 for i in range(3**9)]

def evauluateBoard(board):
    # win checks
    if board[0] == board[1] and board[1] == board[2] and board[0] != 0:
        return board[0]

    if board[3] == board[4] and board[4] == board[5] and board[3] != 0:
        return board[3]

    if board[6] == board[7] and board[7] == board[8] and board[6] != 0:
        return board[6]

    if board[0] == board[5] and board[5] == board[8] and board[0] != 0:
        return board[0]

    if board[2] == board[5] and board[5] == board[6] and board[2] != 0:
        return board[2]

    if board[0] == board[3] and board[3] == board[6] and board[0] != 0:
        return board[0]

    if board[1] == board[4] and board[4] == board[7] and board[1] != 0:
        return board[1]

    if board[2] == board[5] and board[5] == board[8] and board[2] != 0:
        return board[2]

    # draw
    if not len([x for x in board if x == 0]):
        return 3

    # ongoing
    return 0

def boardToTurn(board):
    c1 = board.count(1)
    c2 = board.count(2)

    return 2 - int(c1 == c2)

def minimax(a, depth):
    if DP[a] != -1:
        return DP[a]
    
    board = intToBoard(a)
    turn = boardToTurn(board)
    v = evauluateBoard(board)
    
    if v == 3:
        return 0

    if v:
        return (1 - 2 * (turn != v)) * (10 - depth)

    f0 = board.index(0)
    mn = minimax(a + turn * (3 ** f0), depth + 1)
    mni = f0
    mx = mn
    mxi = f0

    for i in range(9):
        if board[i]:
            continue

        nv = minimax(a + turn * (3 ** i), depth + 1)

        if nv < mn:
            mn = nv            
            mni = i

        if nv > mx:
            mx = nv
            mxi = i

    if turn == 1:
        DP[a] = mx       
        OM[a] = mxi
        return mx 
    else:
        DP[a] = mn
        OM[a] = mni
        return mn

if __name__ == '__main__':
    minimax(0, 0)
    for i in range(3**9):
        print(i, OM[i])

    tint = 180
    board = intToBoard(tint)
    turn = boardToTurn(board)

    printBoard(board)
    print(turn)

    printBoard(intToBoard(tint+ turn * 3 ** OM[0]))

    for i in range(len(OMROT)):
        OMROT[minRotBoard(intToBoard(i))] = OM[i]

    mx = 0
    for index, value in enumerate(OMROT):
        if value != -1:
            mx = max(index, mx)

    print(mx)
        
