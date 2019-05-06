from object_detection.detection import *
from ai.RunCheckersAIMLDev import *
from manipulation.manipulationWQueue import *
import cv2
import subprocess
import sys
import time

def calculate_move(squares_center, piece_to_move, square_to_move_to):
  distance_in_pixels_in_y = abs(squares_center[0][0] - squares_center[3][0]) # distance of horizontal board
  distance_in_pixels_in_x = abs(squares_center[3][1] - squares_center[27][1]) # distance of vertical board
  mm_per_pixels_y = 234 / distance_in_pixels_in_y
  mm_per_pixels_x = 234 / distance_in_pixels_in_x

  piece_to_move_x_pixels = abs(squares_center[3][1] - piece_to_move[1])   # piece_to_move[1]distance in pixels from 3rd black square
  piece_to_move_y_pixels = abs(squares_center[3][0] - piece_to_move[0])

  piece_to_move_y_mm = piece_to_move_y_pixels * mm_per_pixels_y      # distance convert to mm
  piece_to_move_x_mm = piece_to_move_x_pixels * mm_per_pixels_x

  piece_to_move_y_mm = 142 - int(piece_to_move_y_mm)
  piece_to_move_x_mm = 351 + int(piece_to_move_x_mm)


  square_to_move_to_x_pixels = abs(squares_center[3][1] - square_to_move_to[1])
  square_to_move_to_y_pixels = abs(squares_center[3][0] - square_to_move_to[0])

  square_to_move_y_mm = square_to_move_to_y_pixels * mm_per_pixels_y
  square_to_move_x_mm = square_to_move_to_x_pixels * mm_per_pixels_x

  square_to_move_y_mm = 142 - int(square_to_move_y_mm)
  square_to_move_x_mm = 351 + int(square_to_move_x_mm)

  return piece_to_move_x_mm, piece_to_move_y_mm, square_to_move_x_mm, square_to_move_y_mm, mm_per_pixels_x, mm_per_pixels_y


