# Board.py, by Barb Wahl and Theresa Wilson (11-17-19)
# Modified by:
#     STUDENT NAME: Lauren Dickman
#     DATE: Monday, December 2, 2019

# The Connect Four board is represented by a list of seven columns,
# where each column is a list with entries from the set {'.', 'X', 'O'}.
# An entry equal to 'X' represents a checker belonging to player 1, and
# an entry equal to 'O' represents a checker belonging to player 2. An
# entry equal to '.' is an open spot on the board.

# If C is a column in the board, then C[0] represents the checker at the
# TOP of the column, C[1] is the next checker DOWN, and so on. An "empty"
# column looks like ['.', '.', '.', '.', '.', '.'] and is filled from
# right to left ("bottom" to "top") by replacing '.' with 'X' or 'O'
# as checkers are dropped into that column.

# A player wins the game by getting four of their checkers adjacent on the
# board, either vertically, horizontally, or diagonally (falling from left-to-
# right or right-to-left). If the board becomes full without a winner, the
# game ends in a tie due to deadlock. Since there are 7 columns and 6 rows, the
# maximum number of turns that can be taken in a game is 42.

from copy import copy

class Board:
    # Class Constants -- refer to by NAME, not by VALUE
    NUM_ROWS = 6
    NUM_COLS = 7
    MAX_MOVES = 42
    CHECKER = ['.', 'X', 'O']

    ### SPECIAL METHODS ###
    ###
    # __init__
    # The Board "constructor" method. Activated when a function call: Board()
    #    is executed. Initializes a new Board object to create an empty board
    #    for game play. Automatically returns a reference to the new object.
    ###
    def __init__(self):
        blank_col = ['.', '.', '.', '.', '.', '.']
        self.cols = []
        for c in range(Board.NUM_COLS):
            self.cols.append(copy(blank_col))  # copy to prevent aliasing

    ###
    # __str__
    # The "to string" method for the Board class.
    # Activated when a Board object is printed; returns the string
    # representation of a Board.
    ###
    def __str__(self):
        border = '=' * 29 + "\n"
        acc = "\n  0   1   2   3   4   5   6   \n"    # column indexs
        acc += border                     # top border
        for row in range(Board.NUM_ROWS):
            acc += self.row_to_string(row) + "\n"
        acc += border
        return acc

    ### OTHER METHODS ###
    ###
    # is_empty_square
    # Checks whether a given board location has no checker.
    # paramters: `col`, an index in range(Board.NUM_COLS)
    #            `row`, an index in range(Board.NUM_ROWS)
    # return: True if the board location is holding the character
    #         '.', False otherwise.
    ###
    def is_empty_square(self, col, row):
        if self.cols[col][row] == '.':
            return True
        else:
            return False

    ###
    # fill
    # For testing; fills a Board with the characters from a provided string.
    # The first column is filled, then the second, and so on.
    # parameters:  s, a string of length 42 or more
    ###
    def fill(self, s):
        # use chars in s to fill columns of Board
        for c in range(Board.NUM_COLS):
            # stop minus start equals number of rows in board, which
            # is the length of one column
            start = Board.NUM_ROWS * c
            stop = Board.NUM_ROWS * (c + 1)
            self.cols[c] = list(s[start : stop])

    ###
    # row_to_string
    # Helper for the __str__ method, returns the string for printing
    # a single row of the board.
    ###
    def row_to_string(self, row):
        acc = '|'
        for col in range(Board.NUM_COLS):
            acc = acc + ' ' + self.cols[col][row] + ' |'
        return acc

    ###
    # take_turn
    # Prompts a player to choose a column number (an integer in the range
    # 0 through 6) until a valid column is entered, then places the player's
    # checker into that column.
    # parameters: player_num, an integer, either 1 or 2
    # return: the tuple (col, row) indicating where the checker was placed;
    #         the column index `col` is determined by prompting the player to
    #         enter a valid column number, repeately, until they do so
    # note:   A valid column cannot be completely full of checkers.
    ###
    def take_turn(self, player_num):
        move = int(input("Player " + str(player_num) + " enter a number between 0 and 6: "))
        while self.is_valid_move(move) == False:
            move = int(input("Player " + str(player_num) + " enter a number between 0 and 6: "))
        print("Placing checker at column number", move)
        return self.place_checker_in_column(move, player_num)

    ###
    # is_valid_move
    # helper for take_turn; checks that a given column index is a valid move
    # return: True if col is in range(Board.NUM_COLS) and that column of the
    #         board is not completely full of checkers.
    # note: Use a call to the is_empty_square method.
    ###
    def is_valid_move(self, col):
        if col not in range(Board.NUM_COLS):
            return False
        for i in range(Board.NUM_COLS):
            if self.is_empty_square(col, i) == True:
                return True
            else:
                return False

    ###
    # place_checker_in_column
    # updates the board by adding a specific checker to a given column
    # parameters: `col`, an index in range(Board.NUM_COLS)
    #             `player_num`, an integer (1 or 2)
    #
    # return: the tuple (col, row) indicating where the checker was placed
    # note:   The LAST occurrence of '.' in the specified column is replaced
    #         by 'X' or 'O'. (Use a call to the is_empty_square method.)
    ###
    def place_checker_in_column(self, col, player_num):
        for i in range(Board.NUM_ROWS - 1, -1, -1):
            if self.is_empty_square(col, i) == True:
                self.cols[col][i] = Board.CHECKER[player_num]
                return (col, i)

    ###
    # has_winner
    # verifies whether the checker that was just played at a specific position
    # on the board has created a winning condition
    # paramters: `col`, an index in range(Board.NUM_COLS)
    #            `row`, an index in range(Board.NUM_ROWS)
    # return: True if there is a winner in the row indexed by `row`, the column
    #         indexed by `col`, or one of the two diagonals through (col, row);
    #         otherwise, False.
    ###
    def has_winner(self, col, row):
        # check column `col`
        if has_winning_substring(self.get_col(col)):
            return True
        # check row `row`
        if has_winning_substring(self.get_row(row)):
            return True
        # check LR_diag through (col, row)
        if has_winning_substring(self.get_LR_diag(col, row)):
            return True
        # check RL_diag through (col, row)
        if has_winning_substring(self.get_RL_diag(col, row)):
            return True
        # no winner
        return False

    ###
    # get_row
    # helper for has_winner, returns a string representation of a given row
    # parameters: `row`, an integer in range(Board.NUM_ROWS)
    # return: a string accumulated by concatenating the characters in the row
    #         indexed by `row`
    ###
    def get_row(self, row):
        newstr = ""
        for i in range(Board.NUM_COLS):
            newstr = newstr + self.cols[i][row]
        return newstr

    ###
    # get_col
    # helper for has_winner, returns a string representation of a given column
    # parameters: `col`, an integer in range(Board.NUM_COLS)
    # return: a string accumulated by concatenating the characters in the
    #         column indexed by `col`
    ###
    def get_col(self, col):
        newstr = ""
        for i in range(Board.NUM_ROWS):
            newstr = newstr + self.cols[col][i]
        return newstr

    ###
    # get_LR_diag
    # helper for has_winner, returns a string representation of a given
    #     left-to-right diagonal
    # parameters: `col`, an integer in range(Board.NUM_COLS)
    #             `row`, an integer in range(Board.NUM_ROWS)
    # return: a string accumulated by concatenating the characters in the
    #         left-to-right diagonal which passes through board location
    #         (col, row)
    ###
    def get_LR_diag(self, col, row):
        cols = []
        rows = []
        # move left and up to find the first position in the diagonal
        while col > 0 and row > 0:
            col -= 1
            row -= 1
        # move right and down to accumulate the characters along the diagonal
        while col < Board.NUM_COLS and row < Board.NUM_ROWS:
            cols.append(col)
            rows.append(row)
            col += 1
            row += 1
        return self.get_string_from(cols, rows)

    ###
    # get_RL_diag
    # helper for has_winner, returns a string representation of a given
    #     right-to-left diagonal
    # parameters: `col`, an integer in range(Board.NUM_COLS)
    #             `row`, an integer in range(Board.NUM_ROWS)
    # return: a string accumulated by concatenating the characters in the
    #         right-to-left diagonal which passes through board location
    #         (`col`, `row`)
    ###
    def get_RL_diag(self, col, row):
        cols = []
        rows = []
        # move right and up to find the first position in the diagonal
        while col < Board.NUM_COLS - 1 and row > 0:
            col += 1
            row -= 1
        # move left and down to accumulate the characters along the diagonal
        while col >= 0 and row < Board.NUM_ROWS:
            cols.append(col)
            rows.append(row)
            col -= 1
            row += 1
        return self.get_string_from(cols, rows)

    ###
    # get_string_from
    # helper for get_LR_diag and get_RL_diag, takes parallel lists of
    #     column and row indices and returns the corresponding string
    #     of characters from those positions on the board
    # parameters: C, a list of column indices
    #             R, a list of row indices where len(R) = len(C)
    # return: the string of characters from locations (C[0], R[0]),
    #         (C[1], R[1]), (C[2], R[2]), etc.
    ###
    def get_string_from(self, C, R):
        acc = ""
        for i in range(len(C)):
            acc += self.cols[C[i]][R[i]]
        return acc
