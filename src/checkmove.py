from errors import InvalidMove, IllegalMove

class Checkmove:
    def __init__(self, board) -> None:
        self.board = board

    def __pawn(self):
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
        

    def __rook(self):
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
    
    def __knight(self):
        extr_top = (self.target == self.pos - (8*2 - 1)) or (self.target == self.pos - (8*2 + 1))
        top = (self.target == self.pos - (8 + 2)) or (self.target == self.pos - (8 - 2))
        bottom = (self.target == self.pos + (8 + 2)) or (self.target == self.pos + (8 - 2))
        extr_bottom = (self.target == self.pos + (8*2 - 1)) or (self.target == self.pos + (8*2 + 1))

        if extr_top or top or bottom or extr_bottom: return True
        else: return False

    def __bishop(self):
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

    def __queen(self):
        return self.__rook() or self.__bishop()

    def __king(self):
        return self.dy in [-1,0,1] and self.dx in [-1,0,1]

    def __piece(self):
        if self.type == 'P': 
            if not self.__pawn(): raise InvalidMove("pawn")
        elif self.type == 'R': 
            if not self.__rook(): raise InvalidMove("rook")
        elif self.type == 'N': 
            if not self.__knight(): raise InvalidMove("knight")
        elif self.type == 'B': 
            if not self.__bishop(): raise InvalidMove("bishop")
        elif self.type == 'Q': 
            if not self.__queen(): raise InvalidMove("queen")
        elif self.type == 'K': 
            if not self.__king(): raise InvalidMove("king")
        else: raise Exception('Unknown error in __piece')

    def __promotion(self):
        if not self.__pawn(): return False
        offset = 0 if self.board[self.pos].col == 'W' else 56
        return offset + 0 <= self.target <= offset + 7
    
    def __castling(self):
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
    
    def __enpassant(self):
        offset = 24 if self.board[self.pos].col == 'W' else 32
        killpos = self.target + (8 if self.board[self.pos].col == 'W' else -8)
        if self.board[killpos].col != 'N': return False
        if not((self.dx == 1 or self.dx == -1) and self.dy == (1 if self.board[self.pos].col == 'B' else -1)): return False
        if not (offset <= self.pos <= 7 + offset) or self.board[killpos].moved_again or self.type != 'P': return False
        return True
    
    
    # def __check(self):
    #     for i in range(64):
    #         if self.board[i].name == 'K' or self.board[i].col == self.board[self.pos].col or self.board[i].col == 'N':
    #             continue
    #         cmove = Checkmove(self.board)#to avoid polluting the current Checkmove object
    #         if cmove.check(i,self.target):
    #             return False
    #     return True

    def __checkbounds(self, index):
        if index < 0 or index > 63: raise IndexError("Out of range")
        else: return index

    def __check(self, col):
        #To-do update the board
        kingpos = 0
        for i in range(64):
            if self.board[i].name == 'K' and self.board[i].col == col:
                kingpos = i
                break

        #check knight threat
        try: extr_top_left = self.board[self.__checkbounds(kingpos - (8*2 - 1))].name == 'N' and self.board[self.__checkbounds(kingpos - (8*2 - 1))].col != col
        except IndexError: extr_top_left = False
        try: extr_top_right = self.board[self.__checkbounds(kingpos - (8*2 + 1))].name == 'N' and self.board[self.__checkbounds(kingpos - (8*2 + 1))].col != col
        except IndexError: extr_top_right = False
        try: top_left = self.board[self.__checkbounds(kingpos - (8 + 2))].name == 'N' and self.board[self.__checkbounds(kingpos - (8 + 2))].col != col
        except IndexError: top_left = False
        try: top_right = self.board[self.__checkbounds(kingpos - (8 - 2))].name == 'N' and self.board[self.__checkbounds(kingpos - (8 - 2))].col != col
        except IndexError: top_right = False
        try: bottom_left = self.board[self.__checkbounds(kingpos + (8 + 2))].name == 'N' and self.board[self.__checkbounds(kingpos + (8 + 2))].col != col
        except IndexError: bottom_left = False
        try: bottom_right = self.board[self.__checkbounds(kingpos + (8 - 2))].name == 'N' and self.board[self.__checkbounds(kingpos + (8 - 2))].col != col
        except IndexError: bottom_right = False
        try: extr_bottom_left = self.board[self.__checkbounds(kingpos + (8*2 - 1))].name == 'N' and self.board[self.__checkbounds(kingpos + (8*2 - 1))].col != col
        except IndexError: extr_bottom_left = False
        try: extr_bottom_right = self.board[self.__checkbounds(kingpos + (8*2 + 1))].name == 'N' and self.board[self.__checkbounds(kingpos + (8*2 + 1))].col != col
        except IndexError: extr_bottom_right = False

        if extr_top_left or extr_top_right or top_left or top_right or bottom_left or bottom_right or extr_bottom_left or extr_bottom_right: return True

        #check down threat

        return False

    def __checkmate(self):
        return False

    def __stalemate(self):
        return False
                
    def check(self, startpos, endpos):
        self.pos = startpos
        self.target = endpos
        self.type = self.board[startpos].name
        self.dy = self.target//8 - self.pos//8
        self.dx = self.target%8 - self.pos%8

        if self.__promotion(): return_value = "promotion"
        elif self.__castling(): return_value = "castling"
        elif self.__enpassant(): return_value = "enpassant"
        else: return_value = self.__piece()

        if self.__checkmate(): return "checkmate"
        elif self.__stalemate(): return "stalemate"
        elif self.__check(self.board[startpos].col): raise IllegalMove
        else: return return_value
    
