class Checkmove:
    def __init__(self, board) -> None:
        self.board = board

    def __check_pawn(self):
        if self.board[self.pos].col == 'B': 
            if self.pos <= 15 and self.pos >= 8:
                if self.target == self.pos + (8) or self.target == self.pos + (8*2):
                    return self.board[self.target].col == 'N'
            elif self.target == self.pos + (8) and self.board[self.target].col == 'N':
                return True
            if self.target == self.pos + (8 + 1) or self.target == self.pos + (8 - 1):
                return self.board[self.target].col == 'W'
        else: 
            if self.pos >= 63 - 15 and self.pos <= 63 - 8:
                if self.target == self.pos - (8) or self.target == self.pos - (8*2):
                    return self.board[self.target].col == 'N'
            elif self.target == self.pos - (8) and self.board[self.target].col == 'N':
                return True
            if self.target == self.pos - (8 + 1) or self.target == self.pos - (8 - 1):
                return self.board[self.target].col == 'B'
        return False

    def __check_rook(self):
        if self.drow == 0:
            if self.dcol > 0:
                for i in range(self.dcol):
                    if self.board[self.pos+i].col != 'N':
                        return False
            else:
                for i in range(self.dcol):
                    if self.board[self.pos-i].col != 'N':
                        return False
        elif self.dcol == 0:
            if self.drow > 0:
                for i in range(self.drow):
                    if self.board[self.pos+8*i].col != 'N':
                        return False
            else:
                for i in range(self.drow):
                    if self.board[self.pos-8*i].col != 'N':
                        return False
        else:
            return False
        return True
    
    def __check_knight(self):
        extr_top = self.target == self.pos + (8*2 - 1) or self.target == self.pos + (8*2 + 1)
        top = self.target == self.pos + (8 + 2) or self.target == self.pos + (8 - 2)
        bottom = self.target == self.pos - (8 + 2) or self.target == self.pos - (8 - 2)
        extr_bottom = self.target == self.pos - (8*2 - 1) or self.target == self.pos - (8*2 + 1)

        if extr_top or top or bottom or extr_bottom: return True
        else: return False

    def __check_bishop(self):
        return self.drow == self.dcol

    def __check_queen(self):
        return self.__check_rook() or self.__check_bishop()

    def __check_king(self):
        return self.drow in [-1,0,1] and self.dcol in [-1,0,1]

    def __check_piece(self):
        if self.type == 'P': return self.__check_pawn()
        elif self.type == 'R': return self.__check_rook()
        elif self.type == 'N': return self.__check_knight()
        elif self.type == 'B': return self.__check_bishop()
        elif self.type == 'Q': return self.__check_queen()
        elif self.type == 'K': return self.__check_king()
        else: raise Exception('Unknown error in __check_piece')

    def __check_castling():
        pass

    def __check_enpassant():
        pass

    def __check_promotion():
        pass

    def __check_meta(self): #stuff like castling, en passant, promotion
        if self.__check_castling() or self.__check_enpassant() or self.__check_promotion():
            return True
        else: 
            return False

    def check(self, startpos, endpos):
        self.pos = startpos
        self.target = endpos
        self.type = self.board[startpos].name
        self.erow = self.target//8
        self.srow = self.pos//8
        self.ecol = self.target%8
        self.scol = self.pos%8
        self.drow = self.erow - self.srow
        self.dcol = self.ecol - self.scol

        if self.__check_piece() or self.__check_meta(): return 1
        else: return -1
