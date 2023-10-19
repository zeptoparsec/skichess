from engine.errors import *
import operator
from board.piece import Piece

class CheckMove:
    def __init__(self, board, prev_move) -> None:
        self.board = board
        self.prev_move = prev_move

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
        xBounds = lambda x: (0 <= x <= 63) and (pos//8 != x//8)
        yBounds = lambda x: (0 <= x <= 63) and (pos//8 == x//8)

        i = 1 #up
        while xBounds(pos - 8*i) and self.board[pos - 8*i].col != col:
            moves.append(pos - 8*i)
            if self.board[pos - 8*i].col != 'N': break
            i += 1

        i = 1 #down
        while xBounds(pos + 8*i) and self.board[pos + 8*i].col != col:
            moves.append(pos + 8*i)
            if self.board[pos + 8*i].col != 'N': break
            i += 1

        i = 1 #right
        while yBounds(pos + i) and self.board[pos + i].col != col:
            moves.append(pos + i)
            if self.board[pos + i].col != 'N': break
            i += 1
            
        i = 1 #left
        while yBounds(pos - i) and self.board[pos - i].col != col:
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
        moves = list()
        check = lambda x: (0 <= x <= 63) and (abs(pos//8 - x//8) <= 1 and abs(pos%8 - x%8) <= 1)
        possible_pos = [
            pos + (8 - 1),
            pos + (8),
            pos + (8 + 1),
            pos - 1,
            pos + 1,
            pos - (8 - 1),
            pos - (8),
            pos - (8 + 1)
        ]
        for i in possible_pos:
            if check(i) and self.board[i].col != col:
                moves.append(i)
        
        return moves

    def __primaryValidation(self):
        if self.type == 'P':
            if self.end_pos not in self.__pawn(self.start_pos, self.col): 
                raise InvalidMove("pawn")

        elif self.type == 'R': 
            if self.end_pos not in self.__rook(self.start_pos, self.col): 
                raise InvalidMove("rook")
        
        elif self.type == 'N':
            if self.end_pos not in self.__knight(self.start_pos, self.col): 
                raise InvalidMove("knight")

        elif self.type == 'B':
            if self.end_pos not in self.__bishop(self.start_pos, self.col): 
                raise InvalidMove("bishop")

        elif self.type == 'Q':
            if self.end_pos not in self.__queen(self.start_pos, self.col): 
                raise InvalidMove("queen")

        elif self.type == 'K':
            if self.end_pos not in self.__king(self.start_pos, self.col): 
                raise InvalidMove("king")

        else: raise Exception

        boardcp = self.board[::]
        if boardcp[self.end_pos] == 'N':
            boardcp[self.start_pos], boardcp[self.end_pos] = boardcp[self.end_pos], boardcp[self.start_pos]
        elif boardcp[self.end_pos] != self.col:
            boardcp[self.start_pos], boardcp[self.end_pos] = Piece('E',self.start_pos,0,'N'), boardcp[self.start_pos]
        cmove = CheckMove(boardcp, None)
        king_pos = 0
        for i in range(64):
            if cmove.board[i].name == 'K' and cmove.board[i].col == self.col:
                king_pos = i
                break
        if cmove.check(king_pos, self.board[self.start_pos].col):
            raise IllegalMove()

        return True

    def __promotion(self):
        if self.end_pos not in self.__pawn(self.start_pos, self.board[self.start_pos].col): return False
        offset = 0 if self.board[self.start_pos].col == 'W' else 56
        return offset + 0 <= self.end_pos <= offset + 7

    def __castling(self):
        #(rook, end_pos, start_pos/king_pos, col)
        possible_pos = [(0, 2, 4, 'B'), (7, 6, 4, 'B'), (56, 58, 60, 'W'), (63, 62, 60, 'W')]

        if self.type != 'K': 
            return False

        for rook_pos, end_pos, start_pos, col in possible_pos:
            valid = True
            if self.board[rook_pos].col != col or self.board[start_pos].col != col:
                valid = False
            if self.start_pos != start_pos or self.board[self.start_pos].moved:
                valid = False
            if self.board[rook_pos].name != 'R' or self.board[rook_pos].moved:
                valid = False
            if self.end_pos != end_pos:
                valid = False
            if not valid:
                continue

            for i in range(min(start_pos, rook_pos), max(start_pos, rook_pos)):
                if self.check(i, col):
                    return False
            break
        return True

    def __enpassant(self): # needs revision(check is prev move was that pawn to be killed)
        offset = 24 if self.board[self.start_pos].col == 'W' else 32
        kill_pos = self.end_pos + (8 if self.board[self.start_pos].col == 'W' else -8)
        if self.board[kill_pos].col != 'N': return False
        if not((self.dx == 1 or self.dx == -1) and self.dy == (1 if self.board[self.start_pos].col == 'B' else -1)): return False
        if not (offset <= self.start_pos <= 7 + offset) or self.board[kill_pos].moved_again or self.type != 'P': return False
        return True

    def check(self, pos, col):
        for i in self.__knight(pos, None):
            if self.board[i].name == 'N' and self.board[i].col != col:
                return True

        for i in self.__rook(pos, None):
            if self.board[i].name in 'QR' and self.board[i].col != col:
                return True

        for i in self.__bishop(pos, None):
            if self.board[i].name in 'QB' and self.board[i].col != col:
                return True

        for i in self.__king(pos, None):
            if self.board[i].name in 'K' and self.board[i].col != col:
                return True

        s = lambda x: abs(pos//8 - x//8) <= 1 and abs(pos%8 - x%8) <= 1
        if col == 'B':
            if s(pos + (8 - 1)) and self.board[pos + (8 - 1)].name == 'P' and self.board[pos + (8 - 1)].col == 'W': 
                return True
            elif s(pos + (8 + 1)) and self.board[pos + (8 + 1)].name == 'P' and self.board[pos + (8 + 1)].col == 'W': 
                return True
        elif col == 'W':
            if s(pos - (8 - 1)) and self.board[pos - (8 - 1)].name == 'P' and self.board[pos - (8 - 1)].col == 'B': 
                return True
            elif s(pos - (8 + 1)) and self.board[pos - (8 + 1)].name == 'P' and self.board[pos - (8 + 1)].col == 'B': 
                return True
        
        return False
                
    def validate(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.col = self.board[start_pos].col
        self.type = self.board[start_pos].name
        self.dy = self.end_pos//8 - self.start_pos//8
        self.dx = self.end_pos%8 - self.start_pos%8

        complex_move = False
        if self.type == 'P': 
            if self.__promotion(): complex_move = "promotion"
            elif self.__enpassant(): complex_move = "enpassant"

        elif self.type == 'K' and self.__castling(): 
            complex_move = "castling"
        
        if not complex_move: return self.__primaryValidation()
        else: return complex_move
    
    def preview(self, pos): 
        name = self.board[pos].name
        col = self.board[pos].col

        if name == 'P': return self.__pawn(pos, col) # add enpassant pos
        elif name == 'R': return self.__rook(pos, col)
        elif name == 'N': return self.__knight(pos, col)
        elif name == 'B': return self.__bishop(pos, col)
        elif name == 'Q': return self.__queen(pos, col)
        elif name == 'K': return self.__king(pos, col) # add castling pos
        else: raise Exception("Unknown")
