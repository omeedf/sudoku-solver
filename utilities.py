## Utilities for Sudoku Solver
## by Omeed Fallahi

## References:
##      • Murtaza Hassan: https://github.com/murtazahassan
##			-> refered to for CNN (digit classification) and OpenCV implementation

import os, cv2, numpy as np
from skimage import data
from skimage.transform import resize


# Find the biggest contour by area and return its four corners and area
def findBiggestContour(contours):
    biggest = []
    max = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 50:
            perim = cv2.arcLength(c, True)
            corners = cv2.approxPolyDP(c, 0.02 * perim, True)
            if area > max and len(corners) == 4:
                biggest = corners
                max = area

    return biggest, max

# Re-order the corners of the biggest contour as ([0,0], [0, width], [height, 0], [height, width])
def reorderCorners(corners):
    corners = corners.reshape((4,2))
    ordered = np.zeros((4, 1, 2), dtype = int)
    total = corners.sum(1)
    ordered[0] = corners[np.argmin(total)]  #smallest sum of points is origin
    ordered[3] = corners[np.argmax(total)]  #largest sum of points is last
    diff = np.diff(corners, axis=1)
    ordered[1] = corners[np.argmin(diff)]   #negative difference in points is second
    ordered[2] = corners[np.argmax(diff)]   #positive difference in points is third
    return ordered

# Split the Sudoku board into each individual square
def getSquares(board):
    rows = np.vsplit(board, 9)
    squares = []
    for row in rows:
        cols = np.hsplit(row, 9)
        for square in cols:
            squares.append(square)

    return squares


# Determine the digit in the square using prediction model
def getDigit(squares, model):
    numbers = []
    for sq in squares:
        img = np.asarray(sq)
        img = img[6:img.shape[0] - 6, 6:img.shape[1] - 6]
        img = cv2.resize(img, (28,28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        prediction = model.predict(img)
        index = np.argmax(prediction, axis=-1)
        prob = np.amax(prediction)
        if prob > 0.8:
            numbers.append(index[0])
        else:
            numbers.append(0)
    return numbers

def projectNums(img, numbers, color = (0, 255, 0)):
    W = int(img.shape[1] / 9)
    H = int(img.shape[0] / 9)

    for i in range(9):
        for j in range(9):
            if numbers[(j * 9) + i] != 0:
                cv2.putText(img, str(numbers[(j * 9) + i]),
                            (i * W + int(W/2)-10, int((j+ 0.8)*H)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            2, color, 2, cv2.LINE_AA)
    return img
