#from abc import ABC, abstractmethod
class Piece:
    def __init__(self, name, pos, val, col, table):
        self.name = name
        self.pos = pos
        self.val = val
        self.col = col
        self.table = table
        self.moved = False
        self.moved_again = False

'''
class Piece(ABC):
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    @abstractmethod
    @property
    def val():
        ...

    @abstractmethod
    def validatemove(dx,dy,board,pos,target):
        ...

class Pawn(Piece):
    def val():
        return 1.0
    def validatemove(self, dx, dy, board, pos, target):
        if board[pos].col == 'B': 
            if pos <= 15 and pos >= 8:
                if target == pos + (8) or target == pos + (8*2):
                    return board[target].col == 'N'
            elif target == pos + (8) and board[target].col == 'N':
                return True
            if target == pos + (8 + 1) or target == pos + (8 - 1):
                return board[target].col == 'W'
        else: 
            if pos >= 63 - 15 and pos <= 63 - 8:
                if target == pos - (8) or target == pos - (8*2):
                    return board[target].col == 'N'
            elif target == pos - (8) and board[target].col == 'N':
                return True
            if target == pos - (8 + 1) or target == pos - (8 - 1):
                return board[target].col == 'B'
        return False

class Bishop(Piece):
    def val():
        return 3.3

class Knight(Piece):
    def val():
        return 3.2
    
class Rook(Piece):
    def val():
        return 5

class Queen(Piece):
    def val():
        return 9

class King(Piece):
    def val():
        return 200

class Empty(Piece):
    def val():
        return 0
'''