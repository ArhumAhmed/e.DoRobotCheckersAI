'''

testing
'''


from DraughtsBrain import DraughtsBrain
from DBoard import DBoard
from DPiece import DPiece
from DAction import DAction
import math

def RunAI(inputBoard, color):
    AI = DraughtsBrain({'PIECE':  15,
                        'KING':   30,
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 8)
    if color == 1:
        AI.turn = 'LIGHT'
    elif color == 0:
        AI.turn = 'DARK'
    # inputBoard = [0, 1, 0, 1, 0, 1, 0, 1, #
                   # 1, 0, 1, 0, 1, 0, 1, 0,
                   # 0, 1, 0, 1, 0, 1, 0, 1,
                   # 0, 0, 0, 0, 0, 0, 0, 0,
                   # 0, 0, 0, 0, 0, 0, 0, 0,
                   # -1, 0, -1, 0, -1, 0, -1, 0,
                   # 0, -1, 0, -1, 0, -1, 0, -1,
                   # -1, 0, -1, 0, -1, 0, -1, 0]

    for i in range(64):
        if inputBoard[i] != 0:
            if inputBoard[i] == 1:
                new_piece = DPiece(AI.board, int(math.floor(i/8)), i % 8, 'DARK')
                AI.board.dark_pieces.append(new_piece)
                AI.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoard[i] == -1:
                new_piece = DPiece(AI.board, int(math.floor(i/8)), i % 8, 'LIGHT')
                AI.board.light_pieces.append(new_piece)
                AI.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoard[i] == 2:
                new_piece = DPiece(AI.board, int(math.floor(i/8)), i % 8, 'DARK')
                new_piece.is_king = True
                AI.board.dark_pieces.append(new_piece)
                AI.board.set_bitmap(int(i/8), i % 8, new_piece)
            elif inputBoard[i] == -2:
                new_piece = DPiece(AI.board, int(math.floor(i / 8)), i % 8, 'LIGHT')
                new_piece.is_king = True
                AI.board.light_pieces.append(new_piece)
                AI.board.set_bitmap(int(i / 8), i % 8, new_piece)

    move = DraughtsBrain.best_move(AI)
    moveFrom = move.getSource()
    moveFromIndex = moveFrom[0] + (moveFrom[1] * 8)
    moveTo = move.getDestination()
    moveToIndex = moveTo[0] + (moveTo[1] * 8)
    moveJumps = move.getCapture()
    moveJumpsIndex = []
    if moveJumps != None:
        for i in moveJumps/2:
            moveJumpsIndex[i] = moveJumps[0] + (moveJumps[1] * 8)
    print(AI.board)
    return moveFromIndex, moveToIndex, moveJumpsIndex
    # print(moveJumps)
    # print(move.getSource(), ' to ', move.getDestination())
    # print(moveFromIndex, ' to ', moveToIndex)
    # AI.apply_action(move)

def legalBoardState(inputBoard2):
    AI2 = DraughtsBrain({'PIECE':  15,
                        'KING':   30,
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 3)
    AI2.turn = 'DARK'
    inputBoard2 = [0, 1, 0, 1, 0, 1, 0, 1, # comment out when actual imput is coming
              1, 0, 1, 0, 1, 0, 1, 0,
              0, 1, 0, 1, 0, 1, 0, 1,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              -1, 0, -1, 0, -1, 0, -1, 0,
              0, -1, 0, -1, 0, -1, 0, -1,
              -1, 0, -1, 0, -1, 0, -1, 0]
    for i in range(64):
        if math.floor(int(i/8)) % 2 == 0:
            if (i % 8) % 2 == 0:
                if inputBoard2[i] != 0:
                    return False
        else:
            if (i % 8) & 2 == 1:
                if inputBoard2[i] !=0:
                    return False
    return True

def isValidMove(inputBoardOld, inputBoardNew):
    AI3 = DraughtsBrain({'PIECE':  15,
                        'KING':   30,
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 3)
    AI3.turn = 'LIGHT'
    AI4 = DraughtsBrain({'PIECE':  15,
                        'KING':   30,
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 3)
    AI4.turn = 'LIGHT'

    for i in range(64):
        if inputBoardNew[i] != 0:
            if inputBoardNew[i] == 1:
                new_piece = DPiece(AI3.board, int(math.floor(i/8)), i % 8, 'DARK')
                AI3.board.dark_pieces.append(new_piece)
                AI3.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoardNew[i] == -1:
                new_piece = DPiece(AI3.board, int(math.floor(i/8)), i % 8, 'LIGHT')
                AI3.board.light_pieces.append(new_piece)
                AI3.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoardNew[i] == 2:
                new_piece = DPiece(AI3.board, int(math.floor(i/8)), i % 8, 'DARK')
                new_piece.is_king = True
                AI3.board.dark_pieces.append(new_piece)
                AI3.board.set_bitmap(int(i/8), i % 8, new_piece)
            elif inputBoardNew[i] == -2:
                new_piece = DPiece(AI3.board, int(math.floor(i / 8)), i % 8, 'LIGHT')
                new_piece.is_king = True
                AI3.board.light_pieces.append(new_piece)
                AI3.board.set_bitmap(int(i / 8), i % 8, new_piece)
    for i in range(64):
        if inputBoardOld[i] != 0:
            if inputBoardOld[i] == 1:
                new_piece = DPiece(AI4.board, int(math.floor(i/8)), i % 8, 'DARK')
                AI4.board.dark_pieces.append(new_piece)
                AI4.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoardOld[i] == -1:
                new_piece = DPiece(AI4.board, int(math.floor(i/8)), i % 8, 'LIGHT')
                AI4.board.light_pieces.append(new_piece)
                AI4.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoardOld[i] == 2:
                new_piece = DPiece(AI4.board, int(math.floor(i/8)), i % 8, 'DARK')
                new_piece.is_king = True
                AI4.board.dark_pieces.append(new_piece)
                AI4.board.set_bitmap(int(i/8), i % 8, new_piece)
            elif inputBoardOld[i] == -2:
                new_piece = DPiece(AI4.board, int(math.floor(i / 8)), i % 8, 'LIGHT')
                new_piece.is_king = True
                AI4.board.light_pieces.append(new_piece)
                AI4.board.set_bitmap(int(i / 8), i % 8, new_piece)
    possibleMoves = AI4.board.all_move('LIGHT')
    print("AI3 \n" + AI3.board.__str__())
    for i in possibleMoves:
        AI4.board.apply_action(i)  # Can also do AI4.apply_action(i) May causeDiff results during end game/piece capture
        ai3State=AI3.board.__str__()
        ai4State=AI4.board.__str__()
        print("AI4 \n" + AI4.board.__str__())
        if ai3State == ai4State:
            return True
        AI4.board.undo_last()
    return False

BoardOld = [1, 1, 0, 1, 0, 1, 0, 1, # comment out when actual input is coming
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 -1, 0, -1, 0, -1, 0, -1, 0,
                 0, -1, 0, -1, 0, -1, 0, -1,
                 -1, 0, -1, 0, -1, 0, -1, 0]

BoardNew = [0, 1, 0, 1, 0, 1, 0, 1, # comment out when actual input is coming
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, -1, 0, 0, 0, 0, 0, 0,
                 0, 0, -1, 0, -1, 0, -1, 0,
                 0, -1, 0, -1, 0, -1, 0, -1,
                 -1, 0, -1, 0, -1, 0, -1, 0]

# output = RunAI(BoardOld, 1)
# print(output)
test = isValidMove(BoardOld, BoardNew)
print(test)
