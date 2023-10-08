from datetime import datetime
from os import path
import random
import json
from time import sleep
from errors import *
from osCompat import *
from boardState import BoardState
from clear import clr
from sound import sound
from player import Player
from game import Game, board

board = BoardState()

class Pvp:
    def __init__(self, time, turn, load, settings):
        self.x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.then = 0
        self.now = 0
        self.time = time
        self.inc = [0, 0]
        self.turn = turn
        self.load = load
        self.preview = False
        self.legacy = settings['legacy']
        self.fixed_board = settings['fixed_board']
        self.fixed_axis = settings['fixed_axis']
        self.idle_compat = settings['idle_compat']
        self.board_sound = settings['board_sound']

    def __loadGame(self):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games', self.load]),'r') as file:
            data = json.load(file)
            moves = data["moves"].split()

        fixed_axis = self.fixed_axis
        self.fixed_axis, self.fixed_board = False, False
        self.time = [data["wtime"], data["btime"]]
        self.p1 = Player(data["white"], 'W', None)
        self.p2 = Player(data["black"], 'B', None)

        for i in moves:
            self.__makemove(i)
            self.turn = not self.turn

        board.loadGame(' '.join([str(i) for i in moves]) + ' ')
        self.fixed_axis = fixed_axis

    def __saveGame(self, move):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(["..","data","games", move[5:]+'.json']).lstrip(), 'w') as file:
            lines = {
                "moves": board.getMoveHistory(),
                "wtime": self.time[0],
                "btime": self.time[1],
                "white": self.p1.name if self.p1.col == 'W' else self.p2.name,
                "black": self.p1.name if self.p1.col == 'B' else self.p2.name
            }

            file.seek(0)
            json.dump(lines, file, indent=4)

    def __axisToPos(self, x, y):
        newpos = self.x_axis[x] + self.y_axis[y]*8 - 1
        if not self.fixed_board and (self.fixed_axis and not self.turn):
            newpos = 63 - newpos
        return newpos

    def __makemove(self, move):
        if not (move[0].isalpha and move[1].isdigit()): raise Exception
        self.preview = False
        board.unPreview()
        start_pos = self.__axisToPos(move[0], move[1])

        if len(move) == 2: 
            self.preview = True
            board.preview(start_pos)

        elif len(move) == 4 : 
            if not (move[2].isalpha and move[3].isdigit()): raise Exception
            end_pos = self.__axisToPos(move[2], move[3])
            if not self.fixed_board and (self.fixed_axis and not self.turn): 
                move = chr(201 - ord(move[0])) + str(9 - int(move[1])) + chr(201 - ord(move[2])) + str(9 - int(move[3]))
            board.makeMove(start_pos, end_pos, self.turn, move.lower())

        else: raise Exception

    def run(self):
        format_time = lambda s: ("{}:{}".format(s//60, s - (s//60)*60))
        time_offset = lambda x: (abs(len(self.p1.name) - len(self.p2.name))) if len(self.p1.name if self.p1.col == x else self.p2.name) < len(self.p1.name if self.p1.col != x else self.p2.name) else 0
        clr()
        print("Chess pvp")

        if self.load == False:
            self.p1 = Player(input("Player one: "), random.choice(['W', 'B']), None)
            self.p2 = Player(input("Player two: "), 'W' if self.p1.col == 'B' else 'B', None)
        else: self._load_game()

        then = now = 0
        
        while True:
            clr()
            print("Chess pvp")
            print("White: {}{} [{}]\nBlack: {}{} [{}]\n".format(
                    self.p1.name if self.p1.col == 'W' else self.p2.name, 
                    ' '*time_offset('W'), 
                    format_time(self.time[0]),
                    self.p1.name if self.p1.col == 'B' else self.p2.name,
                    ' '*time_offset('B'), 
                    format_time(self.time[1])
                )
            )
          
            board.printBoard(self.legacy, self.turn, self.fixed_board, self.fixed_axis)

            print("\nCommands:")
            print(" back\n restart\n save: <file name>\n <move>: eg - b1a3, b1\n")

            if self.time[0] <= 0:
                print('\nBlack ran out of time!')
                print(self.p1.name if self.p1.col != 'B' else self.p2.name, "wins!")
                break
            
            if self.time[1] <= 0:
                print('\nWhite ran out of time!')
                print(self.p1.name if self.p1.col != 'W' else self.p2.name, "wins!")
                break

            now = int(datetime.now().timestamp())
            if self.turn: move = input("White's turn: ").lower() #input
            else: move = input("Black's turn: ").lower()
            then = int(datetime.now().timestamp())

            self.time[int(not self.turn)] -= then - now - self.inc[int(not self.turn)]

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
                    if len(move) == 5: raise UnNamedFile

                    self.__saveGame(move)

                    board.restart()
                    return

                self.__makemove(move)

            except InvalidMove as e: print("Invalid Move:", e, "cannot move there")
            except IllegalMove: print("Check!")
            except OpponentsPiece: print("Cannot move opponent's piece")
            except EmptyBox: print("There is no piece there")
            except CaptureOwnPiece: print("Cannot capture your own piece")
            except UnNamedFile: print("File name is required")
            except InvalidPromotionInput: print("Invalid piece: Use Q, B, N, R")
            except CheckMate: break
            except StaleMate: break
            except Exception as e: print("Invalid Input: "+str(e)+"!")

            else:
                if not self.preview: 
                    self.turn = not self.turn
                    board.unPreview()
                continue
            sleep(3)
            self.time[int(not self.turn)] -= 3

        board.restart()
        del self.p1, self.p2

        # Game results here
        print("\nPress any key to continue")
