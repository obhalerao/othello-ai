import sys
from random import choice

class Strategy():

    movesCache = {}

    NEIGHBORS = [None for i in range(64)]

    CX_SQUARES = {1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62}

    holePos = set()

    MAX_DEPTH = 20

    WEIGHTS = [620, -120, 20, 5, 5, 20, -120, 620,
               -120, -140, -5, -5, -5, -5, -140, -120,
               20, -5, 15, 3, 3, 15, -5, 20,
               5, -5, 3, 3, 3, 3, -5, 5,
               5, -5, 3, 3, 3, 3, -5, 5,
               20, -5, 15, 3, 3, 15, -5, 20,
               -120, -140, -5, -5, -5, -5, -140, -120,
               620, -120, 20, 5, 5, 20, -120, 620]

    def __init__(self):
        self.gen_neighbors()

    def gen_neighbors(self):
        for val in range(64):
            nbrs = set()
            x = val // 8
            y = val % 8
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (8 * (x + i) + y + j >= 0 and 8 * (x + i) + y + j < 64): nbrs.add(8 * (x + i) + y + j)
            nbrs.remove(val)
            self.NEIGHBORS[val] = nbrs.copy()

    def display(self, board, moves):
        listBoard = list(board)
        for i in moves:
            listBoard[i] = '*'
        newBoard = ''.join(listBoard)
        for i in range(0, 64, 8):
            print(newBoard[i:i+8])

    def score(self, board):
        return str(board.count('X')) + "/" + str(board.count('O'))

    def value(self, board):
        return board.count('X') - board.count('O')

    def checkidx(self, boards, tkn):
        if (boards, tkn) in self.movesCache: return self.movesCache[(boards, tkn)]
        idxs = {}
        board = [list(boards[i:i + 8]) for i in range(0, 64, 8)]
        for idx in self.holePos:
            idxSet = set()
            if boards[idx] != '.': continue
            x = idx // 8
            y = idx % 8
            i = x+1
            currSet = set()
            while(i < 8):
                if(board[i][y] != tkn): currSet.add((i*8)+y)
                if(board[i][y] == '.'): break
                if(board[i][y] == tkn and i != x+1):
                    idxSet = idxSet | currSet
                    break
                elif(board[i][y] == tkn):
                    break
                i+=1
            i = x-1
            currSet = set()
            while (i >= 0):
                if (board[i][y] != tkn): currSet.add((i * 8) + y)
                if (board[i][y] == '.'): break
                if (board[i][y] == tkn and i != x-1):
                    idxSet = idxSet | currSet
                    break
                elif(board[i][y] == tkn):
                    break
                i -= 1
            j = y + 1
            currSet = set()
            while (j < 8):
                if (board[x][j] != tkn): currSet.add((x * 8) + j)
                if (board[x][j] == '.'): break
                if (board[x][j] == tkn and j != y+1):
                    idxSet = idxSet | currSet
                    break
                elif(board[x][j] == tkn):
                    break
                j += 1
            j = y - 1
            currSet = set()
            while (j >= 0):
                if (board[x][j] != tkn): currSet.add((x * 8) + j)
                if (board[x][j] == '.'): break
                if (board[x][j] == tkn and j != y-1):
                    idxSet = idxSet | currSet
                    break
                elif(board[x][j] == tkn):
                    break
                j -= 1
            k = 1
            currSet = set()
            while(x+k < 8 and y+k < 8):
                if (board[x+k][y+k] != tkn): currSet.add(((x+k) * 8) + y+k)
                if (board[x+k][y+k] == '.'): break
                if(board[x+k][y+k] == tkn and k != 1):
                    idxSet = idxSet | currSet
                    break
                elif(board[x+k][y+k] == tkn):
                    break
                k+=1
            k = 1
            currSet = set()
            while (x - k >= 0 and y - k >= 0):
                if (board[x-k][y-k] != tkn): currSet.add(((x-k) * 8) + y-k)
                if (board[x - k][y - k] == '.'): break
                if (board[x - k][y - k] == tkn and k != 1):
                    idxSet = idxSet | currSet
                    break
                elif(board[x-k][y-k] == tkn):
                    break
                k += 1
            k = 1
            currSet = set()
            while (x + k < 8 and y - k >= 0):
                if (board[x+k][y-k] != tkn): currSet.add(((x+k) * 8) + y-k)
                if (board[x + k][y - k] == '.'): break
                if (board[x + k][y - k] == tkn and k != 1):
                    idxSet = idxSet | currSet
                    break
                elif(board[x+k][y-k] == tkn):
                    break
                k += 1
            k = 1
            currSet = set()
            while (x - k >= 0 and y + k < 8):
                if (board[x-k][y+k] != tkn): currSet.add(((x-k) * 8) + y+k)
                if (board[x - k][y + k] == '.'): break
                if (board[x - k][y + k] == tkn and k != 1):
                    idxSet = idxSet | currSet
                    break
                elif(board[x-k][y+k] == tkn):
                    break
                k+=1
            if(len(idxSet) > 0):
                idxs[idx] = idxSet | set([idx])
        self.movesCache[(boards, tkn)] = {idx: idxs[idx].copy() for idx in idxs}
        return idxs

    def move(self, boards, tkn, moves):
        board = list(boards)
        for move in moves:
            board[move] = tkn
        return ''.join(board)

    def turn(self, board):
        if (board.count('X') + board.count('O')) % 2 == 0:
            return 'X'
        else:
            return 'O'

    def coin_parity(self, board, color):
        return color * 100 * ((board.count('X') - board.count('O')) / (board.count('X') + board.count('O')))

    def corners(self, board, color, xs, os):
        xmoves = set()
        omoves = set()
        for idx, i in enumerate(board):
            if i == 'X': xmoves.add(idx)
            if i == 'O': omoves.add(idx)
        xval = 5000 * len(xmoves & {0, 7, 56, 63}) + 30 * len(xs & {0, 7, 56, 63}) - 3000 * len(xs & self.CX_SQUARES)
        oval = 5000 * len(omoves & {0, 7, 56, 63}) + 30 * len(os & {0, 7, 56, 63}) - 3000 * len(os & self.CX_SQUARES)

        if (xval + oval == 0): return 0
        return color * 100 * (xval - oval) / (xval + oval)

    def weighted_score(self, board, color):
        xscore = 0
        oscore = 0

        for idx, i in enumerate(board):
            if (i == 'X'): xscore += self.WEIGHTS[idx]
            if (i == 'O'): oscore += self.WEIGHTS[idx]

        return color * (xscore - oscore)

    def stability(self, board, color):
        xstable = set()
        ostable = set()

        if (board[0] != '.'):
            currTkn = board[0]
            currSet = {0}
            for i in range(1, 8):
                edges = 0
                done = True
                x = 0
                y = i
                for j in range(i):
                    if board[8 * x + y] == currTkn and len(self.NEIGHBORS[8 * x + y] & currSet) > 1:
                        done = False
                        currSet.add(8 * x + y)
                    x += 1
                    y -= 1
                if done: break
            if currTkn == 'X':
                xstable = xstable | currSet
            else:
                ostable = ostable | currSet

        if (board[7] != '.'):
            currTkn = board[7]
            currSet = {7}
            for i in range(1, 8):
                edges = 0
                done = True
                x = 0
                y = 8 - i
                for j in range(i):
                    if board[8 * x + y] == currTkn and len(self.NEIGHBORS[8 * x + y] & currSet) > 1:
                        done = False
                        currSet.add(8 * x + y)
                    x += 1
                    y += 1
                if done: break
            if currTkn == 'X':
                xstable = xstable | currSet
            else:
                ostable = ostable | currSet

        if (board[56] != '.'):
            currTkn = board[56]
            currSet = {56}
            for i in range(1, 8):
                edges = 0
                done = True
                x = 7
                y = i
                for j in range(i):
                    if board[8 * x + y] == currTkn and len(self.NEIGHBORS[8 * x + y] & currSet) > 1:
                        done = False
                        currSet.add(8 * x + y)
                    x -= 1
                    y -= 1
                if done: break
            if currTkn == 'X':
                xstable = xstable | currSet
            else:
                ostable = ostable | currSet

        if (board[63] != '.'):
            currTkn = board[63]
            currSet = {63}
            for i in range(1, 8):
                edges = 0
                done = True
                x = 7
                y = 8 - i
                for j in range(i):
                    if board[8 * x + y] == currTkn and len(self.NEIGHBORS[8 * x + y] & currSet) > 1:
                        done = False
                        currSet.add(8 * x + y)
                    x -= 1
                    y += 1
                if done: break
            if currTkn == 'X':
                xstable = xstable | currSet
            else:
                ostable = ostable | currSet

        return len(xstable), len(ostable)

    def mobility(self, board, color):
        xmoves = set()
        omoves = set()
        for idx, i in enumerate(board):
            if (i == 'X'):
                for x in self.NEIGHBORS[idx]:
                    if(board[x] == '.'): omoves.add(x)
            elif (i == 'O'):
                for x in self.NEIGHBORS[idx]:
                    if(board[x] == '.'): xmoves.add(x)
       # if (len(xmoves) + len(omoves) == 0): return 0
        return len(xmoves), len(omoves)

    def heuristicOld(self, board, color, moves):
        xmoves = None
        omoves = None
        if color == 1:
            xmoves = moves
            omoves = self.checkidx(board, 'O').keys()
        else:
            omoves = moves
            xmoves = self.checkidx(board, 'X').keys()
        cp = self.coin_parity(board, color)
        cr = self.corners(board, color, xmoves, omoves)
        s_raw = self.stability(board, color)
        if(sum(s_raw) == 0): s = 0
        else: s = 100 * (s_raw[0] - s_raw[1]) / sum(s_raw)
        m = self.mobility(board, color)
        return (80 * cr + 25 * cp + 25 * s + 5 * m) / 135


    def heuristic(self, board, color, mvs):
        xmoves = set()
        omoves = set()
        for idx, i in enumerate(board):
            if i == 'X': xmoves.add(idx)
            if i == 'O': omoves.add(idx)
        scores = [0, 0]
        scores[0] += 1000*len(xmoves & {0, 7, 56, 63})
        scores[1] += 1000*len(omoves & {0, 7, 56, 63})
        for idx, moves in enumerate([xmoves, omoves]):
            if (board[0] == '.'):
                if 1 in moves and len(moves) > 1: scores[idx] -= 5000
                if 8 in moves and len(moves) > 1: scores[idx] -= 5000
                if 9 in moves and len(moves) > 1: scores[idx] -= 5000
            if (board[7] == '.'):
                if 6 in moves and len(moves) > 1: scores[idx] -= 5000
                if 15 in moves and len(moves) > 1: scores[idx] -= 5000
                if 14 in moves and len(moves) > 1: scores[idx] -= 5000
            if (board[56] == '.'):
                if 48 in moves and len(moves) > 1: scores[idx] -= 5000
                if 49 in moves and len(moves) > 1: scores[idx] -= 5000
                if 57 in moves and len(moves) > 1: scores[idx] -= 5000
            if (board[63] == '.'):
                if 55 in moves and len(moves) > 1: scores[idx] -= 5000
                if 54 in moves and len(moves) > 1: scores[idx] -= 5000
                if 62 in moves and len(moves) > 1: scores[idx] -= 5000
        mob = self.mobility(board, color)
        scores[0] += 5*mob[0]
        scores[1] += 5*mob[1]


        return color*(scores[0]-scores[1])

    def remove_corners(self, moves, board):
        if (board[0] == '.'):
            if 1 in moves and len(moves) > 1: moves.remove(1)
            if 8 in moves and len(moves) > 1: moves.remove(8)
            if 9 in moves and len(moves) > 1: moves.remove(9)
        if (board[7] == '.'):
            if 6 in moves and len(moves) > 1: moves.remove(6)
            if 15 in moves and len(moves) > 1: moves.remove(15)
            if 14 in moves and len(moves) > 1: moves.remove(14)
        if (board[56] == '.'):
            if 48 in moves and len(moves) > 1: moves.remove(48)
            if 49 in moves and len(moves) > 1: moves.remove(49)
            if 57 in moves and len(moves) > 1: moves.remove(57)
        if (board[63] == '.'):
            if 55 in moves and len(moves) > 1: moves.remove(55)
            if 54 in moves and len(moves) > 1: moves.remove(54)
            if 62 in moves and len(moves) > 1: moves.remove(62)

    def analyze_edges(self, board, moves, tkn):
        new_moves = set()

        edge1 = board[0:8]
        edge2 = board[0::8]
        edge3 = board[56:64]
        edge4 = board[7::8]

        if (board[0] == tkn):
            new_moves.add(edge1.find('.'))
            new_moves.add(edge2.find('.') * 8)
        if (board[7] == tkn):
            new_moves.add(edge1.rfind('.'))
            new_moves.add((edge4.find('.') * 8) + 7)
        if (board[56] == tkn):
            new_moves.add(edge2.rfind('.') * 8)
            new_moves.add(edge3.find('.') + 56)
        if (board[63] == tkn):
            new_moves.add(edge3.rfind('.') + 56)
            new_moves.add((edge4.rfind('.') * 8) + 7)

        return list(new_moves & set(moves))

    def alphabeta(self, board, depth, alpha, beta, color):
        moves = self.checkidx(board, 'X' if color == 1 else 'O')

        if (len(moves) == 0):
            nmoves = self.checkidx(board, 'O' if color == 1 else 'X')
            if (len(nmoves) == 0):
                return [color * self.value(board)]
            ab = self.alphabeta(board, depth - 1, -beta, -alpha, -color)
            return [-ab[0]] + ab[1:] + [-1]

        if (depth == 0):
            return [self.heuristic(board, color, moves.keys())]

        if (len(moves) == 1 and board.count('.') == 1):
            for idx0 in moves:
                nb = self.move(board, 'X' if color == 1 else 'O', moves[idx0])
                return [color * self.value(nb), idx0]

        points = [-float("inf")]

        orderedMoves = list(moves.keys() & {0, 7, 56, 63}) + list(moves.keys() - {0, 7, 56, 63})

        for idx0 in orderedMoves:
            new_board = self.move(board, 'X' if color == 1 else 'O', moves[idx0])
            self.holePos.remove(idx0)
            ab = self.alphabeta(new_board, depth - 1, -beta, -alpha, -color)
            self.holePos.add(idx0)
            currScore = -ab[0]
            if currScore > beta: return [currScore]
            if currScore < alpha: continue
            points = [currScore] + ab[1:] + [idx0]
            if (depth == self.MAX_DEPTH): print("Score: {} Move Sequence: {}".format(points[0], points[1:]))
            alpha = currScore + 1

        return points

    def final_code(self, board, tkn, best_move):

        bm = 0

        for idx, i in enumerate(board):
            if i == '.':
                self.holePos.add(idx)

        moves = self.checkidx(board, tkn)

        listOfMoves = list(moves.keys())

        edges = self.analyze_edges(board, listOfMoves, tkn)

        if len(moves.keys() & {0, 7, 56, 63}) > 0:
            best_move.value = self.convert_move((choice(list(moves.keys() & {0, 7, 56, 63}))))
        elif len(edges) > 0:
            best_move.value = self.convert_move((choice(edges)))
        else:
            self.remove_corners(listOfMoves, board)
            best_move.value = self.convert_move((choice(listOfMoves)))

        if(board.count('.') < 12): bm = self.alphabeta(board, self.MAX_DEPTH, float("-inf"), float("inf"), 1 if tkn == 'X' else -1)[-1]
        else: bm = self.alphabeta(board, 3, float("-inf"), float("inf"), 1 if tkn == 'X' else -1)[-1]

        return bm

    def convert_move(self, move):
        return move + 11 + 2*(move // 8)


    def best_strategy(self, board, player, best_move, still_running):
        nb = board.replace('?', '').replace('@', 'X').upper()
        bm = self.final_code(nb, 'X' if player == '@' else 'O', best_move)
        best_move.value = self.convert_move(bm)


def codetoidx(code):
    return (int(code[1])-1)*8 + (ord(code[0]) - ord('A'))





def main():
    global holePos, MAX_DEPTH
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

    s = Strategy()

    if not tkn:
        tkn = s.turn(board)

    for idx, i in enumerate(board):
        if i == '.':
            s.holePos.add(idx)

    moves = s.checkidx(board, tkn)

    '''if idx != -1 and ((idx not in moves['X'] and idx not in moves['O']) or (tkn == 'X' and idx not in moves['X']) or (tkn == 'O' and idx not in moves['O'])):
        print("Hey, Buster, you're actually bad!")
        exit(0)'''


    listOfMoves = list(moves.keys())

    print(listOfMoves)

    if(board.count('.') < 12): MAX_DEPTH = 20

    points = s.alphabeta(board, s.MAX_DEPTH, float("-inf"), float("inf"), 1 if tkn == 'X' else -1)

    print("Score: {} Move Sequence: {}".format(points[0], points[1:]))

    '''else:
        edges = analyze_edges(board, listOfMoves, tkn)

        if len(moves.keys() & {0, 7, 56, 63}) > 0:
            print(choice(list(moves.keys() & {0, 7, 56, 63})))
        elif len(edges) > 0:
            print(choice(edges))
        else:
            remove_corners(listOfMoves, board)
            print(choice(listOfMoves))'''

if __name__ == '__main__':
    main()



