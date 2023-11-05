"""
    sound.py
    ========
    The sound subsystem.
"""

from playsound import playsound
from compat.osCompat import escapeFilePaths
from engine.settings import settings
from os import path, system
from threading import Thread

class Sound:
    """
        The Sound class
        ===============
    """
    def __init__(self):
        self.sound_path = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','..','data','sounds'], False)

        self.menu_select = self.sound_path + 'menu_select.mp3'
        self.menu_enter = self.sound_path + 'menu_enter.mp3'

        self.board_start_game = self.sound_path + 'board_start_game.mp3'
        self.board_move = self.sound_path + 'board_move.mp3'
        self.board_capture = self.sound_path + 'board_capture.mp3'

    def __playSound(self, path):
        if settings.active_settings['sound']:
            Thread(target=playsound, args=(path,)).start() # Need to use a different module to play sound

    def boardStartGame(self):
        self.__playSound(self.board_start_game)

    def boardMove(self):
        self.__playSound(self.board_move)

    def boardCapture(self):
        self.__playSound(self.board_capture)

    def menuSelect(self):
        self.__playSound(self.menu_select)

    def menuEnter(self):
        self.__playSound(self.menu_enter)

sound = Sound()
