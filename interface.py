#!/usr/bin/env python3

from boardstate import Boardstate
from singleplayer import Singleplayer_menu
from multiplayer import Multiplayer_menu
from os import system, name
from time import sleep
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key
import argparse

parser = argparse.ArgumentParser(description='Simple chess game')
parser.add_argument('--legacy',action='store_true',default=False)
parser.add_argument('-t',type=int,default=600)
parser.add_argument('-i',type=int,default=0)
parser.add_argument('-o',type=int,default=2)

args = parser.parse_args()

board = Boardstate()
simpleplayer = Singleplayer_menu()
multiplayer = Multiplayer_menu()

x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

then = 0
now = 0

time = [args.t,args.t]
inc = [args.i, args.i]

turn = True
legacy = args.legacy

pointer = 0

options = [' Single player',' Multiplayer',' Exit']

def makemove(move):
    startpos = x_axis[move[0]] + y_axis[move[1]]*8 - 1
    endpos = x_axis[move[2]] + y_axis[move[3]]*8 - 1

    is_valid_input = (move[0: 3: 2].isalpha() and move[1: 4: 2].isnumeric()) == (len(move) == 4)
    if not is_valid_input or board.makemove(startpos, endpos, turn, move, legacy) == -1: raise Exception

def clearscreen():
    if name == 'nt': system('cls')
    else: system('clear')

def menu():
    clearscreen()
    global pointer

    print('Welcome to Chess!')
    for i in range(len(options)):
        if i == pointer: print(end='>')
        else: print(end=' ')
        print(options[i])

# 0 - Single player
# 1 - Mulitplayer
# 2 - Exit
def page(option): 
    if option == 0: pass
    elif option == 1: pass
    elif option == 2: exit(0)

def on_key_updown(key):
    global pointer

    if key == Key.up: pointer = (pointer - 1) % len(options)
    elif key == Key.down: pointer = (pointer + 1) % len(options)
    elif key == Key.enter: page(pointer)

    if pointer <= 0: pointer = 0
    elif pointer >= len(options): pointer = len(options) - 1

    menu()

menu()

if args.o == 2:
    with keyboard.Listener(on_release = on_key_updown) as listener:
        listener.join()
else:
    page(args.o)

while True:
    clearscreen()
    board.printboard(legacy)
    time[int(not turn)] -= then - now - inc[int(not turn)]

    print("Time spent:", then-now)
    print("Time left :", time[int(not turn)])

    if time[0] <= 0:
        print('Black ran out of time!')
        break
    
    if time[1] <= 0:
        print('White ran out of time!')
        break

    now = int(datetime.now().timestamp())

    if turn: move = input("White's turn: ").lower()
    else: move = input("Black's turn: ").lower()
    then = int(datetime.now().timestamp())

    try:
        if move == 'restart':
            board.restart()
            time = [600, 600]
            turn = True
            continue

        if move == 'save':
            clearscreen()
            file = open(input('Enter the filename to save the game in: '), 'w')
            file.write(board.getMoveHistory())
            continue

        if move == 'load':
            clearscreen()
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

