from piece import Piece
from checkmove import Checkmove
from time import sleep
from os import system, name

class Boardstate:
    def __init__(self):
        self._board = [Piece('E',0,0,'N',[])]*64
        self._board[0] = Piece('R',0,5,'B',[])
        self._board[1] = Piece('N',1,3.2,'B',[])
        self._board[2] = Piece('B',2,3.3,'B',[])
        self._board[3] = Piece('Q',3,9,'B',[])
        self._board[4] = Piece('K',4,200,'B',[])
        self._board[5] = Piece('B',5,3.3,'B',[])
        self._board[6] = Piece('N',6,3.2,'B',[])
        self._board[7] = Piece('R',7,5,'B',[])
        self._board[63-0] = Piece('R',0,5,'W',[])
        self._board[63-1] = Piece('N',1,3.2,'W',[])
        self._board[63-2] = Piece('B',2,3.3,'W',[])
        self._board[63-3] = Piece('K',3,200,'W',[])
        self._board[63-4] = Piece('Q',4,9,'W',[])
        self._board[63-5] = Piece('B',5,3.3,'W',[])
        self._board[63-6] = Piece('N',6,3.2,'W',[])
        self._board[63-7] = Piece('R',7,5,'W',[])

        for i in range(8,16):
            self._board[i] = Piece('P',i,1,'B', [0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5,  5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5,-10,  0,  0,-10, -5,  5, 5, 10, 10,-20,-20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0])

        for i in range(48,56):
            self._board[i] = Piece('P',i,1,'W',[0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5,  5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5,-10,  0,  0,-10, -5,  5, 5, 10, 10,-20,-20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0])

        for i in range(16,48):
            self._board[i] = Piece('E',i,0,'N',[])

        self._movehistory = ''

    def printboard(self, legacy):
        if legacy:
            pieces = {'PW': 'P', 'RW': 'R', 'NW': 'N', 'BW': 'B', 'KW': 'K', 'QW': 'Q', 'EN' : ' ',
           'PB': 'p', 'RB': 'r', 'NB': 'n', 'BB': 'b', 'KB': 'k', 'QB': 'q'}
        else:
            pieces = {'PW': '♟', 'RW': '♜', 'NW': '♞', 'BW': '♝', 'KW': '♚', 'QW': '♛', 'EN' : ' ',
           'PB': '♙', 'RB': '♖', 'NB': '♘', 'BB': '♗', 'KB': '♔', 'QB': '♕'}
        
        for i in range(8):
            print(8-i,end=' ')

            for j in range(8):
                print(pieces[self._board[8*i+j].name+self._board[8*i+j].col], end=' ')
            print()
        print(end='  ')
        for i in range(1,9):
            print(chr(64+i),end=' ')
        print()

    def restart(self):
        self.__init__()

    def __move(self, startpos, endpos, move):
        if self._board[endpos].col != 'N':
            self._board[endpos] = self._board[startpos]
            self._board[startpos] = Piece('E',startpos,0,'N',[])
        else:
            self._board[startpos], self._board[endpos] = self._board[endpos], self._board[startpos]

        self._board[endpos].moved = True
        if self._board[startpos].name == 'P' and self._board[startpos].moved: 
            self._board[startpos].moved_again = True

        if move != None: self._movehistory += move+' '

    def makemove(self, startpos, endpos, turn, move):
        checkmove = Checkmove(self._board) # I don't want to do this...
    
        is_same_colour =  self._board[endpos].col == self._board[startpos].col
        is_empty_space = self._board[startpos].col == 'N'
        move_type = checkmove.check(startpos, endpos)
        is_correct_piece = True if turn == (self._board[startpos].col == 'W') else False
    
        if is_same_colour or is_empty_space or not is_correct_piece or move_type == False:
            self._movehistory = self._movehistory[0:len(self._movehistory)-5]
            return -1
        elif move_type == "promotion":
            while True: 
                promo = input("Promote to: ").upper()
                if promo in 'QBNR': break

                print("Invalid piece!")
                sleep(1)
                if name == 'nt': system('cls')
                else: system('clear')
                self.printboard(False)
    
            self.__move(startpos, endpos, move)
            self._board[endpos].name = promo
            self._board[endpos].val = 9 if promo == 'Q' else 5 if promo == 'R' else 3.3 if promo == 'B' else 3.2 #wow thats long
            return 0

        elif move_type == "enpassant":
            #execute enpassant
            return 0
        elif move_type == "castling":
            offset = 0 if self._board[startpos].col == 'B' else 56
            self.__move(startpos, endpos, move)
            if endpos == 1 + offset:
                startpos = 0 + offset
                endpos = 2 + offset
            elif endpos == 6 + offset:
                startpos = 7 + offset
                endpos = 5 + offset
            self.__move(startpos, endpos, None)
            return 0
            
        self.__move(startpos, endpos, move)
        return 0 

    def getMoveHistory(self):
        return self._movehistory

    def loadGame(self, movehistory):
        self._movehistory = movehistory

    def boardval(self):
        res = 0
        for i in self._board:
            if i.col == 'W':
                res += i.val
            elif i.col == 'B':
                res -= i.val
        return res
