from boardstate import Boardstate
from os import system
from time import sleep
from datetime import datetime

board = Boardstate()

x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

then = 0
now = 0

time = [600,600]
inc = [1,1]

turn = True
legacy = False

while True:
    system('cls')
    board.printboard(legacy)

    time[int(not turn)] -= then - now - inc[int(not turn)]

    print("You spent",then-now,"seconds on the previous move.\nYou have",time[int(not turn)],'seconds left.')

    if time[0] <= 0:
        print('Black ran out of time!')
        break
    
    if time[1] <= 0:
        print('White ran out of time!')
        break

    now = int(datetime.now().timestamp())

    if turn:
        move = input("White's turn: ").lower()
    else:
        move = input("Black's turn: ").lower()
    then = int(datetime.now().timestamp())

    try:
        if move == 'restart':
            board.restart()
            time = [600, 600]
            turn = True
            continue

        if move == 'legacy':
            print('Legacy')
            legacy = True
            time = [600, 600]
            board.restart()
            turn = True
            continue

        startpos = x_axis[move[0]] + y_axis[move[1]]*8 - 1
        endpos = x_axis[move[2]] + y_axis[move[3]]*8 - 1

        is_valid_input = (move[0: 3: 2].isalpha() and move[1: 4: 2].isnumeric()) == (len(move) == 4)
        if not is_valid_input or board.makemove(startpos, endpos, turn, move) == -1: raise Exception
    except: 
        print("Invalid move!")
        sleep(1)
    else:
        turn = not turn
