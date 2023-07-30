class Checkmove:

    def __check_pawn(self):
        if self.board[self.pos].col == 'B': 
            if self.pos <= 15 and self.pos >= 8:
                if self.target == self.pos + (8) or self.target == self.pos + (8*2):
                    if self.board[self.target].col == 'N':
                        return True
            elif self.target == self.pos + (8) and self.board[self.target].col == 'N':
                return True
            if self.target == self.pos + (8 + 1) or self.target == self.pos + (8 - 1):
                if self.board[self.target].col == 'W':
                    return True
        else: 
            if self.pos >= 63 - 15 and self.pos <= 63 - 8:
                if self.target == self.pos - (8) or self.target == self.pos - (8*2):
                    if self.board[self.target].col == 'N':
                        return True
            elif self.target == self.pos - (8) and self.board[self.target].col == 'N':
                return True
            if self.target == self.pos - (8 + 1) or self.target == self.pos - (8 - 1):
                if self.board[self.target].col == 'B':
                    return True
        return False

    def __check_rook(self):
        pass

    def __check_knight(self):
        pass

    def __check_bishop(self):
        pass

    def __check_queen(self):
        pass

    def __check_king(self):
        pass

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

    def check(self, startpos, endpos, board):
        self.pos = startpos
        self.target = endpos
        self.type = board[startpos].name
        self.board = board
        
        if not self.__check_pawn(): return -1
        # if self.__check_meta() or self.__check_piece():
        #     return 1
        # else:
        #     return -1
