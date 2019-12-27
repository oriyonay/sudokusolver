# an efficient sudoku solver in python, written by ori yonay

import time

def load(filename):
    board = []
    f = open(filename, 'r')
    for line in f.readlines():
        # in case user enters dashes instead of 0s:
        line = line.replace('-', '0')

        # check for errors:
        if len(line.split(' ')) != 9:
            print('error: invalid input!')
            return None

        # append the board with the new row:
        board.append([int(i) for i in(line.split(' '))])

    # check for errors:
    if len(board) != 9:
        print('error: invalid input!')
        return None

    return board

def printboard(board):
    for row in board:
        rowStr = ''
        for i in row:
            rowStr += '- ' if i == 0 else (str(i) + ' ')
        print(rowStr)

# determines whether num is a valid option in board at position pos:
def valid(board, num, pos):
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    for i in range(3 * (pos[0] // 3), 3*(pos[0] // 3) + 3):
        for j in range(3 * (pos[1] // 3), 3*(pos[1] // 3) + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

# returns the next empty square in the board, if there is one:
def nextemptysquare(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return None

# the backtracking algorithm:
def backtrack(board):
    pos = nextemptysquare(board)
    if not pos:
        return board

    row, col = pos

    # otherwise, we try the next empty spot with all possible options:
    for num in range(9):
        if valid(board, num+1, (row, col)):
            board[row][col] = num+1
            solvedBoard = backtrack(board)
            if solvedBoard != None:
                return solvedBoard
            board[row][col] = 0

    return None

# the meat of this whole thing. solve() performs the 'obvious squares' heuristic,
# and then calls the backtracking algorithm:
def solve(board):
    # create the options board:
    options = []

    # keep track of the number of solved squares:
    solved = 0

    # fill the options board:
    for row in range(9):
        options.append([])
        for col in range(9):
            options[row].append([])
            if board[row][col] == 0:
                options[row][col] = [True] * 9
            else:
                options[row][col] = [False] * 9
                options[row][col][(board[row][col])-1] = True
                # increment the number of solved squares:
                solved += 1

    # fill the options board as much as possible:
    num = 0
    while solved != 81:
        solvedAtLeastOneSquare = False
        # update the options board:
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    numIdx = board[row][col] - 1 # index of truth 'switch'
                    for i in range(9):
                        if i != col:
                            options[row][i][numIdx] = False
                        if i != row:
                            options[i][col][numIdx] = False
                    # update the inside box:
                    for i in range(3 * (row // 3), 3*(row // 3) + 3):
                        for j in range(3 * (col // 3), 3*(col // 3) + 3):
                            if i != row and j != col:
                                options[i][j][numIdx] = False

        # now that the options board is updated, we can look for possible squares to solve:
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0 and options[row][col].count(True) == 1:
                    # then there's only one option for this square:
                    board[row][col] = options[row][col].index(True) + 1
                    # update our flags:
                    solvedAtLeastOneSquare = True
                    solved += 1

        # if we haven't solved at least one square in this iteration, then
        # this will go on indefinitely and we need to break.
        if not solvedAtLeastOneSquare:
            break

    # if the board is completely solved, we're done:
    if solved == 81:
        return board

    # now that we've eliminated as many 'easy' squares as possible, we backtrack
    # our way to solve the puzzle.
    return backtrack(board)

if __name__ == '__main__':
    # load the board from text file:
    board = load('./hardestever.txt')

    # start the timer:
    start_time = time.time()

    # solve the board:
    board = solve(board)

    # print it, along with the time:
    printboard(board)
    print()
    print("--- solve took %f seconds ---" % (time.time() - start_time))
