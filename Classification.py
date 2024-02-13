#from turtle import color
import imutils
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import pillow_heif
from  get_shapes import get_square_size, get_line_size, remove_lines
from grid import get_coords_lines, plot_grid 


def calculate_black_percentage(x_coords, y_coords, gray):

    xp, yp = np.meshgrid(x_coords, y_coords)
    percentage = []
    x_square = []
    y_square = []
    y_counter = 0
    for j in range(len(yp[0])-1):
        for i in range(len(xp[0])):

            x_square.append(int(xp[0][i]))
            y_square.append(int(yp[j + y_counter][0]))

            if y_counter > 1:
                y_counter = 0

            if len(x_square)%2 != 0:
                y_counter = y_counter + 1
                
            else:
                crop_img = gray[y_square[0]:y_square[1], x_square[0]:x_square[1]]
                pct = crop_img.sum()/(np.shape(crop_img)[0]*np.shape(crop_img)[1]*255)
                
                percentage.append(pct) 
                x_square = [x_square[1]]
                y_square = [y_square[0]]

        x_square = []
        y_square = []
        y_counter = 0
    
    return percentage



def pct_classification(percentage):

    classification = []

    for pct in percentage:
      
        if pct < 1 and pct >= 0.98:
            classification.append(1)
        
        elif pct < 0.98 and pct >= 0.94:
            classification.append(2)

        elif pct < 0.94 and pct >= 0.80:
            classification.append(3)

        elif pct < 0.80 and pct >= 0.68:
            classification.append(4)

        elif pct < 0.68:
            classification.append(5)

        else:
            classification.append(0)

    return classification



def get_test_result(classification):

    ones = classification.count(1)
    twos = classification.count(2)
    threes = classification.count(3)
    fours = classification.count(4)
    fives = classification.count(5)

    if sum([twos, threes, fours, fives])/54 > 0.5:
        result_any = 3
    
    elif sum([twos, threes, fours, fives])/54 > 0.25 and sum([twos, threes, fours, fives])/54 <= 0.5:
        result_any = 2

    elif sum([twos, threes, fours, fives])/54 > 0 and sum([twos, threes, fours, fives])/54 <= 0.25:
        result_any = 1

    elif sum([twos, threes, fours, fives])/54 == 0:
        result_any = 0


    if sum([fours, fives])/54 >= 20/76:
        result_darkest_gray = 3
    
    elif sum([fours, fives])/54 >= 10/76 and sum([fours, fives])/54 < 20/76:
        result_darkest_gray = 2
    
    elif sum([fours, fives])/54 > 0 and sum([fours, fives])/54 < 10/76:
        result_darkest_gray = 1

    elif sum([fours, fives])/54 == 0:
        result_darkest_gray = 0


    if result_darkest_gray != result_any:
        final_result = np.max([result_darkest_gray, result_any])
    else:
        final_result = result_darkest_gray
    
    if final_result == 3:
        test_result = "SEVERE"
    
    elif final_result == 2:
        test_result = "MODERATE"
    
    elif final_result == 1:
        test_result = "MILD"

    elif final_result == 0:
        test_result = "NO DEFECT"

    else:
        test_result = "ERROR"
    
    return test_result

