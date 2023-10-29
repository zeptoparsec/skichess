class Piece:
    def __init__(self, name, pos, val, col): # remove pos and val as it's not used
        self.name = name
        self.pos = pos
        self.val = val
        self.col = col
        self.moved = False
        self.moved_again = False
