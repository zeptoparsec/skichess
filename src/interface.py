from pvp import Pvp
from pvp_lan import Pvp_lan_menu
from pva import Pva
import menu
from time import sleep
from os import listdir, path, remove
import argparse
import json
from oscompat import escapeFilePaths

parser = argparse.ArgumentParser(description='Simple chess game')
parser.add_argument('-t',type=int,default=600)
args = parser.parse_args()

def load_settings():
    settings = open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','settings.json']),'r').read()
    return json.loads(settings)

def update_settings(updates):
    with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','settings.json']),'r+') as file:
        file.seek(0)
        json.dump(updates, file, indent=4)
        file.truncate()

active_settings = load_settings()

# menu tree
curr_dir = 'Chess Engine'
select = [0, 0, 0, 0]
while True:
    option = menu.run(curr_dir, ['Player vs Player', 'Player vs Ai', 'Settings', 'Exit'], select[0])
    select[0] = option

    if option == 0: 
        curr_dir += ' -> Player vs Player'

        while True:
            option = menu.run(curr_dir, ['New game', 'Saved game', 'Lan game', 'Back'], select[1])
            select[1] = option

            if option == 0: 
                Pvp([args.t, args.t], True, False, active_settings['legacy']).run()
                sleep(1)

            elif option == 1:
                curr_dir += ' -> Saved game'

                while True:
                    option = menu.run(curr_dir, ['Play', 'Delete', 'Back'], select[2])
                    select[2] = option

                    if option in [0, 1]:
                        delete = False if option == 0 else True
                        curr_dir += ' -> Play' if option == 0 else ' -> Delete'
                        
                        while True:
                            cache_path = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games'])
                            cache_files = [i for i in listdir(cache_path)]
                            cache_files.append('Back')

                            option = menu.run(curr_dir, cache_files, select[3])
                            select[3] = option

                            if cache_files[option] != 'Back': 
                                if not delete:
                                    Pvp([args.t, args.t], True, cache_files[option], active_settings['legacy']).run()
                                    sleep(1)
                                    
                                else:
                                    remove(escapeFilePaths([cache_path, cache_files[option]])) #error
                                    continue

                            else: 
                                curr_dir = curr_dir[:(-10 if delete else -8)]
                                select[3] = 0
                                break

                    elif option == 2:
                        curr_dir = curr_dir[:-14]
                        select[2] = 0
                        break

            elif option == 2: 
                Pvp_lan_menu().run()
                sleep(1)

            elif option == 3: 
                curr_dir = curr_dir[:-20]
                select[1] = 0
                break

    elif option == 1: 
        Pva().run()
        sleep(1)

    elif option == 2: 
        curr_dir += ' -> Settings'
        while True:
            option = menu.run(
                curr_dir, 
                [
                    'Legacy: ' + ('Enabled' if active_settings['legacy'] else 'Disabled'), 
                    'Back'
                ], 
                0
            )

            if option == 0:
                active_settings['legacy'] = not active_settings['legacy']
                update_settings(active_settings)

            elif option == 1:
                curr_dir = curr_dir[:-12]
                break

    elif option == 3: break