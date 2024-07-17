
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

# 0 1 2
# 3 4 5
# 6 7 8
def evauluateBoard(board):
    # win checks
    if board[0] == board[1] and board[1] == board[2] and board[0] != 0:
        return board[0]

    if board[3] == board[4] and board[4] == board[5] and board[3] != 0:
        return board[3]

    if board[6] == board[7] and board[7] == board[8] and board[6] != 0:
        return board[6]

    if board[0] == board[4] and board[4] == board[8] and board[0] != 0:
        return board[0]

    if board[2] == board[4] and board[4] == board[6] and board[2] != 0:
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
        if turn == 2:
            return 10 - depth
        else:
            return -10 + depth

    if turn == 1:
        bestVal = -1000

        for i in range(9):
            if board[i] != 0:
                continue

            value = minimax(a + turn * (3 ** i), depth + 1)            

            if value > bestVal:
                bestVal = value
                bestMove = i

        DP[a] = bestVal
        OM[a] = bestMove
    else:
        bestVal = 1000

        for i in range(9):
            if board[i] != 0:
                continue

            value = minimax(a + turn * (3 ** i), depth + 1)            

            if value < bestVal:
                bestVal = value
                bestMove = i

        DP[a] = bestVal
        OM[a] = bestMove

    return DP[a]

def fillOMROT():
    for i in range(len(OMROT)):
        OMROT[minRotBoard(intToBoard(i))] = OM[i]  

if __name__ == '__main__':
    minimax(0, 0)
    fillOMROT()

    print(OM[1])
    print(OM[9])
    print(OM[3 ** 6])
    print(OM[3 ** 8])

    # printBoard(intToBoard(11))
    # print(boardToInt(intToBoard(3 ** 8)))

    # tint = 180
    # board = intToBoard(tint)
    # turn = boardToTurn(board)

    # printBoard(board)
    # print(turn)

    # printBoard(intToBoard(tint+ turn * 3 ** OM[0]))

    # mx = 0
    # for index, value in enumerate(OMROT):
    #     if value != -1:
    #         mx = max(index, mx)

    # print(mx)
    # print(OMROT[0:mx + 1])

    # mx2 = 0
    # for index, value in enumerate(OMROT):
    #     if value != -1 and index < mx:
    #         mx2 = max(index, mx2)

    # print(mx2)
        
