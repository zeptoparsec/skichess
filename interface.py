from boardstate import Boardstate
from os import system, name
from time import sleep
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key

board = Boardstate()

x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

then = 0
now = 0

time = [600,600]
inc = [1,1]

turn = True
legacy = False

pointer = 0

options = [' New untimed Game',' New timed Game',' Load Game']

def makemove(move):
    startpos = x_axis[move[0]] + y_axis[move[1]]*8 - 1
    endpos = x_axis[move[2]] + y_axis[move[3]]*8 - 1

    is_valid_input = (move[0: 3: 2].isalpha() and move[1: 4: 2].isnumeric()) == (len(move) == 4)
    if not is_valid_input or board.makemove(startpos, endpos, turn, move, legacy) == -1: raise Exception

def clearscreen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

"""
def menu():
    global pointer

    print('Welcome to <nameless>!')
    for i in range(len(options)):
        if i == pointer:
            print(end='>')
        else:
            print(end=' ')
        print(options[i])

def on_key_updown(key):
    clearscreen()

    global pointer

    if key == Key.up:
        pointer -= 1
    elif key == Key.down:
        pointer += 1
    elif key == Key.enter:
        exit()

    if pointer <= 0:
        pointer = 0
    elif pointer >= len(options):
        pointer = len(options) - 1

    menu()

menu()

with keyboard.Listener(on_release=on_key_updown) as listener:
    listener.join()
"""

while True:
    clearscreen()

    board.printboard(legacy)

    time[int(not turn)] -= then - now - inc[int(not turn)]

    print("Time spent:",then-now)
    print("Time left :", time[int(not turn)])

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
            board.restart()
            time = [600, 600]
            turn = True

            continue

        if move == 'save':
            if name == 'nt':
                system('cls')
            else:
                system('clear')

            file = open(input('Enter the filename to save the game in: '), 'w')
            file.write(board.getMoveHistory())

            continue

        if move == 'load':
            if name == 'nt':
                system('cls')
            else:
                system('clear')

            game = open(input('Enter the file to load the game from: '),'r').read()

            turn = True

            for i in game.split():
                makemove(i)
                turn = not turn

            board.loadGame(game)

            time = [600,600]

            continue

        makemove(move)
    except:
        print("Invalid move!")
        sleep(1)
    else:
        turn = not turn
