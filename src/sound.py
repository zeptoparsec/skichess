from playsound import playsound
from osCompat import escapeFilePaths
from os import path

soundpath = path.dirname(path.abspath(__file__)) +escapeFilePaths(['..','data','sounds'], False)

class Sound:
    def __init__(self):
        self.soundpath = soundpath
        self.move = self.soundpath+'move.mp3'
        self.capture = self.soundpath+'capture.mp3'

    def movesound(self):
        playsound(self.move)

    def capturesound(self):
        playsound(self.capture)

sound = Sound()