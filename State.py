from Cell import *


class State:
    def __init__(self, size, board=[]):
        self.board = board
        self.size = size

    def print_domain(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                print(self.board[i][j].domain, end=" ")
            print("\n")

    def print_board(self):
        white_circle = '\u26AB'
        black_circle = '\u26AA'
        w_sqr = '\u2B1B'
        b_sqr = '\u2B1C'
        line = '\u23E4'

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].value == 'b':
                    print(black_circle, end='  ')
                elif self.board[i][j].value == 'B':
                    print(b_sqr, end='  ')

                elif self.board[i][j].value == 'W':
                    print(w_sqr, end='  ')

                elif self.board[i][j].value == 'w':
                    print(white_circle, end='  ')
                else:
                    print(line, end='')
                    print(line, end='')
                    print(end='  ')

            print()
            print()
