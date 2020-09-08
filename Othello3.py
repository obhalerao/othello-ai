import sys



def display(board, moves):
    listBoard = list(board)
    for i in moves:
        listBoard[i] = '*'
    newBoard = ''.join(listBoard)
    for i in range(0, 64, 8):
        print(newBoard[i:i+8])

def score(board):
    return str(board.count('X')) + "/" + str(board.count('O'))

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

    moves = {'X': checkidx(board, 'X'), 'O': checkidx(board, 'O')}

    '''if idx != -1 and ((idx not in moves['X'] and idx not in moves['O']) or (tkn == 'X' and idx not in moves['X']) or (tkn == 'O' and idx not in moves['O'])):
        print("Hey, Buster, you're actually bad!")
        exit(0)'''

    if not tkn:
        tkn = turn(board)

    display(board, list(moves[tkn].keys()))
    print(board + " " + score(board))

    if len(moves[tkn]) == 0: tkn = 'O' if tkn == 'X' else 'X'

    if(len(moves[tkn]) == 0):
        print("No moves possible.")
    else:
        print("Possible moves for {}: {}".format(tkn, list(moves[tkn].keys())))

    for idx in idxs:
        print('{} moves to {}'.format(tkn, idx))
        board = move(board, tkn, idx, moves[tkn])
        moves = {'X': checkidx(board, 'X'), 'O': checkidx(board, 'O')}
        tkn = 'O' if tkn == 'X' else 'X'
        if len(moves[tkn]) == 0: tkn = 'O' if tkn == 'X' else 'X'
        display(board, list(moves[tkn].keys()))
        print(board + " " + score(board))

        if len(moves[tkn]) == 0:
            print("No moves possible.")
        else:
            print("Possible moves for {}: {}".format(tkn, list(moves[tkn].keys())))






if __name__ == '__main__':
    main()