# END OF BOARD CLASS DEFINITION

###
# has_winning_substring
# External helper function (not part of the Board class) for has_winner; takes
#     a string of characters and checks for a winning substring
# parameters: `s`, a string
# return: True if `s` has a substring equal to "XXXX" or "OOOO"; otherwise,
#     returns False
###
def has_winning_substring(s):
    if "XXXX" in s:
        return True
    if "OOOO" in s:
        return True
    else:
        return False

# main
# Testing function for Board class
# Delete or comment out the call to main() when you are done with testing
#     the Board class.
def main():
   board = Board()  # create a board
   print("\nTesting get_col...")
   test_string = 'colum0colum1colum2colum3colum4colum5colum6'
   board.fill(test_string)
   print(board)
   print("Here are the columns of the board:")
   for c in range(Board.NUM_COLS):
       col = board.get_col(c)
       correct = 'colum' + str(c)
       assert col == correct
       print(col)
   print("\nTesting get_row...")
   test_string = '012345012345012345012345012345012345012345'
   board.fill(test_string)
   print(board)
   print("Here are the rows of the board:")
   for r in range(Board.NUM_ROWS):
       row = board.get_row(r)
       correct = str(r) * Board.NUM_COLS
       assert row == correct
       print(row)
   print("\nTesting has_winning_substring...")
   negative = ['xxxx', '....', 'XXX', 'OOO', 'XOXOXOXO', 'OO.OO']
   positive = ['XXXX', 'OOOO', 'XXXXO', '.XXXX', 'XOOOO.', 'XXXOXXXX']
   print()
   for word in negative:
       print("Testing word =", word)
       assert not has_winning_substring(word)
       print("OK")
   for word in positive:
       print("Testing word =", word)
       assert has_winning_substring(word)
       print("OK")
   print("\nTesting is_valid_move...")
   test_string = '........OOXX.XXOOXOOXOXOXOXOXOOXXOXX..XOOX'
   board.fill(test_string)
   print(board)
   negative = [-2, -1, 3, 4, 5, 7, 8]
   positive = [0, 1, 2, 6]
   for move in negative:
       print("Testing move =", move)
       assert not board.is_valid_move(move)
       print("OK")
   for move in positive:
       print("Testing move =", move)
       assert board.is_valid_move(move)
       print("OK")
   print("\nCurrent board:")
   print(board)
   print("\nTesting place_checker_in_column...")
   #test 1: put an 'O' in column 2
   print("\nTest: put an 'O' in column 2")
   old_col_info = board.get_col(2)
   correct = 'O' + old_col_info[1:]
   col, row = board.place_checker_in_column(2, 2)
   assert col == 2
   assert row == 0
   assert board.get_col(2) == correct
   print(board)
   print("OK")
   #test 2: put an 'X' in column 1
   print("\nTest: put an 'X' in column 1")
   old_col_info = board.get_col(1)
   correct = '.X' + old_col_info[2:]
   col, row = board.place_checker_in_column(1, 1)
   assert col == 1
   assert row == 1
   assert board.get_col(1) == correct
   print(board)
   print("OK")
   print("\nTesting take_turn interactively.")
   print("Be sure to enter some INVALID moves in addition to valid moves.")
   board.take_turn(1)  # Player 1 ('X' checker) prompted to make a move
   print(board)
   board.take_turn(2)  # Player 2 ('O' checker) prompted to make a move
   print(board)
   board.take_turn(1)  # Player 1 ('X' checker) prompted to make a move
   print(board)
   board.take_turn(2)  # Player 2 ('O' checker) prompted to make a move
   print(board)
   print("Board class is looking good!")

#main()