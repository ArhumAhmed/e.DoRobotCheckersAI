import cv2
import numpy as np
import math
import sys
from matplotlib import pyplot as plt

def find_dominant_color(img, circles):   #must be changed to account for new colors
    white_circles = []
    black_circles = []

    # circles = circles[0]
    test_white = []
    test_black = []

    for item in circles:
        rad = item[2]
        circle_img = img[(item[1]-rad):(item[1]+rad), (item[0]-rad):(item[0]+rad)]

        # cv2.imshow('test', circle_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        average = circle_img.mean(axis=0).mean(axis=0)
        pixels = np.float32(circle_img.reshape(-1,3))
        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]

        if dominant[2] <= 128:
            black_circles.append(item)
            # test_black.append(dominant)
        else:
            white_circles.append(item)
            # test_white.append(dominant)
            # print(dominant)
    
    return white_circles, black_circles

def find_distance(x1, y1, x2, y2):
    num_x = x2 - x1
    num_x = num_x ** 2

    num_y = y2 - y1
    num_y = num_y ** 2

    num_total = num_x + num_y
    num_total = num_total ** 0.5

    return num_total

def sort_squares(squares_center, squares):
    squares_partly_sorted = []
    squares_center_partly_sorted = []

    squares_center, squares = sort_squares_by_y(squares_center, squares)

    for i in range(8):
        squares_center_slice = squares_center[(i*4):((i+1)*4)]
        squares_slice = squares[(i*4):((i+1)*4)]

        squares_center_temp, squares_temp = sort_squares_by_x(squares_center_slice, squares_slice)

        for x in squares_center_temp:
            squares_center_partly_sorted.append(x)

        for x in squares_temp:
            squares_partly_sorted.append(x)

    squares_center = squares_center_partly_sorted
    squares = squares_partly_sorted

    return squares_center, squares

def sort_squares_by_y(square_center_list, square_list):
    for i in range(1, len(square_center_list)):
        j = i - 1
        nxt_element = square_center_list[i]
        nxt_element_alt = square_list[i]

        while(square_center_list[j][1] > nxt_element[1]) and (j >= 0):
            square_center_list[j+1] = square_center_list[j]
            square_list[j+1] = square_list[j]
            j=j-1
        square_center_list[j+1] = nxt_element
        square_list[j+1] = nxt_element_alt
    return square_center_list, square_list

def sort_squares_by_x(square_center_list, square_list):
    for i in range(1, len(square_center_list)):
        j = i - 1
        nxt_element = square_center_list[i]
        nxt_element_alt = square_list[i]

        while(square_center_list[j][0] > nxt_element[0]) and (j >= 0):
            square_center_list[j+1] = square_center_list[j]
            square_list[j+1] = square_list[j]
            j=j-1
        square_center_list[j+1] = nxt_element
        square_list[j+1] = nxt_element_alt
    return square_center_list, square_list

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt( np.dot(d1, d1) * np.dot(d2, d2)))

