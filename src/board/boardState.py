from engine.errors import *
from board.checkMove import CheckMove
from engine.settings import settings
from ui.sound import sound
from board.piece import Piece

class BoardState:
    def __init__(self):
        self.__board = [Piece('E', 0, 0, 'N')]*64
        self.__board[0] = Piece('R', 0, 5, 'B')
        self.__board[1] = Piece('N', 1, 3.2, 'B')
        self.__board[2] = Piece('B', 2, 3.3, 'B')
        self.__board[3] = Piece('Q', 3, 9, 'B')
        self.__board[4] = Piece('K', 4, 200, 'B')
        self.__board[5] = Piece('B', 5, 3.3, 'B')
        self.__board[6] = Piece('N', 6, 3.2, 'B')
        self.__board[7] = Piece('R', 7, 5, 'B')
        self.__board[63-0] = Piece('R', 63-0, 5, 'W')
        self.__board[63-1] = Piece('N', 63-1, 3.2, 'W')
        self.__board[63-2] = Piece('B', 63-2, 3.3, 'W')
        self.__board[63-3] = Piece('K', 63-3, 200, 'W')
        self.__board[63-4] = Piece('Q', 63-4, 9, 'W')
        self.__board[63-5] = Piece('B', 63-5, 3.3, 'W')
        self.__board[63-6] = Piece('N', 63-6, 3.2, 'W')
        self.__board[63-7] = Piece('R', 63-7, 5, 'W')

        for i in range(8,16):
            self.__board[i] = Piece('P', i, 1, 'B')

        for i in range(48,56):
            self.__board[i] = Piece('P', i, 1, 'W')

        for i in range(16,48):
            self.__board[i] = Piece('E', i, 0, 'N')

        self.__move_history = ''
        self.prev_end_pos = None

    def printBoard(self, legacy, turn, fixed_board, fixed_axis):
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
            if fixed_axis or fixed_board: 
                print(8-i,end=' ')
            else: 
                if turn: print(8-i,end=' ')
                else: print(i+1,end=' ')

            for j in range(8):
                if turn or fixed_board:
                    print(pieces[self.__board[8*i + j].name+self.__board[8*i + j].col], end=' ')
                else: 
                    print(pieces[self.__board[63 - 8*i - j].name+self.__board[63 - 8*i - j].col], end=' ')
            print()
        print(end='  ')

        for i in range(1,9):
            if fixed_axis or fixed_board: 
                print(chr(64 + i),end=' ')
            else: 
                if turn: print(chr(64 + i),end=' ')
                else: print(chr(73 - i),end=' ')
            if settings.active_settings['idle_compat']:
                print(end='  ')
        print()

        if self.__move_history == '':
            sound.boardStartGame()
            

    def restart(self):
        self.__init__()

    def convertPos(self, pos):
        pass

    def preview(self, pos, col):
        if self.__board[pos].col == 'N': 
            raise EmptyBox
        if self.__board[pos].col != col: 
            raise OpponentPreview

        self.__unPreview()
        for i in CheckMove(self.__board).preview(pos, self.prev_end_pos):
            if self.__board[i].col == 'N': self.__board[i] = Piece('H', i, 0, 'N')
        return True

    def __unPreview(self):
        for i in range(64):
            if self.__board[i].name == 'H' and self.__board[i].col == 'N':
                self.__board[i] = Piece('E', i ,0 , 'N')

    def highlight(self):
        for i in range(64):
            if self.__board[i].col == 'N':
                self.__board[i] = Piece('H', i, 0, 'N')

    def __move(self, start_pos, end_pos, move):
        self.__unPreview()
        if self.__board[start_pos].moved: self.__board[start_pos].moved_again = True
        else: self.__board[start_pos].moved = True

        if self.__board[end_pos].name == 'E':
            sound.boardMove()
        else:
            sound.boardCapture()

        self.__board[end_pos] = self.__board[start_pos]
        self.__board[start_pos] = Piece('E',start_pos,0,'N')

        if move != None: self.__move_history += move+' '
                
    def makeMove(self, start_pos, end_pos, turn, move):
        checkmove = CheckMove(self.__board)

        is_same_colour =  self.__board[end_pos].col == self.__board[start_pos].col
        is_empty_space = self.__board[start_pos].col == 'N'
        is_correct_piece = True if turn == (self.__board[start_pos].col == 'W') else False
        
        if is_empty_space: raise EmptyBox
        elif not is_correct_piece: raise OpponentsPiece
        elif is_same_colour: raise CaptureOwnPiece

        move_type = checkmove.validate(start_pos, end_pos, self.prev_end_pos)
        if move_type == "promotion":
            promo = input("Promote to: ").upper()
            if promo not in "QBNR": raise InvalidPromotionInput

            self.__move(start_pos, end_pos, move)
            self.__board[end_pos].name = promo
            self.__board[end_pos].val = 9 if promo == 'Q' else 5 if promo == 'R' else 3.3 if promo == 'B' else 3.2

        elif move_type == "enpassant":
            killpos = end_pos + (8 if self.__board[start_pos].col == 'W' else -8)
            self.__move(start_pos, end_pos, move)
            self.__board[killpos] = Piece('E',start_pos,0,'N')
            
        elif move_type == "castling":
            self.__move(start_pos, end_pos, move)
            match(end_pos):
                case 2:
                    rook_start_pos = 0
                    rook_end_pos = 3
                case 6:
                    rook_start_pos = 7
                    rook_end_pos = 5
                case 58:
                    rook_start_pos = 56
                    rook_end_pos = 59
                case 62:
                    rook_start_pos = 63
                    rook_end_pos = 61
                case _: 
                    raise Exception

            self.__move(rook_start_pos, rook_end_pos, None)
        else:
            self.__move(start_pos, end_pos, move)

        self.prev_end_pos = end_pos

        #checking if king is alive
        king_pos = None
        for i in range(64):
            if self.__board[i].col == 'N':
                continue
            if self.__board[i].name == 'K' and self.__board[i].col != self.__board[end_pos].col:
                king_pos = i
                break

        if king_pos == None:
            raise EndGame('White' if self.__board[end_pos].col == 'W' else 'Black')

    def getMoveHistory(self):
        return self.__move_history

    def loadGame(self, move_history):
        self.__move_history = move_history
