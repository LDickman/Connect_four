# FILE NAME: Connect_four.py
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

from Board import Board
from sys import exit

def intro():
    print("\nWelcome to Connect Four: Python Version. In this simulation a board is drawn with 6 rows and 7 colums.")
    print("Players, one is using 'X' and the other is using 'O', take turns dropping their checker into a column.")
    print("The first player to get four of their checkers in a row either horizontally, vertically, or diagonally wins!")
    print("However, the game can end without a winner and enters a deadlock and the game ends within 42 moves.\n")

# next_player
# Changes the player after the other player takes thier turn
# paramters: `player_num`, an integer (1 or 2)
# return: the integer of either 1 or 2
def next_player(player_num):
    if player_num == 1:
        return 2
    else:
        return 1

# main
# Actually starts the game and declare teh winner the game, or if the game is in a dead lock
# note: uses the Board class.
def main():
    board = Board()
    intro()
    print(board)
    player_num = 1
    col, row = board.take_turn(player_num)
    print(board)
    move = 1
    while board.has_winner(col, row) == False and move < board.MAX_MOVES:
        player_num = next_player(player_num)
        col, row = board.take_turn(player_num)
        print(board)
        move = move + 1
        if move == board.MAX_MOVES:
            print("The game has end in a deadlock. NO ONE WINS! Don't worry you can try again!\n")
            exit()    
    print("Player " + str(player_num) + " won the game!\n")
   
main()