def find_circles(orig_img):
    img_max_y = orig_img.shape[0]
    img_max_x = orig_img.shape[1]

    x_slice1 = int(0.25 * img_max_x)
    x_slice2 = int(0.75 * img_max_x)

    cropped = orig_img[0: img_max_y, x_slice1: x_slice2]

    hsv_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    #lower_yellow = np.array([30,255,200]) # 200 200 0 RGB   
    #upper_yellow = np.array([30,155,255])  # 255 255 100 RGB


    # lower green RGB - 25, 150, 50
    # upper green RGB - 80, 210, 120

    # lower green HSV - 66, 212, 150
    # upper green HSV - 69, 158, 210

    # lower red RGB - 145, 0, 0 
    # upper red RGB - 180, 5, 10

    # lower red HSV - 0, 255, 145
    # upper red HSV - 179, 247, 181

    # 30 210 120 RGB for green pieces
    #yellow being BGR 10, 230, 225

    #lower_yellow = np.array([21, 255, 200])
    #upper_yellow = np.array([41, 244, 240])
    lower_yellow = np.array([30, 50, 50])
    upper_yellow = np.array([40, 255,255])

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])

    #lower_red = np.array([0, 247, 145])
    #upper_red = np.array([179, 255, 181])

    # lower_red = np.array([162, 240, 140])
    # upper_red = np.array([180, 255, 190])

    lower_red_alt1 = np.array([0, 110, 110])
    upper_red_alt1 = np.array([10, 255, 255])

    lower_red_alt2 = np.array([150, 140, 140])
    upper_red_alt2 = np.array([179, 255, 255])

    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([122, 255, 200])

    mask_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv_img, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
    
    mask_red_alt1 = cv2.inRange(hsv_img, lower_red_alt1, upper_red_alt1)
    mask_red_alt2 = cv2.inRange(hsv_img, lower_red_alt2, upper_red_alt2)
    mask_red = cv2.bitwise_or(mask_red_alt1, mask_red_alt2)

    kernel = np.ones((5,5), np.uint8)
    red_erosion = cv2.erode(mask_red, kernel, iterations=1)
    red_dilation = cv2.dilate(red_erosion, kernel, iterations=3)

    blue_erosion = cv2.erode(mask_blue, kernel, iterations=1)
    blue_dilation = cv2.dilate(blue_erosion, kernel, iterations=5)

    yellow_erosion = cv2.erode(mask_yellow, kernel, iterations=1)
    yellow_dilation = cv2.dilate(yellow_erosion, kernel, iterations=3)

    green_erosion = cv2.erode(mask_green, kernel, iterations=1)
    green_dilation = cv2.dilate(green_erosion, kernel, iterations=3)

    # mask_both = cv2.bitwise_or(mask_yellow, mask_green)
    # res = cv2.bitwise_and(cropped, cropped, mask=mask_both)
    res_yellow = cv2.bitwise_and(cropped, cropped, mask=yellow_dilation)
    res_blue = cv2.bitwise_and(cropped, cropped, mask=blue_dilation)
    res_green = cv2.bitwise_and(cropped, cropped, mask=green_dilation)
    res_red = cv2.bitwise_and(cropped, cropped, mask=red_dilation)

    # cv2.imshow('frame',cropped)
    # cv2.imshow('red-eroded', red_dilation)
    # # cv2.imshow('both', mask_both)
    # cv2.imshow('mask_yellow',mask_yellow)
    # cv2.imshow('mask_green',mask_green)
    # cv2.imshow('mask_blue',mask_blue)
    # cv2.imshow('mask_red', mask_red)

    # cv2.imshow('res',res)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    res_yellow_blurred = cv2.GaussianBlur(res_yellow, (5,5), 0)
    res_yellow_gray = cv2.cvtColor(res_yellow_blurred, cv2.COLOR_BGR2GRAY)

    res_blue_blurred = cv2.GaussianBlur(res_blue, (5,5), 0)
    res_blue_gray = cv2.cvtColor(res_blue_blurred, cv2.COLOR_BGR2GRAY)

    res_red_blurred = cv2.GaussianBlur(res_red, (5,5), 0)
    res_red_gray = cv2.cvtColor(res_red_blurred, cv2.COLOR_BGR2GRAY)

    res_green_blurred = cv2.GaussianBlur(res_green, (5,5), 0)
    res_green_gray = cv2.cvtColor(res_green_blurred, cv2.COLOR_BGR2GRAY)

    circles_yellow = cv2.HoughCircles(res_yellow_gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=25, minRadius=15, maxRadius=40)
    circles_green = cv2.HoughCircles(res_green_gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=25, minRadius=15, maxRadius=40)
    circles_blue = cv2.HoughCircles(res_blue_gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=20, minRadius=15, maxRadius=40)
    circles_red = cv2.HoughCircles(res_red_gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=20, minRadius=15, maxRadius=40)
    # cv2.imshow('blurred_blue', res_blue_gray)
    # cv2.imshow('blurred_red', res_red_gray)
    # cv2.imshow('blurred_yellow', res_yellow_gray)
    # cv2.imshow('blurred_green', res_green_gray)    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    try:
        for i in range(circles_yellow[0].__len__()):
            circles_yellow[0][i][0] = circles_yellow[0][i][0] + x_slice1
    except:
        pass

    try:
        for i in range(circles_green[0].__len__()):
            circles_green[0][i][0] = circles_green[0][i][0] + x_slice1
    except:
        pass

    try:
        for i in range(circles_blue[0].__len__()):
            circles_blue[0][i][0] = circles_blue[0][i][0] + x_slice1
    except:
        pass

    try:
        for i in range(circles_red[0].__len__()):
            circles_red[0][i][0] = circles_red[0][i][0] + x_slice1
    except:
        pass

    # try:
    #     circles = np.uint16(np.around(circles))
    # except:
    #     print("NO CIRCLES DETECTED")
    #     exit(1)

    return circles_yellow, circles_green, circles_red, circles_blue

def find_squares(img):
    squares = []

    # kernel = np.ones((5, 5), np.uint8)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)
    blur = cv2.medianBlur(gray, 3)
    gaussian = cv2.GaussianBlur(blur, (5, 5), 0)

    # cv2.imshow('test', gaussian)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # _,bin = cv2.threshold(gaussian, 127, 255, cv2.THRESH_BINARY)
    # bin = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    bin = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15, 2)
    # bin = cv2.dilate(bin, kernel, iterations=1)
    # bin = cv2.erode(bin, np.ones((11,11)))
    # _, bin = cv2.threshold(gaussian,75,255,cv2.THRESH_BINARY)

    #cv2.imshow('test', bin)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # cv2.imshow("bin", bin)

    contours, hierarchy = cv2.findContours(bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours( gray, contours, -1, (0, 255, 0), 3 )

    #cv2.imshow('contours', gray)
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)

        # for comau tournament board w/ poker chips
        #if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
        #if len(cnt) == 4 and (cv2.contourArea(cnt) > 1000 and cv2.contourArea(cnt) < 10000) and cv2.isContourConvex(cnt):
        if len(cnt) == 4 and ((cv2.contourArea(cnt) > 1000 and cv2.contourArea(cnt) < 10000) or (cv2.contourArea(cnt) > 400000 and cv2.contourArea(cnt) < 500000)) and cv2.isContourConvex(cnt):
            cnt = cnt.reshape(-1, 2)
            max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
            if max_cos < 0.1:
                squares.append(cnt)
    return squares

