from pynput.keyboard import Key, Listener
from os import system, name
from time import sleep

class Menu:
    def __init__(self, title, options):
        self.options = options
        self.title = title
        self.menucp = self.__menu()

    def __clearscreen(self):
        if name == 'nt': system('cls')
        else: system('clear')

    def __menu(self):
        pointer = 0

        def print_options():
            self.__clearscreen()

            print(self.title)
            for i in range(len(self.options)):
                print(end='>') if i == pointer else print(end=' ')
                print(' ' + self.options[i], ' '*(len(max(self.options, key=len)) - len(self.options[i])),end='')
                print('<') if i == pointer else print()


        def shift_pointer(shift):
            nonlocal pointer
            pointer = (pointer + shift) % len(self.options)
            if pointer <= 0: pointer = 0
            elif pointer >= len(self.options): pointer = len(self.options) - 1

        def call_page():
            return pointer

        return [print_options, shift_pointer, call_page]

    def __on_key_updown(self, key):
        if key == Key.up: self.menucp[1](-1)
        elif key == Key.down: self.menucp[1](1)
        elif key == Key.enter: 
            input()
            return False
        self.menucp[0]()

    def run(self):
        self.menucp[0]()
        sleep(0.1)
        with Listener(on_release=self.__on_key_updown) as listener:
            listener.join()
        return self.menucp[2]()
