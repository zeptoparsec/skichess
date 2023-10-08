from datetime import datetime
import random
from time import sleep
from errors import *
from osCompat import *
from clear import clr
from player import Player
from game import Game, board

class Pvp(Game):
    def run(self):
        format_time = lambda s: ("{}:{}".format(s//60, s - (s//60)*60))
        time_offset = lambda x: (abs(len(self.p1.name) - len(self.p2.name))) if len(self.p1.name if self.p1.col == x else self.p2.name) < len(self.p1.name if self.p1.col != x else self.p2.name) else 0
        clr()
        print("Chess pvp")

        if self.load == False:
            self.p1 = Player(input("Player one: "), random.choice(['W', 'B']), None)
            self.p2 = Player(input("Player two: "), 'W' if self.p1.col == 'B' else 'B', None)
        else: self._loadGame()

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

                    self._saveGame(move)

                    board.restart()
                    return

                self._makeMove(move)

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
