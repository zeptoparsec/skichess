class Piece:
    def __init__(self, name, val, col, moved=False, moved_again=False):
        self.name = name
        self.val = val
        self.col = col
        self.moved = moved
        self.moved_again = moved_again
