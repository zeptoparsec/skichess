#!/usr/bin/env python3

from pvp import Pvp
from pvp_lan import Pvp_lan_menu
from os import system, name
from pynput import keyboard
from pynput.keyboard import Key
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Simple chess game')
parser.add_argument('-o',type=int,default=2)
args = parser.parse_args()

def clearscreen():
    if name == 'nt': system('cls')
    else: system('clear')

def menu():
    pointer = 0
    options = [' Single player',' Multiplayer',' Exit']

    def print_options():
        clearscreen()

        print('Welcome to Chess!')
        for i in range(len(options)):
            print(end='>') if i == pointer else print(end=' ')
            print(options[i], ' '*(len(max(options)) - len(options[i])),end='')
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
    if option == 0: Pvp().run()
    elif option == 1: Pvp_lan_menu().run()
    elif option == 2: exit()
    sleep(0.5)

menucp = menu()
menucp[0]()

def on_key_updown(key):
    if key == Key.up: menucp[1](-1)
    elif key == Key.down: menucp[1](1)
    elif key == Key.enter: menucp[2]()
    menucp[0]()

if args.o == 2:
    with keyboard.Listener(on_release=on_key_updown) as listener:
        listener.join()
else: page(args.o)
