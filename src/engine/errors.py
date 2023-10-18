class IllegalMove(Exception):
    pass

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

class StaleMate(Exception):
    pass

class CheckMate(Exception):
    pass