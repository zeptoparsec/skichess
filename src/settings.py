import json
from os import path
from osCompat import escapeFilePaths

class Settings:
    def __init__(self, path):
        self.path = path
        self.active_settings = self.__loadSettings()
        
    def __loadSettings(self):
        settings = open(self.path, 'r').read()
        return json.loads(settings)

    def updateSettings(self, updates):
        with open(self.path, 'r+') as file:
            file.seek(0)
            json.dump(updates, file, indent=4)
            file.truncate()

settings = Settings(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','settings.json']))

