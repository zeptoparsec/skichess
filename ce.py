class piece:
    def __init__(self, name, pos, val, col) -> None:
        self.name = name
        self.pos = pos
        self.val = val
        self.col = col

class boardstate:
    def __init__(self) -> None:
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

    def __convertto_pos(self, move):
        x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

        startpos = x_axis[move[0]]+y_axis[move[1]]*8-1
        endpos = x_axis[move[2]]+y_axis[move[3]]*8-1

        return (startpos, endpos)

    def makemove(self, startpos, endpos):
        #startpos = self.__convert_pos(startpos)
        #endpos = self.__convert_pos(endpos)

        if self._board[endpos].col == self._board[startpos].col or self._board[startpos].col == 'N':
            return -1
        elif self._board[endpos].col != 'N':
            self._board[endpos] = self._board[startpos]
            self._board[startpos] = piece('E',startpos,0,'N')
        else:
            self._board[startpos], self._board[endpos] = self._board[endpos], self._board[startpos]
            # Maybe do some move validation here?
        return 0
    def ucimakemove(self, move):
        pos = self.__convertto_pos(move)
        self.makemove(pos[0],pos[1])
    
board = boardstate()
#a7 - a6
board.ucimakemove('e2e3')
board.printboard()
