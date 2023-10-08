from errors import *
import operator

class Checkmove:
    def __init__(self, board) -> None:
        self.board = board
        self.ischeck = False

    def __pawn(self, pos, col):
        moves = list()
        offset, ops = (0, operator.add) if col == 'B' else (40, operator.sub)

        if 0 <= ops(pos, 8) <= 63:
            if self.board[ops(pos, 8)].col == 'N': 
                moves.append(ops(pos, 8))
            
        if 0 <= ops(pos, 8*2) <= 63 and (offset + 8) <= pos <= (offset + 15):
            if self.board[ops(pos, 8*2)].col == 'N' or self.board[ops(pos, 8)].col == 'N': 
                moves.append(ops(pos, 8*2))

        if 0 <= ops(pos, (8 + 1)) <= 63 and pos%8 != (0 if col == 'W' else 7):
            if self.board[ops(pos, (8 + 1))].col not in (col + 'N'): 
                moves.append(ops(pos, (8 + 1))) # left kill

        if 0 <= ops(pos, (8 - 1)) <= 63 and pos%8 != (7 if col == 'W' else 0):
            if self.board[ops(pos, (8 - 1))].col not in (col + 'N'): 
                moves.append(ops(pos, (8 - 1))) # right kill

        return moves
        
    def __rook(self, pos, col):
        moves = list()
        xbounds = lambda x: (0 <= x <= 63) and (pos//8 != x//8)
        ybounds = lambda x: (0 <= x <= 63) and (pos//8 == x//8)

        i = 1 #up
        while xbounds(pos - 8*i) and self.board[pos - 8*i].col != col:
            moves.append(pos - 8*i)
            if self.board[pos - 8*i].col != 'N': break
            i += 1

        i = 1 #down
        while xbounds(pos + 8*i) and self.board[pos + 8*i].col != col:
            moves.append(pos + 8*i)
            if self.board[pos + 8*i].col != 'N': break
            i += 1
            

        i = 1 #right
        while ybounds(pos + i) and self.board[pos + i].col != col:
            moves.append(pos + i)
            if self.board[pos + i].col != 'N': break
            i += 1
            
        
        i = 1 #left
        while ybounds(pos - i) and self.board[pos - i].col != col:
            moves.append(pos - i)
            if self.board[pos - i].col != 'N': break
            i += 1
            
        return moves

    def __knight(self, pos, col):
        moves = list()
        s = lambda x: abs(pos//8 - x//8) <= 2 and abs(pos%8 - x%8) <= 2

        possible_pos = [
            pos - (8*2 + 1), # extreme top left
            pos - (8*2 - 1), # extreme top right
            pos - (8 + 2),   # top left
            pos - (8 - 2),   # top right
            pos + (8 + 2),   # bottom left
            pos + (8 - 2),   # bottom right
            pos + (8*2 + 1), # extreme bottom left
            pos + (8*2 - 1)  # extreme bottom right
        ]

        for i in possible_pos:
            if (0 <= i <= 63) and self.board[i].col != col and s(i):
                moves.append(i)

        return moves

    def __bishop(self, pos, col):
        moves = list()
        bounds = lambda x: (0 <= x <= 63) and abs(pos//8 - x//8) == abs(pos%8 - x%8)

        i = 1 #top-left
        while bounds(pos - (8*i + i)) and self.board[pos - (8*i + i)].col != col:
            moves.append(pos - (8*i + i))
            if self.board[pos - (8*i + i)].col != 'N': break
            i += 1

        i = 1 #top-right
        while bounds(pos - (8*i - i)) and self.board[pos - (8*i - i)].col != col:
            moves.append(pos - (8*i - i))
            if self.board[pos - (8*i - i)].col != 'N': break
            i += 1

        i = 1 #bottom-left
        while bounds(pos + (8*i - i)) and self.board[pos + (8*i - i)].col != col:
            moves.append(pos + (8*i - i))
            if self.board[pos + (8*i - i)].col != 'N': break
            i += 1

        i = 1 #bottom-right
        while bounds(pos + (8*i + i)) and self.board[pos + (8*i + i)].col != col:
            moves.append(pos + (8*i + i))
            if self.board[pos + (8*i + i)].col != 'N': break
            i += 1

        return moves

    def __queen(self, pos, col):
        return (self.__rook(pos, col) + self.__bishop(pos, col))

    def __king(self, pos, col):
        s = lambda x: abs(pos//8 - x//8) <= 1 and abs(pos%8 - x%8) <= 1
        check = lambda x, y: self.__check_check(x, y)
        return [i for i in self.__queen(pos, col) if s(i) and check(i, pos)]

    def __primary_validation(self):
        if not self.ischeck:
            for i in range(64):
                if self.board[i].col == self.col and self.board[i].name == 'K':
                    if not self.__check_check(i,i):
                        raise InvalidMove("check")

        if self.type == 'P': 
            if self.target not in self.__pawn(self.pos, self.col): 
                raise InvalidMove("pawn")

        elif self.type == 'R': 
            if self.target not in self.__rook(self.pos, self.col): 
                raise InvalidMove("rook")
        
        elif self.type == 'N':
            if self.target not in self.__knight(self.pos, self.col): 
                raise InvalidMove("knight")

        elif self.type == 'B':
            if self.target not in self.__bishop(self.pos, self.col): 
                raise InvalidMove("bishop")

        elif self.type == 'Q':
            if self.target not in self.__queen(self.pos, self.col): 
                raise InvalidMove("queen")

        elif self.type == 'K':
            if self.target not in self.__king(self.pos, self.col): 
                raise InvalidMove("king")

        else: raise Exception
        return True

    def __promotion(self):
        if self.target not in self.__pawn(self.pos, self.board[self.pos].col): return False
        offset = 0 if self.board[self.pos].col == 'W' else 56
        return offset + 0 <= self.target <= offset + 7
    
    def __castling(self): #validation pending
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

    def __check_check(self, target, pos):
        boardcp = self.board[::]

        boardcp[pos], boardcp[target] = boardcp[target], boardcp[pos]

        cmove = Checkmove(boardcp)#to avoid polluting the current Checkmove object

        for i in range(64):
            if self.board[i].col == self.board[pos].col or self.board[i].col == 'N':
                continue

            if self.board[i].name == 'K':
                if abs(pos//8 - i//8) <= 1 and abs(pos%8 - i%8) <= 1:
                    return False
                continue


            try:
                cmove.validate(i, target, True)
            except Exception:
                pass
            else:
                return False

        return True

    def check(self, col): # test it
        kingpos = 0
        for i in range(64):
            if self.board[i].name == 'K' and self.board[i].col == col:
                kingpos = i
                break
        else: raise IllegalMove

        for i in self.__knight(kingpos, None):
            if self.board[i].name == 'N' and self.board[i].col not in col + 'N':
                return True

        for i in self.__rook(kingpos, None):
            if self.board[i].name in 'QR' and self.board[i].col not in col + 'N':
                return True

        for i in self.__bishop(kingpos, None):
            if self.board[i].name in 'QB' and self.board[i].col not in col + 'N':
                return True

        for i in self.__king(kingpos, None):
            if self.board[i].name in 'K' and self.board[i].col not in col + 'N':
                return True

        s = lambda x: abs(kingpos//8 - x//8) <= 1 and abs(kingpos%8 - x%8) <= 1
        if col == 'B':
            if self.board[kingpos + (8 - 1)].name == 'P' and self.board[kingpos + (8 - 1)].col == 'W' and s(kingpos + (8 - 1)):
                return True
            elif self.board[kingpos + (8 + 1)].name == 'P' and self.board[kingpos + (8 + 1)].col == 'W' and s(kingpos + (8 + 1)):
                return True
        elif col == 'W':
            if self.board[kingpos - (8 - 1)].name == 'P' and self.board[kingpos - (8 - 1)].col == 'B' and s(kingpos - (8 - 1)):
                return True
            elif self.board[kingpos - (8 + 1)].name == 'P' and self.board[kingpos - (8 + 1)].col == 'W' and s(kingpos - (8 + 1)):
                return True
        
        return False
                
    def validate(self, pos, target, ischeck):
        self.pos = pos
        self.target = target
        self.col = self.board[pos].col
        self.type = self.board[pos].name
        self.dy = self.target//8 - self.pos//8
        self.dx = self.target%8 - self.pos%8
        self.ischeck = ischeck

        complex_move = False
        if self.type == 'P': 
            if self.__promotion(): complex_move = "promotion"
            elif self.__enpassant(): complex_move = "enpassant"
        elif self.type == 'K' and self.__castling(): complex_move = "castling"
        
        if not complex_move: return self.__primary_validation()
        else: return complex_move
    
    def preview(self, pos): 
        name = self.board[pos].name
        col = self.board[pos].col

        if name == 'P': return self.__pawn(pos, col)
        elif name == 'R': return self.__rook(pos, col)
        elif name == 'N': return self.__knight(pos, col)
        elif name == 'B': return self.__bishop(pos, col)
        elif name == 'Q': return self.__queen(pos, col)
        elif name == 'K': return self.__king(pos, col)
        else: raise Exception
