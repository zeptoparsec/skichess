class Checkmove:
    def __init__(self, board) -> None:
        self.board = board

    def __check_pawn(self):
        if self.board[self.pos].col == 'B': 
            if 15 >= self.pos >= 8:
                if self.target == self.pos + (8) or self.target == self.pos + (8*2):
                    return self.board[self.target].col == 'N'
            elif self.target == self.pos + (8) and self.board[self.target].col == 'N':
                return True
            if self.target == self.pos + (8 + 1) or self.target == self.pos + (8 - 1):
                return self.board[self.target].col == 'W'
        else: 
            if 63 - 15 <= self.pos <= 63 - 8:
                if self.target == self.pos - (8) or self.target == self.pos - (8*2):
                    return self.board[self.target].col == 'N'
            elif self.target == self.pos - (8) and self.board[self.target].col == 'N':
                return True
            if self.target == self.pos - (8 + 1) or self.target == self.pos - (8 - 1):
                return self.board[self.target].col == 'B'
        return False

    def __check_rook(self):
        if self.dy == 0:
            for i in range(1, abs(self.dx)):
                if self.dx > 0:
                    if self.board[self.pos + i].col != 'N': return False
                else:
                    if self.board[self.pos - i].col != 'N': return False
        elif self.dx == 0:
            for i in range(1, abs(self.dy)):
                if self.dy > 0:
                    if self.board[self.pos + 8*i].col != 'N': return False
                else:
                    if self.board[self.pos - 8*i].col != 'N': return False
        else: return False
        return True
    
    def __check_knight(self):
        extr_top = self.target == self.pos + (8*2 - 1) or self.target == self.pos + (8*2 + 1)
        top = self.target == self.pos + (8 + 2) or self.target == self.pos + (8 - 2)
        bottom = self.target == self.pos - (8 + 2) or self.target == self.pos - (8 - 2)
        extr_bottom = self.target == self.pos - (8*2 - 1) or self.target == self.pos - (8*2 + 1)

        if extr_top or top or bottom or extr_bottom: return True
        else: return False

    def __check_bishop(self):
        iterate = abs(self.dx)
        if abs(self.dx) != abs(self.dy): return False
        if self.dy < 0:
            for i in range(1, iterate):
                if self.dx > 0:
                    if self.board[self.pos - i*8 + i].col != 'N': return False
                else:
                    if self.board[self.pos - i*8 - i].col != 'N': return False
        else:
            for i in range(1, iterate):
                if self.dx > 0:
                    if self.board[self.pos + i*8 + i].col != 'N': return False
                else:
                    if self.board[self.pos + i*8 - i].col != 'N': return False
        return True

    def __check_queen(self):
        return self.__check_rook() or self.__check_bishop()

    def __check_king(self):
        return self.dy in [-1,0,1] and self.dx in [-1,0,1]

    def __check_piece(self):
        if self.type == 'P': return self.__check_pawn()
        elif self.type == 'R': return self.__check_rook()
        elif self.type == 'N': return self.__check_knight()
        elif self.type == 'B': return self.__check_bishop()
        elif self.type == 'Q': return self.__check_queen()
        elif self.type == 'K': return self.__check_king()
        else: raise Exception('Unknown error in __check_piece')

    def __check_promotion(self):
        if not self.__check_pawn(): return False

        if self.board[self.pos].col == 'B':
            if 56 <= self.target <= 63: return True
        else: 
            if 0 <= self.target <= 7: return True

        return False
    
    def __check_castling(self):
        offset = 0 if self.board[self.pos].col == 'B' else 56
        if self.type != 'K' or self.board[self.pos].moved: return False
        if self.pos != 4 + offset: return False

        if self.pos == 4 + offset:
            if self.target == 1 + offset:
                if self.board[0 + offset].moved: return False
                for i in range(1, 4):
                    if self.board[i + offset].col != 'N': return False
            elif self.target == 6 + offset:
                if self.board[7 + offset].moved: return False
                for i in range(5, 7):
                    if self.board[i + offset].col != 'N': return False
            else: return False
        return True
    
    def __check_enpassant(self):
        # offset = 0 if self.board[self.pos].col == 'B' else 
        # if 24 <= self.pos <= 31:
        return False

    def check(self, startpos, endpos):
        self.pos = startpos
        self.target = endpos
        self.type = self.board[startpos].name
        self.dy = self.target//8 - self.pos//8
        self.dx = self.target%8 - self.pos%8

        if self.__check_promotion(): return "promotion"
        elif self.__check_castling(): return "castling"
        elif self.__check_enpassant(): return "enpassant"

        return self.__check_piece()
