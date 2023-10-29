from pynput.keyboard import Key, Listener
from compat.clear import clr
from time import sleep
from engine.settings import settings
from ui.sound import sound

def menu(title, options, setpointer):
    pointer = setpointer

    def print_options():
        clr()

        print(title)
        for i in range(len(options)):
            print(end='>') if i == pointer else print(end=' ')
            print(' ' + options[i], ' '*(len(max(options, key=len)) - len(options[i])),end='')
            print('<') if i == pointer else print()

    def shift_pointer(shift):
        nonlocal pointer
        pointer = (pointer + shift) % len(options)
        if pointer <= 0: pointer = 0
        elif pointer >= len(options): pointer = len(options) - 1

    def call_page():
        return pointer

    return [print_options, shift_pointer, call_page]

def on_key_updown(key):
    if key == Key.up:
        menucp[1](-1)
        sound.menuSelect()
    elif key == Key.down:
        menucp[1](1)
        sound.menuSelect()
    elif key == Key.enter: 
        if not settings.active_settings["idle_compat"]:
            input()
        sound.menuEnter()
        return False

    menucp[0]()

def run(title, options, pointer):
    global menucp
    menucp = menu(title, options, pointer)

    menucp[0]()
    sleep(0.1)
    with Listener(on_release=on_key_updown) as listener:
        listener.join()
    return menucp[2]()
