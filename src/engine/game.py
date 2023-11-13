import json
from os import path
from compat.osCompat import escapeFilePaths
from board.boardState import BoardState
from engine.settings import settings
from engine.player import Player

board = BoardState()

class Game:
    def __init__(self, time, inc, turn, load, settings):
        self.x_axis = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.y_axis = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        self.then = 0
        self.now = 0
        self.time = [time, time]
        self.inc = [inc, inc]
        self.turn = turn
        self.load = load
        self.preview = False
        self.legacy = settings['legacy']
        self.fixed_board = settings['fixed_board']
        self.fixed_axis = settings['fixed_axis']
        self.idle_compat = settings['idle_compat']
        self.board_sound = settings['sound']
        self.p1 = Player('','')
        self.p2 = Player('','')

    def _format_time(self, sec):
        insert_0 = lambda t: '0'+str(t) if 0 <= t <= 9 else str(t)
        minutes = sec//60
        seconds = sec - (sec//60)*60
        
        return f"[{insert_0(minutes)}:{insert_0(seconds)}]"

    def _time_offset(self, col):
        name_diff = (abs(len(self.p1.name) - len(self.p2.name)))
        given_name = self.p1.name if self.p1.col == col else self.p2.name
        opp_name = self.p1.name if self.p1.col != col else self.p2.name
        if len(given_name) < len(opp_name):
            return name_diff
        else:
            return 0

    def _saveGame(self, move):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..', '..', 'data','games', move[5:]+'.json']).lstrip(), 'w') as file:
            lines = {
                'board': board.getBoard(),
                'prev_end_pos': board.getPrevEndPos(),
                'turn': self.turn,
                'wtime': self.time[0],
                'btime': self.time[1],
                'white': self.p1.name if self.p1.col == 'W' else self.p2.name,
                'black': self.p1.name if self.p1.col == 'B' else self.p2.name
            }

            file.seek(0)
            json.dump(lines, file, indent=4)

    def _loadGame(self):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..', '..', 'data','games', self.load]),'r') as file:
            data = json.load(file)

        self.turn = data['turn']
        self.time = [data['wtime'], data['btime']]
        self.p1 = Player(data['white'], 'W')
        self.p2 = Player(data['black'], 'B')

        board.setBoard(data['board'])
        board.setPrevEndPos(data['prev_end_pos'])

    def __axisToPos(self, x, y):
        newpos = self.x_axis[x] + self.y_axis[y]*8 - 1
        if not self.fixed_board and (self.fixed_axis and not self.turn):
            newpos = 63 - newpos
        return newpos

    def __validateMove(self, move):
        for i, v in enumerate(move):
            if i % 2 == 0:
                if not v.isalpha():
                    raise Exception
            else:
                if not v.isdigit():
                    raise Exception

    def _makeMove(self, move, load=False):            
        self.__validateMove(move)
        if move == 'h':
            board.highlight()
            self.preview = True
            return

        start_pos = self.__axisToPos(move[0], move[1])
        if len(move) == 2:
            if board.preview(start_pos, 'W' if self.turn else 'B') is True:
                self.preview = True
            return

        elif len(move) == 4:
            self.preview = False
            end_pos = self.__axisToPos(move[2], move[3])
            if not self.fixed_board and (self.fixed_axis and not self.turn): 
                move = chr(201 - ord(move[0])) + str(9 - int(move[1])) + chr(201 - ord(move[2])) + str(9 - int(move[3]))
                
            board.makeMove(start_pos, end_pos, self.turn, move)
