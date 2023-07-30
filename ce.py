class boardstate:
    def __init__(self) -> None:
        self._board = [
            'r','n','b','q','k','b','n','r',
            'p','p','p','p','p','p','p','p',
            'e','e','e','e','e','e','e','e',
            'e','e','e','e','e','e','e','e',
            'e','e','e','e','e','e','e','e',
            'e','e','e','e','e','e','e','e',
            'P','P','P','P','P','P','P','P',
            'R','N','B','Q','K','B','N','R'
        ]
    def makemove(self,startpos, endpos):
        tmp = self._board[startpos]
        self._board[startpos] = self._board[endpos]
        self._board[endpos] = tmp # Maybe do some move validation here?
