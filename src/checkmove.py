from errors import InvalidMove, IllegalMove, CheckMate, StaleMate
import operator

class Checkmove:
    def __init__(self, board) -> None:
        self.board = board

    def __pawn(self, pos, col):
        moves = []
        offset, ops = (0, operator.add) if col == 'B' else (40, operator.sub)

        if self.board[ops(pos, 8)].col == 'N': moves.append(ops(pos, 8))
        if (offset + 8) <= pos <= (offset + 15) and self.board[ops(pos, 8*2)].col == 'N': moves.append(ops(pos, 8*2))
        if self.board[ops(pos, (8 + 1))].col not in ('N' + col) and pos%8 != (0 if col == 'W' else 7): 
            moves.append(ops(pos, (8 + 1))) # left kill
        if self.board[ops(pos, (8 - 1))].col not in ('N' + col) and pos%8 != (7 if col == 'W' else 0): 
            moves.append(ops(pos, (8 - 1))) # right kill

        return [i for i in moves if 0 <= int(i) <= 63]
        
    def __rook(self, pos, col):
        moves = []
        ops = [operator.add, operator.sub]

        inbounds = lambda x, i : (0 <= x <= 63) or ((checkpos//8 == pos//8) if i <= 2 else (checkpos//8 == pos//8))

        for i in range(1, 5):
            checkpos = pos
            while True:
                checkpos = ops[i//3](checkpos, 8 if i <= 2 else 1)
                if self.board[checkpos] not in ('N' + col) or not inbounds(checkpos, i): break
                moves.append(checkpos)
        return

    
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

    def __primary_validation(self):
        if self.type == 'P': 
            moves = self.__pawn(self.pos, self.board[self.pos].col)
            if self.target not in moves: raise InvalidMove("pawn")

        elif self.type == 'R': 
            moves = self.__rook(self.pos, self.target)
            if self.target not in moves: raise InvalidMove("rook")
        
        elif self.type == 'N':
            moves = self.__knight(self.pos, self.target)
            if self.target not in moves: raise InvalidMove("knight")

        elif self.type == 'B':
            moves = self.__bishop(self.pos, self.target) 
            if self.target not in moves: raise InvalidMove("bishop")

        elif self.type == 'Q':
            moves = self.__queen(self.pos, self.target) 
            if self.target not in moves: raise InvalidMove("queen")

        elif self.type == 'K':
            moves = self.__king(self.pos, self.target) 
            if self.target not in moves: raise InvalidMove("king")

        else: raise Exception('Unknown error in __piece')
        return True

    def __promotion(self):
        if self.target not in self.__pawn(self.pos, self.board[self.pos].col): return False
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
                
    def check(self, pos, target):
        self.pos = pos
        self.target = target
        self.type = self.board[pos].name
        self.dy = self.target//8 - self.pos//8
        self.dx = self.target%8 - self.pos%8

        complex_move = False
        if self.__promotion(): complex_move = "promotion"
        elif self.__castling(): complex_move = "castling"
        elif self.__enpassant(): complex_move = "enpassant"

        if self.__checkmate(): raise CheckMate
        elif self.__stalemate(): raise StaleMate
        elif self.__check(self.board[pos].col): raise IllegalMove
        
        if not complex_move: return self.__primary_validation()
        else: return complex_move