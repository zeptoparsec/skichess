from errors import *
from piece import Piece
from checkmove import Checkmove

class Boardstate:
    def __init__(self):
        self.__board = [Piece('E',0,0,'N',[])]*64
        self.__board[0] = Piece('R',0,5,'B',[])
        self.__board[1] = Piece('N',1,3.2,'B',[])
        self.__board[2] = Piece('B',2,3.3,'B',[])
        self.__board[3] = Piece('Q',3,9,'B',[])
        self.__board[4] = Piece('K',4,200,'B',[])
        self.__board[5] = Piece('B',5,3.3,'B',[])
        self.__board[6] = Piece('N',6,3.2,'B',[])
        self.__board[7] = Piece('R',7,5,'B',[])
        self.__board[63-0] = Piece('R',0,5,'W',[])
        self.__board[63-1] = Piece('N',1,3.2,'W',[])
        self.__board[63-2] = Piece('B',2,3.3,'W',[])
        self.__board[63-3] = Piece('K',3,200,'W',[])
        self.__board[63-4] = Piece('Q',4,9,'W',[])
        self.__board[63-5] = Piece('B',5,3.3,'W',[])
        self.__board[63-6] = Piece('N',6,3.2,'W',[])
        self.__board[63-7] = Piece('R',7,5,'W',[])

        for i in range(8,16):
            self.__board[i] = Piece('P',i,1,'B', [0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5,  5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5,-10,  0,  0,-10, -5,  5, 5, 10, 10,-20,-20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0])

        for i in range(48,56):
            self.__board[i] = Piece('P',i,1,'W',[0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5,  5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5,-10,  0,  0,-10, -5,  5, 5, 10, 10,-20,-20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0])

        for i in range(16,48):
            self.__board[i] = Piece('E',i,0,'N',[])

        self.__movehistory = ''

    def printboard(self, legacy, turn, fixed_board, fixed_axis):
        if legacy:
            pieces = {
                'PW': 'P', 'RW': 'R', 'NW': 'N', 'BW': 'B', 'KW': 'K', 'QW': 'Q',
                'PB': 'p', 'RB': 'r', 'NB': 'n', 'BB': 'b', 'KB': 'k', 'QB': 'q',
                'EN': ' ', 'HN': '*'
            }
        else:
            pieces = {
                'PW': '♟', 'RW': '♜', 'NW': '♞', 'BW': '♝', 'KW': '♚', 'QW': '♛',
                'PB': '♙', 'RB': '♖', 'NB': '♘', 'BB': '♗', 'KB': '♔', 'QB': '♕',
                'EN': ' ', 'HN': '*'
            }
        
        for i in range(8):
            if fixed_axis or fixed_board: print(8-i,end=' ')
            else: 
                if turn:
                    print(8-i,end=' ')
                else:
                    print(i+1,end=' ')
            for j in range(8):
                if turn or fixed_board:
                    print(pieces[self.__board[8*i+j].name+self.__board[8*i+j].col], end=' ')
                else:
                    print(pieces[self.__board[63-8*i-j].name+self.__board[63-8*i-j].col], end=' ')
            print()
        print(end='  ')
        for i in range(1,9):
            if fixed_axis or fixed_board: print(chr(64+i),end=' ')
            else: 
                if turn:
                    print(chr(64+i),end=' ')
                else:
                    print(chr(73-i),end=' ')
        print()

    def restart(self):
        self.__init__()

    def __move(self, startpos, endpos, move):
        if self.__board[startpos].moved: self.__board[startpos].moved_again = True
        else: self.__board[startpos].moved = True

        self.__board[endpos] = self.__board[startpos]
        self.__board[startpos] = Piece('E',startpos,0,'N',[])

        if move != None: self.__movehistory += move+' '

    def preview(self, pos):
        checkmove = Checkmove(self.__board)
        if self.__board[pos].col == 'N': raise EmptyBox
        poses = checkmove.preview(pos)
        for i in poses:
            if self.__board[i].col == 'N': self.__board[i] = Piece('H', i, 0, 'N', [])
    
    def unpreview(self):
        for i in range(64):
            if self.__board[i].name == 'H' and self.__board[i].col == 'N':
                self.__board[i] = Piece('E', i ,0 , 'N', [])


    def makemove(self, startpos, endpos, turn, move):
        checkmove = Checkmove(self.__board)
    
        is_same_colour =  self.__board[endpos].col == self.__board[startpos].col
        is_empty_space = self.__board[startpos].col == 'N'
        is_correct_piece = True if turn == (self.__board[startpos].col == 'W') else False
    
        if is_empty_space: raise EmptyBox
        elif not is_correct_piece: raise OpponentsPiece
        elif is_same_colour: raise CaptureOwnPiece

        move_type = checkmove.validate(startpos, endpos)
        if move_type == "promotion":
            promo = input("Promote to: ").upper()
            if promo not in "QBNR": raise InvalidPromotionInput
    
            self.__move(startpos, endpos, move)
            self.__board[endpos].name = promo
            self.__board[endpos].val = 9 if promo == 'Q' else 5 if promo == 'R' else 3.3 if promo == 'B' else 3.2
            return
            
        elif move_type == "enpassant":
            killpos = endpos + (8 if self.__board[startpos].col == 'W' else -8)
            self.__move(startpos, endpos, move)
            self.__board[killpos] = Piece('E',startpos,0,'N',[])
            return

        elif move_type == "castling":
            offset = 0 if self.__board[startpos].col == 'B' else 56
            self.__move(startpos, endpos, move)
            if endpos == 1 + offset:
                startpos = 0 + offset
                endpos = 2 + offset
            elif endpos == 6 + offset:
                startpos = 7 + offset
                endpos = 5 + offset
            self.__move(startpos, endpos, None)
            return
            
        self.__move(startpos, endpos, move)
        return

    def getMoveHistory(self):
        return self.__movehistory

    def loadGame(self, movehistory):
        self.__movehistory = movehistory

    def boardval(self):
        res = 0
        for i in self.__board:
            if i.col == 'W': res += i.val
            elif i.col == 'B': res -= i.val
        return res
