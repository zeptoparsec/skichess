from osCompat import escapeFilePaths
from os import path
import json

class Settings:
    def __init__(self):
        self.active_settings = self.__loadSettings()
        
    def __loadSettings(self):
        settings = open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','settings.json']),'r').read()
        return json.loads(settings)

    def updateSettings(self, updates):
        with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','settings.json']),'r+') as file:
            file.seek(0)
            json.dump(updates, file, indent=4)
            file.truncate()


settings = Settings()