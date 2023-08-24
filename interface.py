from pvp import Pvp
from pvp_lan import Pvp_lan_menu
from pva import Pva
from menu import Menu
from time import sleep
from os import listdir, path, remove
import argparse
import json

parser = argparse.ArgumentParser(description='Simple chess game')
parser.add_argument('-t',type=int,default=600)
args = parser.parse_args()

def load_settings():
    settings = open(path.dirname(path.abspath(__file__)) + "/settings.json",'r').read()
    return json.loads(settings)

active_settings = load_settings()

# menu tree
curr_dir = 'Chess Engine'
start_menu = Menu(curr_dir, ['Player vs Player', 'Player vs Ai', 'Exit'])

while True:
    option = start_menu.run()
    if option == 0: 
        curr_dir += '\\Player vs Player'
        while True:
            choice_pvp = Menu(curr_dir, ['New game', 'Saved game', 'Lan game', 'Back'])
            option = choice_pvp.run()

            if option == 0: 
                Pvp([args.t, args.t], True, False, active_settings['legacy']).run()
                sleep(1)

            elif option == 1:
                curr_dir += '\\Saved game'
                while True:
                    load_menu = Menu(curr_dir, ['Play', 'Delete', 'Back'])
                    option = load_menu.run()

                    if option in [0, 1]:
                        delete = False if option == 0 else True
                        curr_dir += '\\Play' if option == 0 else '\\Delete'
                        
                        while True:
                            cache_path = path.dirname(path.abspath(__file__)) + "\\cache\\games\\"
                            cache_files = [i.title() for i in listdir(cache_path)]
                            cache_files.append('Back')

                            load_game = Menu(curr_dir, cache_files)
                            option = load_game.run()

                            if cache_files[option] != 'Back': 
                                if not delete:
                                    Pvp([args.t, args.t], True, cache_files[option], active_settings['legacy']).run()
                                    sleep(1)
                                    
                                else:
                                    remove(cache_path + cache_files[option])
                                    continue

                            else: 
                                curr_dir = curr_dir[:(-7 if delete else -5)]
                                break

                    elif option == 2:
                        curr_dir = curr_dir[:-11]
                        break

            elif option == 2: 
                Pvp_lan_menu().run()
                sleep(1)

            elif option == 3: 
                curr_dir = curr_dir[:-17]
                break

    elif option == 1: 
        Pva().run()
        sleep(1)

    elif option == 2: break
