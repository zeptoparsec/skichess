from datetime import datetime
import random
from time import sleep
from engine.errors import *
from compat.osCompat import *
from compat.clear import clr
from engine.player import Player
from engine.game import Game, board
from pynput.keyboard import Listener

class Pvp(Game):
    def __print(self):
        clr()
        print("Chess pvp")
        print("White: {}{} {}\nBlack: {}{} {}\n".format(
                self.p1.name if self.p1.col == 'W' else self.p2.name, 
                ' '*self._time_offset('W'), 
                self._format_time(self.time[0]),
                self.p1.name if self.p1.col == 'B' else self.p2.name,
                ' '*self._time_offset('B'), 
                self._format_time(self.time[1])
            )
        )
    
        board.printBoard(self.legacy, self.turn, self.fixed_board, self.fixed_axis)

        print("\nCommands:")
        print(" back\n restart\n resign\n draw\n save: <file name>\n <move>: eg - b1a3, b1, h\n")

    def run(self):
        winner = None
        clr()
        print("Chess pvp")

        if self.load == False:
            self.p1 = Player(input("Player one: "), random.choice(['W', 'B']))
            self.p2 = Player(input("Player two: "), 'W' if self.p1.col == 'B' else 'B')
        else: self._loadGame()

        then = now = 0
        
        while True:
            self.__print()

            if self.time[0] <= 0:
                print('\nBlack ran out of time!')
                raise TimeOut("White")
            
            if self.time[1] <= 0:
                print('\nWhite ran out of time!')
                raise TimeOut("Black")

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

                if move == 'resign':
                    end_game_type = 'resign'
                    winner = 'White' if not self.turn else 'Black'
                    break

                if move == 'draw':
                    print('Draw requested!')
                    choice = input('(y/n): ').lower()
                    if choice == 'y':
                        end_game_type = 'draw'
                        break
                    continue

                if move.__contains__('save:'): 
                    if len(move) == 5: raise UnNamedFile
                    self._saveGame(move)
                    board.restart()
                    return

                self._makeMove(move)

            except InvalidMove as e: print("Invalid Move:", e, "cannot move there")
            except OpponentsPiece: print("Cannot move opponent's piece")
            except OpponentPreview: print("Cannot preview opponent's piece")
            except EmptyBox: print("There is no piece there")
            except CaptureOwnPiece: print("Cannot capture your own piece")
            except UnNamedFile: print("File name is required")
            except InvalidPromotionInput: print("Invalid piece: Use Q, B, N, R")
            except Check: print("Check!")
            except Checkmate as e: 
                end_game_type = 'checkmate'
                winner = e
                break
            except Stalemate as e:
                end_game_type = 'stalemate'
                break
            except TimeOut as e:
                end_game_type = 'timeout'
                winner = e
                break
            except Exception: 
                print("Invalid input!")
            else:
                if not self.preview: 
                    self.turn = not self.turn
                continue
            sleep(3)
            self.time[int(not self.turn)] -= 3

        self.__print()
        board.restart()

        match end_game_type:
            case 'checkmate':
                print(f"Checkmate!\n{winner} wins!")
            case 'stalemate':
                print("Stalemate!\nDraw!")
            case 'time':
                print(f"Time Up!\n{winner} wins!")
            case 'resign':
                print(f"{'Black' if winner == 'White' else 'White'} resigned\n{winner} wins!")
            case 'draw':
                print("Draw!")
        
        print("\nPress any key to continue")
        with Listener(on_press=lambda key: False) as listener:
            listener.join()
