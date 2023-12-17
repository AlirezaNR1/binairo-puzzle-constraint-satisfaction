from time import time
from Binairo import *
from State import *


# w b
def main():
    input_numbers = []
    # first row = size of puzzle(n), second row = number of cells that have color in the start (m), row 3 to row 3+m :

    # enter the test case from test cases folder
    test_case = open("test_cases/input1.txt").readlines()
    for line in test_case:
        line = line.rstrip()
        numbers = line.split(' ')
        n = [int(number) for number in numbers]
        input_numbers.append(n)

    board = []
    size_puzzle = input_numbers[0][0]
    for i in range(0, size_puzzle):

        row = []
        for j in range(0, size_puzzle):
            cell = Cell(i, j)
            row.append(cell)
        board.append(row)

    for i in range(2, len(input_numbers)):

        if input_numbers[i][2] == 0:  # w
            board[input_numbers[i][0]][input_numbers[i][1]].value = 'W'
            board[input_numbers[i][0]][input_numbers[i][1]].domain = ['n']

        if input_numbers[i][2] == 1:  # b
            board[input_numbers[i][0]][input_numbers[i][1]].value = 'B'
            board[input_numbers[i][0]][input_numbers[i][1]].domain = ['n']

    state = State(size_puzzle, board)
    print('initial board:')
    state.print_board()
    start_time = time()

    #this function solves the puzzle
    backTrack(state)

    end_time = time()
    print('time: ', end_time - start_time)


if __name__ == "__main__":
    main()
