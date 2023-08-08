class Piece:
    def __init__(self, name, pos, val, col, table):
        self.name = name
        self.pos = pos
        self.val = val
        self.col = col
        self.table = table
        if name in 'RKP': self.moved = False
        if name == 'P': self.moved_again = False
