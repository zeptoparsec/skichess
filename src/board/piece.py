class Piece:
    def __init__(self, name, val, col, moved=False, moved_again=False): # remove pos and val as it's not used
        self.name = name
        # self.pos = pos
        self.val = val
        self.col = col
        self.moved = moved
        self.moved_again = moved_again
