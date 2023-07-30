from piece import Piece
from checkmove import Checkmove

piece = Piece
checkmove = Checkmove()

class Boardstate:
    def __init__(self):
        self._board = [None]*64
        self._board[0] = piece('R',0,5,'B')
        self._board[1] = piece('N',1,3.2,'B')
        self._board[2] = piece('B',2,3.3,'B')
        self._board[3] = piece('Q',3,9,'B')
        self._board[4] = piece('K',4,200,'B')
        self._board[5] = piece('B',5,3.3,'B')
        self._board[6] = piece('N',6,3.2,'B')
        self._board[7] = piece('R',7,5,'B')
        self._board[63-0] = piece('R',0,5,'W')
        self._board[63-1] = piece('N',1,3.2,'W')
        self._board[63-2] = piece('B',2,3.3,'W')
        self._board[63-3] = piece('K',3,200,'W')
        self._board[63-4] = piece('Q',4,9,'W')
        self._board[63-5] = piece('B',5,3.3,'W')
        self._board[63-6] = piece('N',6,3.2,'W')
        self._board[63-7] = piece('R',7,5,'W')

        for i in range(8,16):
            self._board[i] = piece('P',i,1,'B')
        for i in range(48,56):
            self._board[i] = piece('P',i,1,'W')

        for i in range(16,48):
            self._board[i] = piece('E',i,0,'N')

    def printboard(self):
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

    def makemove(self, startpos, endpos, turn):
        is_same_colour =  self._board[endpos].col == self._board[startpos].col
        is_empty_space = self._board[startpos].col == 'N'
        is_valid_move = checkmove.check(startpos, endpos, self._board) != -1
        is_correct_piece = True if turn == (self._board[startpos].col == 'W') else False

        if  is_same_colour or is_empty_space or  not (is_valid_move or is_correct_piece):
            return -1
        elif self._board[endpos].col == 'N':
            self._board[endpos] = self._board[startpos]
            self._board[startpos] = piece('E',startpos,0,'N')
        else:
            self._board[startpos], self._board[endpos] = self._board[endpos], self._board[startpos]
        return 0