if __name__ == '__main__':
  # picture = sys.argv[1]
  # picture = '../../board_images/final_board/my_photo-7.jpg'
  # picture = '../../board_images/test_images/blue_test2.jpg'
  cam_command = 'v4l2-ctl -d 1 -c saturation=255,zoom_absolute=500,sharpness=255,focus_auto=0,pan_absolute=-4000,tilt_absolute=20000 -p 5'
  subprocess.Popen(cam_command, stdout = subprocess.PIPE, shell = True)

  cap = cv2.VideoCapture(1)
  cap.set(3, 1920)
  cap.set(4, 1080)
  
  #for i in range(4):
  #  cap.grab()
  #ret, frame = cap.read()

  #square_img = frame
  square_picture = '/home/nvidia/my_photo-58.jpg'
  square_img = cv2.imread(square_picture)

  squares = find_squares(square_img)
  squares_center = find_square_centers(squares)
  squares, squares_center = remove_duplicate_squares(squares, squares_center)


  squares_center, squares = sort_squares(squares_center, squares)

  #cv2.imshow('test', frame)
  #cv2.waitKey(0)
  #cv2.destroyAllWindows()
  rospy.init_node("checkers", anonymous = True)
  man = Manipulation()

  gameover = False
  runMe = True
  current_board = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] # starting board state
  turn = True

  while (runMe == True):
    for i in range(4):
      cap.grab()
    ret, frame = cap.read()

    #cv2.imshow('test', frame)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #picture = './my_photo-62.jpg'
    #orig_img = cv2.imread(picture)
    orig_img = frame

    img = orig_img
    height, width, _ = img.shape

    circles_yellow, circles_green, circles_red, circles_blue = find_circles(img)
    # circles = remove_extra_circles(circles, height, width)
    # yellow_pieces, green_pieces = find_dominant_color(img, circles)
    board_array, circles_to_board = create_board_array(circles_yellow, circles_green, circles_red, circles_blue, squares_center)
        
    # if circles.__len__() > 0:
    #     for i in circles:
    #         cv2.circle(img,(i[0], i[1]), i[2], (0, 255, 0), 2)
    #         cv2.circle(img,(i[0], i[1]), 2, (0, 0, 255), 3)
    try:
      for i in circles_yellow[0,:]:
          cv2.circle(img,(i[0], i[1]), i[2], (0, 255, 0), 2)
          cv2.circle(img,(i[0], i[1]), 2, (0, 0, 255), 3)
    except:
        pass

    try:
        for i in circles_green[0,:]:
            cv2.circle(img,(i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(img,(i[0], i[1]), 2, (0, 0, 255), 3)
    except:
        pass

    try:
        for i in circles_red[0,:]:
            cv2.circle(img,(i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(img,(i[0], i[1]), 2, (0, 0, 255), 3)
    except:
        pass

    try:
        for i in circles_blue[0,:]:
            cv2.circle(img,(i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(img,(i[0], i[1]), 2, (0, 0, 255), 3)
    except:
        pass

    number_of_circles = 0
    for i in range (32):
      if current_board[i] !=0:
        number_of_circles = number_of_circles + 1

    total_circle_amount = 0
    try:
      total_circle_amount += circles_yellow[0].__len__()
      # print(str(circles_yellow.__len__()))
    except:
      pass

    try:
      total_circle_amount += circles_green[0].__len__()
      # print(str(circles_green.__len__()))
    except:
      pass

    try:
      total_circle_amount += circles_red[0].__len__()
      # print(str(circles_red.__len__()))
    except:
      pass

    try:
      total_circle_amount += circles_blue[0].__len__()
      # print(str(circles_blue.__len__()))
    except:
      pass

    if turn == True: #Robot's turn
      if number_of_circles == total_circle_amount:
        print("taking my turn")
        #cv2.imshow('test', orig_img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # detection_error(orig_img, squares, circles)
        moveFrom, moveTo, moveJumps = RunAI(board_array)
        moveFromCol = 65 + (moveFrom % 4)
        moveFromRow = moveFrom // 4
        moveToCol = 65 + (moveTo % 4)
        moveToRow = moveTo // 4
        print("Moving a piece from " +chr(moveFromCol) + str(moveFromRow))
        print("to " + chr(moveToCol) + str(moveToRow))

        piece_to_move = circles_to_board[moveFrom]
        square_to_move_to = squares_center[moveTo]


        piece_to_move_x_mm, piece_to_move_y_mm, square_to_move_x_mm, square_to_move_y_mm, mm_per_pixels_x, mm_per_pixels_y = calculate_move(squares_center, piece_to_move, square_to_move_to)

        man.checkersMove(piece_to_move_x_mm, piece_to_move_y_mm, square_to_move_x_mm, square_to_move_y_mm)

        current_board = board_array
        current_board[moveTo] = current_board[moveFrom]
        if moveTo >= 28:
          current_board[moveTo] = 2
        current_board[moveFrom] = 0

        if moveJumps != None:
          for jump in moveJumps:
            capture_piece = circles_to_board[jump]
            capture_x_pixels = abs(squares_center[3][1] - capture_piece[1])
            capture_y_pixels = abs(squares_center[3][0] - capture_piece[0])

            capture_y_mm = capture_y_pixels * mm_per_pixels_y
            capture_x_mm = capture_x_pixels * mm_per_pixels_x

            capture_y_mm = 142 - int(capture_y_mm)
            capture_x_mm = 351 + int(capture_x_mm)
            man.removePiece(capture_x_mm, capture_y_mm)
            current_board[jump] = 0

        turn = False
        gameover = isGameOver(current_board, 'Light')
        if gameover == True:
          man.dance()
          runMe = False

      else:
        print("camera obstructed didn't detect all circles, trying again")
        print(str(total_circle_amount))
        # cv2.imshow('test', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        time.sleep(3)

    else: #Humans turn
      # print(current_board)
      # print(board_array)
      is_valid_move = isValidMove(current_board, board_array)
      if is_valid_move == False:
        if current_board != board_array:
          print("That is not a valid move. Please change the board state back to: ")
          printBoard(current_board)
          print("Keep in mind that if you have a jump available, you must take the jump!\n")
        time.sleep(3)
      elif is_valid_move == True:
        print("That is a valid move, my turn")
        current_board = board_array
        turn = True
        gameover = isGameOver(current_board, 'Dark')
        if gameover == True:
          runMe = False
        
    #END OF WHILE LOOP RIGHT HERE

  cap.release()
  

