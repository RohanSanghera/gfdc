import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_square_size(gray, phone, img):

    area_treshold = 2000   

    # adaptive threshold
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)

    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)  

    # Draw rectangles, the 'area_treshold' value was determined empirically
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
     
    height = []
    width = []  
    for c in cnts:

        if cv2.contourArea(c) > area_treshold :
          
          x,y,w,h = cv2.boundingRect(c)
          cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)

          height.append(h)
          width.append(w) 


    return np.max(height), np.max(width)

def get_line_size(gray, phone, img):
    #Apply blue gray and define threshold using canny
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    #use HoughLinesP to get the lines

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 500  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)
    max_line = []
    min_line = []
    xs_line = []
    ys_line = []

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

            max_line.append(np.max([x1,y1, x2,y2]))
            min_line.append(np.min([x1,y1, x2,y2]))
            xs_line.extend([x1, x2])
            ys_line.extend([y1, y2])

    # Draw the lines on the  image
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

    return np.max(np.array(max_line) - np.array(min_line)), np.min(xs_line), np.min(ys_line)



def remove_lines(line_size, line_start_left, line_start_top, line_thickness, gray):
    line_size = np.round(line_size)
    line_start_left = int(line_start_left)
    line_start_top = int(line_start_top)
        
    gray[line_start_top + int(line_size/2) - line_thickness : line_start_top + int(line_size/2+2) + line_thickness,
               line_start_left  : line_start_left + int(line_size) ] = 255

    gray[line_start_top : line_start_top + int(line_size),
                    line_start_left + int(line_size/2) - line_thickness : line_start_left + int(line_size/2) + line_thickness] = 255


    return gray