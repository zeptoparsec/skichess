from player import Player
import json
from os import path
from oscompat import escapeFilePaths
from boardstate import Boardstate

board = Boardstate()

class Game:
    def __init__(self, time, turn, load, legacy):
        self.x_axis_w = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis_w = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.x_axis_b = {'a': 8, 'b': 7, 'c': 6, 'd': 5, 'e': 4, 'f': 3, 'g': 2, 'h': 1}
        self.y_axis_b = {'8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1, '1': 0}
        self.then = 0
        self.now = 0
        self.time = time
        self.inc = [0, 0]
        self.turn = turn
        self.legacy = legacy
        self.load = load
        self.preview = False

    def _load_game(self):
        file = open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games', self.load]),'r')
        data = json.load(file)
        moves = data["moves"].split()

        self.time = [data["wtime"], data["btime"]]
        self.p1 = Player(data["white"], 'W', None)
        self.p2 = Player(data["black"], 'B', None)

        for i in moves:
            self._makemove(i)
            self.turn = not self.turn

        board.loadGame(' '.join([str(i) for i in moves]) + ' ')

    def _makemove(self, move):
        if self.turn:
            x_axis = self.x_axis_w
            y_axis = self.y_axis_w
        else: 
            x_axis = self.x_axis_b
            y_axis = self.y_axis_b

        if not (move[0].isalpha and move[1].isdigit()): raise Exception
        startpos = x_axis[move[0]] + y_axis[move[1]]*8 - 1
        self.preview = False
        board.unpreview()

        if len(move) == 2: 
            self.preview = True
            board.preview(startpos)

        elif len(move) == 4: 
            if not (move[2].isalpha and move[3].isdigit()): raise Exception
            endpos = x_axis[move[2]] + y_axis[move[3]]*8 - 1
            board.makemove(startpos, endpos, self.turn, move)

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