def find_square_centers(squares):
    squares_center = []

    for sq in squares:  # find the centers of the squares and their "radius"
        mean_x = 0  # set mean x coordinate
        mean_y = 0  # set mean y coordinate

        for coords in sq:
            mean_x += coords[0] # add x coordinate from corner
            mean_y += coords[1] # add y coordinate from corner

        mean_x /= 4 # divide both means by # of corners
        mean_y /= 4
        radius = abs(mean_x - sq[0][0])
        squares_center.append([mean_x, mean_y, radius]) # append center coordinates to array

    return squares_center

def remove_duplicate_squares(squares, squares_center):
    temp_squares = []
    temp_squares_center = []

    for i in range(0, squares.__len__()):
        if squares_center[i] == None:
            continue
        for j in range(0, squares.__len__()):
            if squares_center[j] == None or j == i:
                continue
            if (find_distance(squares_center[i][0], squares_center[i][1], squares_center[j][0], squares_center[j][1]) < 20):
                squares_center[j] = None
                squares[j] = None

    for i in range(0, squares.__len__()):
        if squares_center[i] != None:
            temp_squares.append(squares[i])
            temp_squares_center.append(squares_center[i])

    return temp_squares, temp_squares_center

def remove_extra_circles(circles, height, width):
    output_circles = []

    for i in range(circles[0].__len__()):
        if find_distance(circles[0][i][0], circles[0][i][1], width//2, height//2) < 400:
            output_circles.append(circles[0][i])

    return output_circles

def create_board_array(circles_yellow, circles_green, circles_red, circles_blue, squares_center):
    board_array = [0] * 32
    circles_to_board = [0] * 32

    try:
      green_pieces = circles_green[0]
      for piece in green_pieces:
          smallest = sys.maxsize
          saved_index = 0
          for index in range(len(squares_center)):
              num = find_distance(piece[0], piece[1], squares_center[index][0], squares_center[index][1])
              if num < smallest:
                  smallest = num
                  saved_index = index

          board_array[saved_index] = -1
          circles_to_board[saved_index] = piece
    except:
      pass

    try:
      yellow_pieces = circles_yellow[0]
      for piece in yellow_pieces:
          smallest = sys.maxsize
          saved_index = 0
          for index in range(len(squares_center)):
              num = find_distance(piece[0], piece[1], squares_center[index][0], squares_center[index][1])
              if num < smallest:
                  smallest = num
                  saved_index = index

          board_array[saved_index] = 1
          circles_to_board[saved_index] = piece
    except:
      pass

    try:
      blue_pieces = circles_blue[0]
      for piece in blue_pieces:
          smallest = sys.maxsize
          saved_index = 0
          for index in range(len(squares_center)):
              num = find_distance(piece[0], piece[1], squares_center[index][0], squares_center[index][1])
              if num < smallest:
                  smallest = num
                  saved_index = index

          board_array[saved_index] = -2
          circles_to_board[saved_index] = piece
    except:
      pass

    try:
      red_pieces = circles_red[0]
      for piece in red_pieces:
          smallest = sys.maxsize
          saved_index = 0
          for index in range(len(squares_center)):
              num = find_distance(piece[0], piece[1], squares_center[index][0], squares_center[index][1])
              if num < smallest:
                  smallest = num
                  saved_index = index

          board_array[saved_index] = 2
          circles_to_board[saved_index] = piece
    except:
      pass

    # temp_board_array = []
    # for i in range(0,32):
    #     if (i // 4) % 2 == 0:
    #         temp_board_array.append(0)
    #         temp_board_array.append(board_array[i])
    #     else:
    #         temp_board_array.append(board_array[i])
    #         temp_board_array.append(0)

    # board_array = temp_board_array

    return board_array, circles_to_board

def detection_error(orig_img, squares, circles):
    # if squares.__len__() < 32:
        print("Could not detect all squares")

        if circles.__len__() > 0:
            for i in circles:
                cv2.circle(orig_img,(i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(orig_img,(i[0], i[1]), 2, (0, 0, 255), 3)

        cv2.drawContours(orig_img, squares, -1, (0, 255, 0), 3)

        cv2.imshow('test', orig_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
