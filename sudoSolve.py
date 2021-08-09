## Sudoku Solver using OpenCV
## by Omeed Fallahi

## References:
##      • Murtaza Hassan: https://github.com/murtazahassan
##			-> CNN (digit classification) and OpenCV implementation for board capture and projection
##		• Peter Norvig: http://norvig.com/sudoku.html
##			-> constraint propogation and search algorithm for solving sudoku

from utilities import *
from sudo import *
import os, cv2, numpy as np
from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image

def solvePuzzle():
	st.title("Sudoku Solver with OpenCV")
	st.write("project by Omeed Fallahi")
	st.caption("This Sudoku Solver uses OpenCV to parse an image of a sudoku puzzle "
	"by identifying the boundaries of the grid. It then detects and isolates each square of the grid "
	"and classfies the digit (or blank) on each square using a convolutional neural network. "
	"The board is then solved using a combination of constraint propogation and depth-first search "
	"using an algorithm adopted from Peter Norvig. Finally, the solution is then projected back "
	"onto the original image and displayed. Full source code and references are available on my GitHub.")

	print('Setting up... loading tensorflow...')
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

	model = load_model('digit-classifier.h5')
	height = 450
	width = 450
	blankImg = np.zeros((height, width, 3), np.uint8)

	# 1. Prepare the image
	uploaded_file = st.file_uploader("Choose an image file of a sudoku board to solve (.png, .jpg, .jpeg, etc.).")
	if uploaded_file is not None:
		file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
		image = cv2.imdecode(file_bytes, 1)

		image = cv2.resize(image, (width, height))
		finalCopy = image.copy()
		imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
		imgThresh = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)

		# 2. Find all the contours in the image
		imgContours = image.copy()
		imgLargestContours = image.copy()
		contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

		# 3. Find the biggest contour in the image and use it as the Sudoku board
		biggest, area = findBiggestContour(contours)
		if biggest.size != 0:	#if a board was found
			biggest = reorderCorners(biggest)
			cv2.drawContours(imgLargestContours, biggest, -1, (0, 0, 255), 25)
			p1 = np.float32(biggest)
			p2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
			matrix = cv2.getPerspectiveTransform(p1, p2)
			imgWarp = cv2.warpPerspective(image, matrix, (width, height))
			imgWarp = cv2.cvtColor(imgWarp, cv2.COLOR_BGR2GRAY)

		# 4. Split the image into each square and determine the digit using prediction model
		squares = getSquares(imgWarp)
		digits = getDigit(squares, model)
		sudokuBoard = ''.join(str(e) for e in digits)

		# 5. Find the solution of the parsed board
		solution = solutionArr(sudokuBoard)
		newSpots = [None] * 81
		for i in range(81):
			newSpots[i] = digits[i] - solution[i]
		addedD = [abs(ele) for ele in newSpots]

		# 5. Display the parsed board
		board1 = blankImg.copy()
		board2 = blankImg.copy()
		initialBoard = projectNums(board1, digits, color = (0, 0, 255))
		solvedBoard = projectNums(board2, addedD, color = (124,252,0))

		# 6. Overlay solution
		pts2 = np.float32(biggest)
		pts1 = np.float32([[0,0], [width, 0], [0, height], [width, height]])
		matrix = cv2.getPerspectiveTransform(pts1, pts2)
		final = blankImg.copy()
		final = cv2.warpPerspective(solvedBoard, matrix, (width, height))
		solution = cv2.addWeighted(image, 0.3, final, 0.7, 0)

		# 7. Display solution
		col1, col2 = st.columns(2)
		original = Image.open(uploaded_file)
		col1.header("Unsolved")
		col1.image(original, use_column_width=True)
		col2.header("Solved")
		col2.image(solution, use_column_width=True)
		#cv2.imshow('final', solution)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

if __name__ == '__main__':
    solvePuzzle()
