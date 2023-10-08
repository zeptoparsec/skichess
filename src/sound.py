from playsound import playsound
from osCompat import escapeFilePaths
from os import path
from threading import Thread
from time import sleep

soundpath = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','sounds'], False)

class Sound:
    def __init__(self):
        self.soundpath = soundpath # why do we need this when soundpath is globally declared?
        self.start_game = self.soundpath + 'start_game.mp3'
        self.move = self.soundpath + 'move.mp3'
        self.capture = self.soundpath + 'capture.mp3'

    def startGameSound(self):
        Thread(target=playsound, args=(self.start_game,)).start()
        sleep(0.01)

    def moveSound(self):
        Thread(target=playsound, args=(self.move,)).start()
        sleep(0.01)

    def captureSound(self):
        Thread(target=playsound, args=(self.capture,)).start()
        sleep(0.01)

sound = Sound()
