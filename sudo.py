## Sudoku Solver
## by Omeed Fallahi

## References:
##      • http://norvig.com/sudoku.html
##      • https://liorsinai.github.io/coding/2020/07/27/sudoku-solver.html

### Set up definitions of Sudoku where:
###     • rows are defined by letters A-I
###     • columns are defined by numbers 1-9
###     • squares are named by their row and column position, ex. A1
###     • units are defined as a collection of nine squares (column, row, or box)
###     • peers are defined as squares that share a unit

import os, time, random, argparse

def flatten(list):
    return [val for sublist in list for val in sublist]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = [r + c for r in rows for c in cols]
unitlist = [[r + c for r in rows] for c in cols] + \
           [[r + c for c in cols] for r in rows] + \
           [[r + c for r in rs for c in cs] for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

units = {}
for s in squares:
    units[s] = [u for u in unitlist if s in u]

peers = {}
for s in squares:
    peers[s] = set(flatten(units[s])) - set([s])

### Parse a Sudoku board (string form) into a dictionary {square: digit}
def setBoard(b):
    assert len(b) == 81
    startingBoard = {}
    for i, s in enumerate(squares):
        if b[i] in digits or b[i] in '0.':
            startingBoard[s] = b[i]
    return startingBoard

### Create a Sudoku filled board (dictionary) where, aside from the squares that were given as clues,
###     every digit is a possible value for every square
### Next, assign values in squares that were given as clues and remove the value from the peers of that square
def fillBoard(b):
    board = {}
    for s in squares:
        board[s] = digits
    for s, val in setBoard(b).items():
        if val in digits and not assign(board, s, val):
            return False    # cannot assign val to square s
    return board

def assign(board, s, val):
    otherVals = board[s].replace(val, '')
    for val2 in otherVals:
        if not eliminate(board, s, val2):
            return False
    return board

def eliminate(board, s, val):
    if val not in board[s]:
        return board
    board[s] = board[s].replace(val, '')
    if len(board[s]) == 0:
        return False
    # If a square is reduced to a single value, remove that value from the peers of that square
    if len(board[s]) == 1:
        val2 = board[s]
        for s2 in peers[s]:
            if not eliminate(board, s2, val2):
                return False
    # If there is only one square for a value in a given unit, put the value in that square
    for u in units[s]:
        places = [s for s in u if val in board[s]]
        if len(places) == 0:
            return False
        if len(places) == 1:
            if not assign(board, places[0], val):
                return False
    return board

def display(board):
    width = 1 + max(len(board[s]) for s in squares)
    line = ' + '.join(['-' * (width * 3)] * 3)
    for r in rows:
        for c in cols:
            print(''.join(board[r+c].center(width)+(' | ' if c in '36' else '')), end = "")
        print('\n')
        if r in 'CF':
            print(line)

def arrConvert(board):
    sol = []
    for r in rows:
        for c in cols:
            sol.append(int(board[r+c]))

    return sol

def dfs(board):
    if board == False:
        return False    # failed at an earlier recursive call
    if all(len(board[s]) == 1 for s in squares):
        return board
    sMin = float('inf')
    sUse = 0
    for s in squares:
        if len(board[s]) > 1:
            sLen = len(board[s])
            if sLen < sMin:
                sMin = sLen
                sUse = s
    for val in board[sUse]:
        if dfs(assign(board.copy(), sUse, val)):
            return dfs(assign(board.copy(), sUse, val))

def solutionArr(board):
    return arrConvert(solve(board))

def solve(board):
    return dfs(fillBoard(board))

def timedSolve(board, showif = 0.0):
    start = time.time()
    solution = solve(board)
    end = time.time()
    t = end - start

    if showif is not None and t > showif:
        display(solution)
        print('Solved in %.2f seconds\n' % t)

    return (t, solution)


def bulkSolve(filename, name = '', showif = 0.20):
    boards = open(filename).read().strip().split('\n')

    times, results = zip(*[timedSolve(board, showif) for board in boards])
    N = len(boards)
    if N>1:
        print(f"Solved {len(results)} of {N} {name} puzzles (avg {round(sum(times)/N, 2)}, {round(max(times), 2)} secs).")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sudoku solver -- Omeed Fallahi')
    parser.add_argument('-p','--puzzle', required=True, help='File (.txt) or string with puzzle(s) to solve')
    parser.add_argument('-s','--showif', required=False, help='Show solutions for puzzles that take longer (in seconds) that value entered')
    args = parser.parse_args()
    puzzles = args.puzzle
    showif = float(args.showif)

    if '.txt' in puzzles:
        bulkSolve(puzzles, os.path.splitext(puzzles)[0], showif)
    else:
        timedSolve(puzzles, showif)
