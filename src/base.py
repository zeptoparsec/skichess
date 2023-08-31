# base.py
# I don't know if this works; it's for storing a large number of games

import csv

class Base:
    def __init__(self, file):
        self.__file = open(file,'rw')
        self.reader = csv.reader(__file.read())

    def getdata(self, num):
        ct = 0

        for i in reader:
            if i == ['', '']:
                ct += 1
                continue
        
            if ct == num*3-3:
                wplayer = i
            elif ct == num*3-2:
                bplayer = i
            elif ct == num*3-1:
                game = i

        return [wplayer,bplayer,game]

    def writedata(self, wplayer, bplayer, game):
        pass

    
