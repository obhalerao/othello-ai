import sys

idxs = []

def checkidx(boards, idx, tkn):
    global idxs
    if boards[idx] != '.': return
    board = [list(boards[i:i+8]) for i in range(0, 64, 8)]
    x = idx // 8
    y = idx % 8
    i = x+1
    while(i < 8):
        if(board[i][y] == '.'): break
        if(board[i][y] == tkn and i != x+1):
            idxs.append(idx)
            return
        elif(board[i][y] == tkn):
            break
        i+=1
    i = x-1
    while (i >= 0):
        if (board[i][y] == '.'): break
        if (board[i][y] == tkn and i != x-1):
            idxs.append(idx)
            return
        elif(board[i][y] == tkn):
            break
        i -= 1
    j = y + 1
    while (j < 8):
        if (board[x][j] == '.'): break
        if (board[x][j] == tkn and j != y+1):
            idxs.append(idx)
            return
        elif(board[x][j] == tkn):
            break
        j += 1
    j = y - 1
    while (j >= 0):
        if (board[x][j] == '.'): break
        if (board[x][j] == tkn and j != y-1):
            idxs.append(idx)
            return
        elif(board[x][j] == tkn):
            break
        j -= 1
    k = 1
    while(x+k < 8 and y+k < 8):
        if (board[x+k][y+k] == '.'): break
        if(board[x+k][y+k] == tkn and k != 1):
            idxs.append(idx)
            return
        elif(board[x+k][y+k] == tkn):
            break
        k+=1
    k = 1
    while (x - k >= 0 and y - k >= 0):
        if (board[x - k][y - k] == '.'): break
        if (board[x - k][y - k] == tkn and k != 1):
            idxs.append(idx)
            return
        elif(board[x-k][y-k] == tkn):
            break
        k += 1
    k = 1
    while (x + k < 8 and y - k >= 0):
        if (board[x + k][y - k] == '.'): break
        if (board[x + k][y - k] == tkn and k != 1):
            idxs.append(idx)
            return
        elif(board[x+k][y-k] == tkn):
            break
        k += 1
    k = 1
    while (x - k >= 0 and y + k < 8):
        if (board[x - k][y + k] == '.'): break
        if (board[x - k][y + k] == tkn and k != 1):
            idxs.append(idx)
            return
        elif(board[x-k][y+k] == tkn):
            break
        k += 1

def main():
    global idxs

    board = '.' * 27 + 'OX' + '.' * 6 + 'XO' + '.' * 27

    tkn = ''

    if(len(sys.argv) > 1 and len(sys.argv) < 3):
        if(len(sys.argv[1]) > 1):
            board = sys.argv[1].upper()
        else:
            tkn = sys.argv[1].upper()

    elif(len(sys.argv) > 2):
        board = sys.argv[1].upper()
        tkn =  sys.argv[2].upper()

    if not tkn:
        if(board.count('X') + board.count('O')) % 2 == 0: tkn = 'X'
        else: tkn = 'O'

    newBoard = list(board)
    for i in range(64):
        checkidx(board, i, tkn)
    for i in idxs:
        newBoard[i] = '*'

    for i in range(0, 64, 8):
        print(''.join(newBoard[i:i+8]))

    if (len(idxs) > 0):
        print(idxs)
    else:
        print("No moves possible.")



if __name__ == '__main__':
    main()



