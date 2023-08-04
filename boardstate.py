from piece import Piece
from checkmove import Checkmove

class Boardstate:
    def __init__(self):
        self._board = [Piece('E',0,0,'N')]*64
        self._board[0] = Piece('R',0,5,'B')
        self._board[1] = Piece('N',1,3.2,'B')
        self._board[2] = Piece('B',2,3.3,'B')
        self._board[3] = Piece('Q',3,9,'B')
        self._board[4] = Piece('K',4,200,'B')
        self._board[5] = Piece('B',5,3.3,'B')
        self._board[6] = Piece('N',6,3.2,'B')
        self._board[7] = Piece('R',7,5,'B')
        self._board[63-0] = Piece('R',0,5,'W')
        self._board[63-1] = Piece('N',1,3.2,'W')
        self._board[63-2] = Piece('B',2,3.3,'W')
        self._board[63-3] = Piece('K',3,200,'W')
        self._board[63-4] = Piece('Q',4,9,'W')
        self._board[63-5] = Piece('B',5,3.3,'W')
        self._board[63-6] = Piece('N',6,3.2,'W')
        self._board[63-7] = Piece('R',7,5,'W')

        for i in range(8,16):
            self._board[i] = Piece('P',i,1,'B')

        for i in range(48,56):
            self._board[i] = Piece('P',i,1,'W')

        for i in range(16,48):
            self._board[i] = Piece('E',i,0,'N')

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

    def makemove(self, startpos, endpos, turn, move):
        checkmove = Checkmove(self._board) # I don't want to do this...

        is_same_colour =  self._board[endpos].col == self._board[startpos].col
        is_empty_space = self._board[startpos].col == 'N'
        is_valid_move = checkmove.check(startpos, endpos)
        is_correct_piece = True if turn == (self._board[startpos].col == 'W') else False

        if is_same_colour or is_empty_space or not (is_correct_piece and is_valid_move):
            self._movehistory = self._movehistory[0:len(self._movehistory)-5]
            return -1
        elif is_valid_move == "promotion":
            pass
        elif is_valid_move == "enpassant":
            pass
        elif is_valid_move == "castling":
            pass
        elif self._board[endpos].col != 'N':
            self._board[endpos] = self._board[startpos]
            self._board[startpos] = Piece('E',startpos,0,'N')
        else:
            self._board[startpos], self._board[endpos] = self._board[endpos], self._board[startpos]
        
        self._board[endpos].moved = True

        self._movehistory += move+' '
        return 0
