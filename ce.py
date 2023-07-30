from boardstate import Boardstate
from os import system
from time import sleep

board = Boardstate()

def switch_turn(turn):
    if turn == 'w': return 'b'
    else: return 'w'

turn = "w"
while True:
    system('cls')
    board.printboard()
    if turn == 'w': move = input("White's turn: ").lower()
    else: move = input("Black's turn: ")

    try: board.ucimakemove(move)
    except: 
        print("Invalid move!\n")
        sleep(1)
    else: turn = switch_turn(turn)
