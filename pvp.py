from datetime import datetime
from os import name, system, path
import random
from time import sleep
from boardstate import Boardstate
from player import Player

board = Boardstate()

class Pvp:
    
    def __init__(self, time, turn, load, legacy):
        self.x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.then = 0
        self.now = 0
        self.time = time
        self.inc = [0, 0]
        self.turn = turn
        self.legacy = legacy
        self.load = load
        
    def __clearscreen(self):
        if name == 'nt': system('cls')
        else: system('clear')

    def __makemove(self, move):
        startpos = self.x_axis[move[0]] + self.y_axis[move[1]]*8 - 1
        endpos = self.x_axis[move[2]] + self.y_axis[move[3]]*8 - 1

        is_valid_input = (move[0: 3: 2].isalpha() and move[1: 4: 2].isnumeric()) == (len(move) == 4)
        if not is_valid_input or board.makemove(startpos, endpos, self.turn, move, self.legacy) == -1: raise Exception

    def __load_game(self):
        game = open(path.dirname(path.abspath(__file__)) + "/cache/games/" + self.load,'r').read().split()
        self.turn = bool(game[-7])
        self.time = [int(game[-6]), int(game[-5])]
        self.p1 = Player(game[-3], game[-4], None)
        self.p2 = Player(game[-1], game[-2], None)
        del game[-7:]

        for i in game:
            self.__makemove(i)
            self.turn = not self.turn

        board.loadGame(' '.join([str(i) for i in game]) + ' ')

    def __validate_name(self):
        if self.p1.name == '': self.p1.name = '-'
        if self.p2.name == '': self.p2.name = '-'
        self.p1.name = self.p1.name.replace(' ', '_')
        self.p2.name = self.p2.name.replace(' ', '_')

    def run(self):
        self.__clearscreen()
        print("Chess pvp")

        if self.load == False:
            self.p1 = Player(input("Player one: "), random.choice(['W', 'B']), None)
            self.p2 = Player(input("Player two: "), 'W' if self.p1.col == 'B' else 'B', None)
        else: self.__load_game()

        self.__validate_name()
        then = now = 0
        while True:
            self.__clearscreen()
            print("Chess pvp")
            print(' ' + self.p1.name + ':', "White" if self.p1.col == 'W' else "Black")
            print(' ' + self.p2.name + ':', "White" if self.p2.col == 'W' else "Black")
            print()

            board.printboard(self.legacy)

            print()
            print("Commands:")
            print(" back\n restart\n save: <file name>\n <move>: eg - b1a3")

            self.time[int(not self.turn)] -= then - now - self.inc[int(not self.turn)]

            print()
            print("Time spent:", then-now)
            print("Time left :", self.time[int(not self.turn)])
            print()

            if self.time[0] <= 0:
                print('Black ran out of time!')
                print(self.p2.name, "wins!")
                break
            
            if self.time[1] <= 0:
                print('White ran out of time!')
                print(self.p1.name, "wins!")
                break

            now = int(datetime.now().timestamp())

            if self.turn: move = input("White's turn: ").lower()
            else: move = input("Black's turn: ").lower()
            then = int(datetime.now().timestamp())

            try:
                if move == 'back': 
                    board.restart()
                    del self.p1, self.p2
                    return

                if move == 'restart':
                    board.restart()
                    self.time = [600, 600]
                    self.turn = True
                    continue

                if move.__contains__('save:'): 
                    if len(move) == 5: raise Exception

                    file = open(path.dirname(path.abspath(__file__)) + "\\cache\\games\\" + move[5:].lstrip(), 'w')
                    lines = [board.getMoveHistory(),
                            str(self.turn) + ' ',
                            str(self.time[0]) + ' ',
                            str(self.time[1]) + ' ',
                            self.p1.col + ' ',
                            self.p2.name + ' ',
                            self.p2.col + ' ',
                            self.p1.name + ' ',
                    ]
                    file.writelines(lines)
                    file.close()

                    board.restart()
                    return

                self.__makemove(move)
            except:
                print("Invalid move!")
                sleep(1)
            else: self.turn = not self.turn

        board.restart()
        del self.p1, self.p2

        # Game results here
        print("\nPress any key to continue")
