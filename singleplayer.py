from datetime import datetime
from os import name, system
import random
from time import sleep
from boardstate import Boardstate
from player import Player

board = Boardstate()

class Singleplayer_pvp:
    
    def __init__(self, time, inc, turn, legacy):
        self.x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.then = 0
        self.now = 0

        self.time = time
        self.inc = inc

        self.turn = turn
        self.legacy = legacy
        
    def clearscreen(self):
        if name == 'nt': system('cls')
        else: system('clear')

    def makemove(self, move):
        startpos = self.x_axis[move[0]] + self.y_axis[move[1]]*8 - 1
        endpos = self.x_axis[move[2]] + self.y_axis[move[3]]*8 - 1

        is_valid_input = (move[0: 3: 2].isalpha() and move[1: 4: 2].isnumeric()) == (len(move) == 4)
        if not is_valid_input or board.makemove(startpos, endpos, self.turn, move, self.legacy) == -1: raise Exception

    def run(self):
        board.restart()

        input()
        self.clearscreen()
        print("Chess pvp")

        p1 = Player(input("Player one: "), random.choice(['W', 'B']), None)
        p2 = Player(input("Player two: "), 'W' if p1.col == 'B' else 'B', None)
        then = now = 0

        while True:
            self.clearscreen()
            print("Chess pvp")
            print(p1.name + ":", "White" if p1.col == 'W' else "Black")
            print(p2.name + ":", "White" if p2.col == 'W' else "Black")
            print()

            board.printboard(self.legacy)
            self.time[int(not self.turn)] -= then - now - self.inc[int(not self.turn)]

            print()
            print("Time spent:", then-now)
            print("Time left :", self.time[int(not self.turn)])

            if self.time[0] <= 0:
                print('Black ran out of time!')
                print(p2.name, "wins!")
                break
            
            if self.time[1] <= 0:
                print('White ran out of time!')
                print(p1.name, "wins!")
                break

            now = int(datetime.now().timestamp())

            if self.turn: move = input("White's turn: ").lower()
            else: move = input("Black's turn: ").lower()
            then = int(datetime.now().timestamp())

            try:
                if move == 'back': return

                if move == 'restart':
                    board.restart()
                    self.time = [600, 600]
                    self.turn = True
                    continue

                if move == 'legacy':
                    print('Legacy')
                    self.legacy = True
                    board.restart()
                    self.time = [600, 600]
                    self.turn = True
                    continue

                if move == 'save':
                    self.clearscreen()
                    file = open(input('Enter the filename to save the game in: '), 'w')
                    file.write(board.getMoveHistory())
                    continue

                if move == 'load':
                    self.clearscreen()
                    game = open(input('Enter the file to load the game from: '),'r').read()
                    self.turn = True

                    for i in game.split():
                        self.makemove(i)
                        self.turn = not self.turn

                    board.loadGame(game)
                    self.time = [600,600]
                    continue

                self.makemove(move)
            except:
                print("Invalid move!")
                sleep(1)
            else:
                self.turn = not self.turn
        print("Press any key to continue")
