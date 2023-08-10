class Player:

    def __init__(self, name, col, ip):
        self.name = name
        self.col = col
        self.ip = ip
        self.illegal_moves = 0
        self.score = 0