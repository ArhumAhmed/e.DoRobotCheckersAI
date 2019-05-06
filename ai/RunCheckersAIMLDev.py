'''

testing
'''


from .DraughtsBrain import DraughtsBrain
from .DBoard import DBoard
from .DPiece import DPiece
from .DAction import DAction
import math
import random

def RunAI(inputBoard32):
    
    # Initializes AI object with default heuristic values and minimax weight
    AI = DraughtsBrain({'PIECE':  30,  # piece
                        'KING':   15,  # king
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 5)

    AI.turn = 'Dark'

    # Converts 32 size array to 64 (adds empty spots)
    inputBoard = []
    for i in range(32):
        if (i // 4) % 2 == 0:
            inputBoard.append(0)
            inputBoard.append(inputBoard32[i])
        else:
            inputBoard.append(inputBoard32[i])
            inputBoard.append(0)
    
    # Extracts board state array and creates board in AI.board object
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
    
    # Computes the best move
    move = DraughtsBrain.best_move(AI)
    moveFrom = move.getSource()
    moveFromIndex = moveFrom[0] + (moveFrom[1] * 8)
    moveTo = move.getDestination()
    # In the case of multijumps, loop through move and store last destination
    originalMove = move
    while move.next != None:
        moveTo = move.next.getDestination()
        move = move.next
    move = originalMove
    moveToIndex = moveTo[0] + (moveTo[1] * 8)
    moveJumps = move.getCapture()
    moveJumpsIndex = []
    # In the case of multijump, loop through each jumped piece and add to array
    if moveJumps != None:
        for i in range(1):
            moveJumpsIndex.append(moveJumps[i] + (moveJumps[i + 1] * 8))
        while move.next != None:
            moveJumps = move.next.getCapture()
            move = move.next
            for i in range(1):
                moveJumpsIndex.append(moveJumps[i] + (moveJumps[i + 1] * 8))
    move = originalMove
    AI.apply_action(move)
    print(AI.board)
    winner = AI.turn
    done = AI.gameover

    moveFromIndex = moveFromIndex // 2
    moveToIndex = moveToIndex // 2
    # Do not calculate jumpedindex if no pieces jumped
    if moveJumpsIndex != None:
        for i in range(len(moveJumpsIndex)):
            moveJumpsIndex[i] = moveJumpsIndex[i] // 2

    return moveFromIndex, moveToIndex, moveJumpsIndex

def isValidMove(inputBoardOld32, inputBoardNew32):
    # Convert 32 size board state array of previous state to 64 size
    inputBoardOld = []
    for i in range(32):
        if (i // 4) % 2 == 0:
            inputBoardOld.append(0)
            inputBoardOld.append(inputBoardOld32[i])
        else:
            inputBoardOld.append(inputBoardOld32[i])
            inputBoardOld.append(0)
            
    # Convert 32 size board state array of current state to 64 size
    inputBoardNew = []
    for i in range(32):
        if (i // 4) % 2 == 0:
            inputBoardNew.append(0)
            inputBoardNew.append(inputBoardNew32[i])
        else:
            inputBoardNew.append(inputBoardNew32[i])
            inputBoardNew.append(0)
    
    # Initialize 2 AI objects to compare board states
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
    
    # Extract the board state array of current board state into AI3 object
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
                
    # Extract the board state array of previous board state into AI4 object
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
    
    # Compute all valid moves from previous board state
    possibleMoves = AI4.board.all_move('LIGHT')
    # Loop through all possible moves and apply them to AI4 object board. If
    # that board state matches with current board state, return true
    for i in possibleMoves:
        AI4.board.apply_action(i)  # Can also do AI4.apply_action(i) May causeDiff results during end game/piece capture
        ai3State=AI3.board.__str__()
        ai4State=AI4.board.__str__()
        if ai3State == ai4State:
            return True
        AI4.board.undo_last() # Undo the move to return to original board state
    return False

def isGameOver(inputBoard32, color):
    
    # Initialize AI object with default heuristics and minimax weight
    AI7 = DraughtsBrain({'PIECE':  30,  # piece
                        'KING':   15,  # king
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 5)

    if color == 'Dark':
      AI7.turn = 'Dark'
    else:
      AI7.turn = 'Light'
    
    # Converts 32 size board state array into 64 size board state array
    inputBoard = []
    for i in range(32):
        if (i // 4) % 2 == 0:
            inputBoard.append(0)
            inputBoard.append(inputBoard32[i])
        else:
            inputBoard.append(inputBoard32[i])
            inputBoard.append(0)
    
    # Extract the board state array into AI7 object
    for i in range(64):
        if inputBoard[i] != 0:
            if inputBoard[i] == 1:
                new_piece = DPiece(AI7.board, int(math.floor(i/8)), i % 8, 'DARK')
                AI7.board.dark_pieces.append(new_piece)
                AI7.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoard[i] == -1:
                new_piece = DPiece(AI7.board, int(math.floor(i/8)), i % 8, 'LIGHT')
                AI7.board.light_pieces.append(new_piece)
                AI7.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoard[i] == 2:
                new_piece = DPiece(AI7.board, int(math.floor(i/8)), i % 8, 'DARK')
                new_piece.is_king = True
                AI7.board.dark_pieces.append(new_piece)
                AI7.board.set_bitmap(int(i/8), i % 8, new_piece)
            elif inputBoard[i] == -2:
                new_piece = DPiece(AI7.board, int(math.floor(i / 8)), i % 8, 'LIGHT')
                new_piece.is_king = True
                AI7.board.light_pieces.append(new_piece)
                AI7.board.set_bitmap(int(i / 8), i % 8, new_piece)

    # Compute the best move
    move = DraughtsBrain.best_move(AI7)
    # If there is no best move, there are no valid moves and game is over
    if move == None:
      return True

    white = True
    black = True
    # Search if there is atleast 1 white piece
    for i in range(32):
      if inputBoard32[i] == 1 or inputBoard32[i] == 2:
        white = False
        break
    # Search if there is atleast 1 black piece
    for i in range(32):
      if inputBoard32[i] == -1 or inputBoard32[i] == -2:
        black = False
        break
    
    if white == False and black == False:
      return False
    else:
      return True

def printBoard(inputBoard32):
    
    # Initializes AI8 object with default heuristic and minimax weight
    AI8 = DraughtsBrain({'PIECE':  30,  # piece
                        'KING':   15,  # king
                        'BACK':   3,
                        'KBACK':  3,
                        'CENTER': 6,
                        'KCENTER': 7,
                        'FRONT':  6,
                        'KFRONT': 3,
                        'MOB':    6}, 5)
    
    # Convert 32 size board state array into 64 size board state array
    inputBoard = []
    for i in range(32):
        if (i // 4) % 2 == 0:
            inputBoard.append(0)
            inputBoard.append(inputBoard32[i])
        else:
            inputBoard.append(inputBoard32[i])
            inputBoard.append(0)

    # Extract board state array into AI8 object board
    for i in range(64):
        if inputBoard[i] != 0:
            if inputBoard[i] == 1:
                new_piece = DPiece(AI8.board, int(math.floor(i/8)), i % 8, 'DARK')
                AI8.board.dark_pieces.append(new_piece)
                AI8.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoard[i] == -1:
                new_piece = DPiece(AI8.board, int(math.floor(i/8)), i % 8, 'LIGHT')
                AI8.board.light_pieces.append(new_piece)
                AI8.board.set_bitmap(math.floor(int(i/8)), i % 8, new_piece)
            elif inputBoard[i] == 2:
                new_piece = DPiece(AI8.board, int(math.floor(i/8)), i % 8, 'DARK')
                new_piece.is_king = True
                AI8.board.dark_pieces.append(new_piece)
                AI8.board.set_bitmap(int(i/8), i % 8, new_piece)
            elif inputBoard[i] == -2:
                new_piece = DPiece(AI8.board, int(math.floor(i / 8)), i % 8, 'LIGHT')
                new_piece.is_king = True
                AI8.board.light_pieces.append(new_piece)
                AI8.board.set_bitmap(int(i / 8), i % 8, new_piece)

    # Print the board state of the AI8 object
    print(AI8.board)
