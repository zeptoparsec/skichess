class OpponentsPiece(Exception):
    pass

class OpponentPreview(Exception):
    pass

class EmptyBox(Exception):
    pass

class CaptureOwnPiece(Exception):
    pass

class InvalidMove(Exception): 
    def __init__(self, piece):
        super().__init__(piece)

class UnNamedFile(Exception):
    pass

class InvalidPromotionInput(Exception):
    pass

class Checkmate(Exception):
    def __init__(self, col):
        super().__init__(col)

class Stalemate(Exception):
    pass

class TimeOut(Exception):
    def __init__(self, col):
        super().__init__(col)

class Check(Exception):
    pass