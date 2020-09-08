import sys
from random import choice


def display(board, moves):
    listBoard = list(board)
    for i in moves:
        listBoard[i] = '*'
    newBoard = ''.join(listBoard)
    for i in range(0, 64, 8):
        print(newBoard[i:i+8])

def score(board):
    return str(board.count('X')) + "/" + str(board.count('O'))

def value(board):
    return board.count('X') - board.count('O')

def codetoidx(code):
    return (int(code[1])-1)*8 + (ord(code[0]) - ord('A'))

def checkidx(boards, tkn):
    idxs = {}
    board = [list(boards[i:i + 8]) for i in range(0, 64, 8)]
    for idx in range(64):
        if boards[idx] != '.': continue
        x = idx // 8
        y = idx % 8
        i = x+1
        while(i < 8):
            if(board[i][y] == '.'): break
            if(board[i][y] == tkn and i != x+1):
                if(idx not in idxs): idxs[idx] = []
                idxs[idx].append((0, (i*8)+y))
                break
            elif(board[i][y] == tkn):
                break
            i+=1
        i = x-1
        while (i >= 0):
            if (board[i][y] == '.'): break
            if (board[i][y] == tkn and i != x-1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((1, (i * 8) + y))
                break
            elif(board[i][y] == tkn):
                break
            i -= 1
        j = y + 1
        while (j < 8):
            if (board[x][j] == '.'): break
            if (board[x][j] == tkn and j != y+1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((2, (x * 8) + j))
                break
            elif(board[x][j] == tkn):
                break
            j += 1
        j = y - 1
        while (j >= 0):
            if (board[x][j] == '.'): break
            if (board[x][j] == tkn and j != y-1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((3, (x * 8) + j))
                break
            elif(board[x][j] == tkn):
                break
            j -= 1
        k = 1
        while(x+k < 8 and y+k < 8):
            if (board[x+k][y+k] == '.'): break
            if(board[x+k][y+k] == tkn and k != 1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((4, ((x+k) * 8) + y+k))
                break
            elif(board[x+k][y+k] == tkn):
                break
            k+=1
        k = 1
        while (x - k >= 0 and y - k >= 0):
            if (board[x - k][y - k] == '.'): break
            if (board[x - k][y - k] == tkn and k != 1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((5, ((x-k) * 8) + y-k))
                break
            elif(board[x-k][y-k] == tkn):
                break
            k += 1
        k = 1
        while (x + k < 8 and y - k >= 0):
            if (board[x + k][y - k] == '.'): break
            if (board[x + k][y - k] == tkn and k != 1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((6, ((x+k) * 8) + y-k))
                break
            elif(board[x+k][y-k] == tkn):
                break
            k += 1
        k = 1
        while (x - k >= 0 and y + k < 8):
            if (board[x - k][y + k] == '.'): break
            if (board[x - k][y + k] == tkn and k != 1):
                if (idx not in idxs): idxs[idx] = []
                idxs[idx].append((7, ((x-k) * 8) + y+k))
                break
            elif(board[x-k][y+k] == tkn):
                break
            k+=1
    return idxs

def move(boards, tkn, idx0, moves):
    board = [list(boards[i:i+8]) for i in range(0, 64, 8)]
    board[idx0//8][idx0%8] = tkn
    for tup in moves[idx0]:
        a = tup[0]
        idx = tup[1]
        x = idx // 8
        y = idx % 8
        if(a == 1):
            i = x + 1
            while (i*8 + y != idx0):
                board[i][y] = tkn
                i += 1
        elif(a == 0):
            i = x - 1
            while (i*8 + y != idx0):
                board[i][y] = tkn
                i -= 1
        elif(a == 3):
            j = y + 1
            while (x*8 + j != idx0):
                board[x][j] = tkn
                j += 1
        elif (a == 2):
            j = y - 1
            while (x*8 + j != idx0):
                board[x][j] = tkn
                j -= 1
        elif(a == 5):
            k = 1
            while ((x+k)*8 + y+k != idx0):
                board[x+k][y+k] = tkn
                k += 1
        elif(a == 4):
            k = 1
            while ((x-k)*8 + y-k != idx0):
                board[x-k][y-k] = tkn
                k += 1
        elif(a == 7):
            k = 1
            while ((x+k)*8 + y-k != idx0):
                board[x+k][y-k] = tkn
                k += 1
        elif (a == 6):
            k = 1
            while ((x-k)*8 + y+k != idx0):
                board[x-k][y+k] = tkn
                k += 1
    return ''.join(''.join(brd) for brd in board)

def turn(board):
    if (board.count('X') + board.count('O')) % 2 == 0:
        return 'X'
    else:
        return 'O'

def remove_corners(moves, board):
    if(board[0] == '.'):
        if 1 in moves and len(moves) > 1: moves.remove(1)
        if 8 in moves and len(moves) > 1: moves.remove(8)
        if 9 in moves and len(moves) > 1: moves.remove(9)
    if(board[7] == '.'):
        if 6 in moves and len(moves) > 1: moves.remove(6)
        if 15 in moves and len(moves) > 1: moves.remove(15)
        if 14 in moves  and len(moves) > 1: moves.remove(14)
    if(board[56] == '.'):
        if 48 in moves and len(moves) > 1: moves.remove(48)
        if 49 in moves and len(moves) > 1: moves.remove(49)
        if 57 in moves and len(moves) > 1: moves.remove(57)
    if(board[63] == '.'):
        if 55 in moves and len(moves) > 1: moves.remove(55)
        if 54 in moves and len(moves) > 1: moves.remove(54)
        if 62 in moves and len(moves) > 1: moves.remove(62)

def analyze_edges(board, moves, tkn):
    new_moves = set()

    edge1 = board[0:8]
    edge2 = board[0::8]
    edge3 = board[56:64]
    edge4 = board[7::8]

    if(board[0] == tkn):
        new_moves.add(edge1.find('.'))
        new_moves.add(edge2.find('.') * 8)
    if(board[7] == tkn):
        new_moves.add(edge1.rfind('.'))
        new_moves.add((edge4.find('.')*8) + 7)
    if(board[56] == tkn):
        new_moves.add(edge2.rfind('.') * 8)
        new_moves.add(edge3.find('.') + 56)
    if(board[63] == tkn):
        new_moves.add(edge3.rfind('.') + 56)
        new_moves.add((edge4.rfind('.')*8) + 7)

    return list(new_moves & set(moves))

def negamax(board, depth, color):
    moves = checkidx(board, 'X' if color == 1 else 'O')
    if(depth == 0 or board.count('X' if color == 1 else 'O') == 0 or board.count('.') == 0):
        return color*value(board), []
    if(len(moves) == 0):
        points, moveSeq = negamax(board, depth-1, -color)
        return -points, moveSeq
    points = float("-inf")
    moveSeq = []
    for idx0 in moves:
        new_board = move(board, 'X' if color == 1 else 'O', idx0, moves)
        currScore, currMoveSeq = negamax(new_board, depth-1, -color)
        currScore*=-1
        if(currScore > points):
            points = currScore
            moveSeq = currMoveSeq + [idx0]
    return points, moveSeq



def main():
    def_board = '.' * 27 + 'OX' + '.' * 6 + 'XO' + '.' * 27

    board = def_board

    tkn = ''

    idxs = []

    if(len(sys.argv) >= 2):
        if(len(sys.argv[1]) > 2):
            board = sys.argv[1].upper()
        elif(sys.argv[1].isdigit()):
            idxs.append(int(sys.argv[1]))
        elif(sys.argv[1][0] == '-'):
            pass
        elif(len(sys.argv[1]) == 2 and sys.argv[1][1].isdigit()):
            idxs.append(codetoidx(sys.argv[1].upper()))
        else:
            tkn = sys.argv[1].upper()
    if(len(sys.argv) >= 3):
        if(len(idxs) > 0 or tkn):
            for i in range(2, len(sys.argv)):
                if (sys.argv[i].isdigit()):
                    idxs.append(int(sys.argv[i]))
                elif(sys.argv[i][0] == '-'):
                    continue
                elif (len(sys.argv[i]) == 2 and sys.argv[i][1].isdigit()):
                    idxs.append(codetoidx(sys.argv[i].upper()))
        if(board != def_board):
            if (sys.argv[2].isdigit() or (len(sys.argv[2]) == 2 and sys.argv[2][1].isdigit())):
                for i in range(2, len(sys.argv)):
                    if (sys.argv[i].isdigit()):
                        idxs.append(int(sys.argv[i]))
                    elif(sys.argv[i][0] == '-'):
                        continue
                    elif (len(sys.argv[i]) == 2 and sys.argv[i][1].isdigit()):
                        idxs.append(codetoidx(sys.argv[i].upper()))
            else:
                tkn = sys.argv[2].upper()
                if(len(sys.argv) >= 4):
                    for i in range(3, len(sys.argv)):
                        if (sys.argv[i].isdigit()):
                            idxs.append(int(sys.argv[i]))
                        elif (sys.argv[i][0] == '-'):
                            continue
                        elif (len(sys.argv[i]) == 2 and sys.argv[i][1].isdigit()):
                            idxs.append(codetoidx(sys.argv[i].upper()))

    if not tkn:
        tkn = turn(board)

    moves = checkidx(board, tkn)

    '''if idx != -1 and ((idx not in moves['X'] and idx not in moves['O']) or (tkn == 'X' and idx not in moves['X']) or (tkn == 'O' and idx not in moves['O'])):
        print("Hey, Buster, you're actually bad!")
        exit(0)'''


    listOfMoves = list(moves.keys())

    print(listOfMoves)

    MAX_DEPTH = 20

    points, moveSeq = negamax(board, MAX_DEPTH, 1 if tkn == 'X' else -1)

    print("Score: {} Move Sequence: {}".format(points, moveSeq))


    '''edges = analyze_edges(board, listOfMoves, tkn)

    if len(moves.keys() & {0, 7, 56, 63}) > 0:
        print(choice(list(moves.keys() & {0, 7, 56, 63})))
    elif len(edges) > 0:
        print(choice(edges))
    else:
        remove_corners(listOfMoves, board)
        print(choice(listOfMoves))'''


if __name__ == '__main__':
    main()



