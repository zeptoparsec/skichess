from boardstate import Boardstate
from os import system
from time import sleep

board = Boardstate()

turn = True
while True:
    system('cls')
    board.printboard()
    if turn:
        move = input("White's turn: ").lower()
    else:
        move = input("Black's turn: ")

    try:
        board.ucimakemove(move)
    except: 
        print("Invalid move!\n")
        sleep(1)
    else:
        turn = not turn
