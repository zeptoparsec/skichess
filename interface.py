#!/usr/bin/env python3

from boardstate import Boardstate
from singleplayer import Singleplayer_pvp
from multiplayer import Pvp_lan_menu
from os import system, name
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
singleplayer = Singleplayer_pvp([args.t,args.t],[args.i, args.i],True,args.legacy)
multiplayer = Pvp_lan_menu()

def clearscreen():
    if name == 'nt': system('cls')
    else: system('clear')

def menu():
    pointer = 0
    options = [' Single player',' Multiplayer',' Exit']
    max_option_len = len(max(options))

    def print_options():
        clearscreen()

        print('Welcome to Chess!')
        for i in range(len(options)):
            print(end='>') if i == pointer else print(end=' ')
            print(options[i], ' '*(max_option_len - len(options[i])),end = ' ')
            print('<') if i == pointer else print()


    def shift_pointer(shift):
        nonlocal pointer

        pointer = (pointer + shift) % len(options)

        if pointer <= 0: pointer = 0
        elif pointer >= len(options): pointer = len(options) - 1

    def call_page():
        page(pointer)

    return [print_options, shift_pointer, call_page]

# 0 - Single player
# 1 - Mulitplayer
# 2 - Exit
def page(option): 
    if option == 0: singleplayer.run()
    elif option == 1: pass
    elif option == 2: exit(0)

menucp = menu()

def on_key_updown(key):
    if key == Key.up: menucp[1](-1)
    elif key == Key.down: menucp[1](1)
    elif key == Key.enter: menucp[2]()

    menucp[0]()

menucp[0]()

if args.o == 2:
    with keyboard.Listener(on_release=on_key_updown) as listener:
        listener.join()
else:
    page(args.o)
