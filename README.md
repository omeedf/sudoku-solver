# Sudoku Solver using OpenCV
## project by Omeed Fallahi

[Click here to launch the web-app](https://share.streamlit.io/omeedf/sudoku-solver/main/sudoSolve.py "Sudoku Solver, Omeed Fallahi"), or use the embedded button below!

[![Click here to launch the web app!](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/omeedf/sudoku-solver/main/sudoSolve.py)

This Sudoku Solver uses OpenCV to parse an image of a sudoku puzzle by identifying the boundaries of the grid. It then detects and isolates each square of the grid and classfies the digit (or blank) on each square using a convolutional neural network. The board is then solved using a combination of constraint propogation and depth-first search using an algorithm adopted from Peter Norvig. Finally, the solution is then projected back onto the original image and displayed. 

![Example of Sudoku Solver Implementation](https://github.com/omeedf/sudoku-solver/blob/main/images/sudokuSolver-example.png?raw=true)
