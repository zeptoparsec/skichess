from boardstate import Boardstate
from os import system
from time import sleep

def sanitizeinput(input):
    if len(input) != 4:
        return -1
    return 0

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

    if sanitizeinput(move) != 0:
        print('Invalid input!\n')
        sleep(1)
    else:
        startpos = x_axis[move[0]] + y_axis[move[1]]*8 - 1
        endpos = x_axis[move[2]] + y_axis[move[3]]*8 - 1

        try:
            if board.makemove(startpos, endpos, turn) == -1: raise Exception
        except: 
            print("Invalid move!\b\n")
            sleep(1)
        else:
            turn = not turn
