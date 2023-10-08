from player import Player
import json
from os import path
from osCompat import escapeFilePaths
from boardState import BoardState

board = BoardState()

class Game:
    def __init__(self, time, turn, load, settings):
        self.x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.then = 0
        self.now = 0
        self.time = time
        self.inc = [0, 0]
        self.turn = turn
        self.load = load
        self.preview = False
        self.legacy = settings['legacy']
        self.fixed_board = settings['fixed_board']
        self.fixed_axis = settings['fixed_axis']
        self.idle_compat = settings['idle_compat']
        self.board_sound = settings['board_sound']
        self.p1 = Player('','',None)
        self.p2 = Player('','',None)

    def _saveGame(self, move):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(["..","data","games", move[5:]+'.json']).lstrip(), 'w') as file:
            lines = {
                "moves": board.getMoveHistory(),
                "wtime": self.time[0],
                "btime": self.time[1],
                "white": self.p1.name if self.p1.col == 'W' else self.p2.name,
                "black": self.p1.name if self.p1.col == 'B' else self.p2.name
            }

            file.seek(0)
            json.dump(lines, file, indent=4)

    def _axisToPos(self, x, y):
        newpos = self.x_axis[x] + self.y_axis[y]*8 - 1
        if not self.fixed_board and (self.fixed_axis and not self.turn):
            newpos = 63 - newpos
        return newpos
