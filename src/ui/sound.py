from playsound import playsound
from compat.osCompat import escapeFilePaths
from engine.settings import settings
from os import path
from threading import Thread

class Sound:
    def __init__(self):
        self.sound_path = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','..','data','sounds'], False)

        self.menu_select = self.sound_path + 'menu_select2.mp3'
        self.menu_enter = self.sound_path + 'menu_enter.mp3'

        self.board_start_game = self.sound_path + 'board_start_game.mp3'
        self.board_move = self.sound_path + 'board_move.mp3'
        self.board_capture = self.sound_path + 'board_capture.mp3'

    def __playsound(self, sound):
        if settings.active_settings['sound']:
            Thread(target=playsound, args=(sound,)).start() # this thing sometimes work and sometimes dosent

    def boardStartGameSound(self):
        self.__playsound(self.board_start_game)

    def boardMoveSound(self):
        self.__playsound(self.board_move)

    def boardCaptureSound(self):
        self.__playsound(self.board_capture)

    def menuSelectSound(self):
        self.__playsound(self.menu_select)

sound = Sound()
