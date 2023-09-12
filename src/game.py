from player import Player
import json
from os import path
from oscompat import escapeFilePaths
from boardstate import Boardstate

board = Boardstate()

class Game:
    def __init__(self, time, turn, load, legacy, fixed_axis):
        self.x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.then = 0
        self.now = 0
        self.time = time
        self.inc = [0, 0]
        self.turn = turn
        self.load = load
        self.preview = False
        self.legacy = legacy
        self.fixed_axis = fixed_axis

    def _load_game(self):
        file = open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games', self.load]),'r')
        data = json.load(file)
        moves = data["moves"].split()
        file.close()

        self.time = [data["wtime"], data["btime"]]
        self.p1 = Player(data["white"], 'W', None)
        self.p2 = Player(data["black"], 'B', None)

        for i in moves:
            self._makemove(i)
            self.turn = not self.turn

        board.loadGame(' '.join([str(i) for i in moves]) + ' ')

    def _makemove(self, move):
        self.preview = False
        board.unpreview()

        startpos = self.x_axis[move[0]] + self.y_axis[move[1]]*8 - 1

        if self.fixed_axis and not (self.turn or self.load):
            startpos = 63 - startpos

        if len(move) == 2: 
            if not (move[0].isalpha and move[1].isdigit()): raise Exception
            if self.fixed_axis and not (self.turn or self.load): move = chr(201 - ord(move[0])) + str(9 - int(move[1]))
            self.preview = True
            board.preview(startpos)

        elif len(move) == 4 : 
            if not (move[2].isalpha and move[3].isdigit()): raise Exception
            endpos = self.x_axis[move[2]] + self.y_axis[move[3]]*8 - 1
            if self.fixed_axis and not (self.turn or self.load): 
                move = chr(201 - ord(move[0])) + str(9 - int(move[1])) + chr(201 - ord(move[2])) + str(9 - int(move[3]))
                endpos = 63 - endpos
            board.makemove(startpos, endpos, self.turn, move.lower())

        else: raise Exception

    def _save_game(self, move):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(["..","data","games", move[5:]]).lstrip(), 'w') as file:
            lines = {
                "moves": board.getMoveHistory(),
                "wtime": self.time[0],
                "btime": self.time[1],
                "white": self.p1.name if self.p1.col == 'W' else self.p2.name,
                "black": self.p1.name if self.p1.col == 'B' else self.p2.name,
                "mode": "pvp"
            }

            file.seek(0)
            json.dump(lines, file, indent=4)
            file.close()