from engine.settings import settings
from os import name, system

def clr():
    if settings.active_settings['idle_compat']: 
        print('\n'*49)
    else:
        if name == 'nt': system('cls')
        else: system('clear')