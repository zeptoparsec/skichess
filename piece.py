class Piece:
    def __init__(self, name, pos, val, col, table):
        self.name = name
        self.pos = pos
        self.val = val
        self.col = col
        self.moved = False
        self.table = table
