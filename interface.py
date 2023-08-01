from boardstate import Boardstate
from os import system
from time import sleep

board = Boardstate()

x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

turn = True
while True:
    system('cls')
    board.printboard()
    if turn:
        move = input("White's turn: ").lower()
    else:
        move = input("Black's turn: ").lower()

    try:
        if move == 'restart':
            board.restart()
            turn = True
            continue

        startpos = x_axis[move[0]] + y_axis[move[1]]*8 - 1
        endpos = x_axis[move[2]] + y_axis[move[3]]*8 - 1

        is_valid_input = (move[0: 3: 2].isalpha() and move[1: 4: 2].isnumeric()) == (len(move) == 4)
        if not is_valid_input or board.makemove(startpos, endpos, turn) == -1: raise Exception
    except: 
        print("Invalid move!")
        sleep(1)
    else:
        turn = not turn
