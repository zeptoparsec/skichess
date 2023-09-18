from pvp import Pvp
from pvp_lan import Pvp_lan_menu
from pva import Pva
import menu
from time import sleep
from os import listdir, path, remove
import argparse
import json
from oscompat import escapeFilePaths
from playsound import playsound
from threading import Thread, Event

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
        file.close()

active_settings = load_settings()
back = lambda path, remove: path[:-len(remove)] if path.endswith(remove) else path

def loop_music():
    while True:
        if music_event.is_set(): break
        playsound(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data', 'music', active_settings['music']]))

music_event = Event()
music_thread = Thread(target=loop_music)
if active_settings['music'] != 'Off': 
    music_event.clear()
    music_thread.start()

# menu tree
curr_dir = " _   _           _              ____                _                   _   _\n| | | |_ __   __| | ___ _ __   / ___|___  _ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __\n| | | | '_ \\ / _` |/ _ \\ '__| | |   / _ \\| '_ \\/ __| __| '__| | | |/ __| __| |/ _ \\| '_ \\ \n| |_| | | | | (_| |  __/ |    | |__| (_) | | | \\__ \\ |_| |  | |_| | (__| |_| | (_) | | | |\n \\___/|_| |_|\\__,_|\\___|_|     \\____\\___/|_| |_|___/\\__|_|   \\__,_|\\___|\\__|_|\\___/|_| |_|\n\n Home"
select = [0, 0, 0, 0]
while True:
    option = menu.run(curr_dir, ['New Game', 'Saved Game', 'Lan Game', 'Settings', 'Exit'], select[0])
    select[0] = option

    if option == 0: 
        curr_dir += ' -> New Game'

        while True:
            option = menu.run(curr_dir, ['Player vs Player', 'Player vs Ai', 'Back'], select[1])
            select[1] = option

            if option == 0: 
                Pvp([args.t, args.t], 
                    True, 
                    False, 
                    active_settings['legacy'], 
                    active_settings['fixed_board'],
                    active_settings['fixed_axis'],
                    active_settings['board_sound'],
                ).run()
                sleep(1)

            elif option == 1:
                Pva().run()
                sleep(1)
                
            elif option == 2: 
                curr_dir = back(curr_dir, " -> New Game")
                select[1] = 0
                break

    elif option == 1:
        curr_dir += " -> Saved Game"
        
        while True:
            option = menu.run(curr_dir, ['Play', 'Delete', 'Back'], select[2])
            select[1] = option

            if option in [0, 1]:
                delete = False if option == 0 else True
                curr_dir += ' -> Play' if option == 0 else ' -> Delete'
                
                while True:
                    game_path = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games'])
                    game_files = listdir(game_path)
                    game_files.append('Back')

                    option = menu.run(curr_dir, [i.title().strip() for i in game_files], select[2])
                    select[2] = option

                    if game_files[option] != 'Back': 
                        if not delete:
                            file = open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games', game_files[option]]),'r')
                            data = json.load(file)
                            file.close()
                            
                            if data["mode"] == "pvp":
                                Pvp([args.t, args.t], 
                                    True, 
                                    game_files[option], 
                                    active_settings['legacy'],
                                    active_settings['fixed_board'],
                                    active_settings['fixed_axis'],
                                    active_settings['board_sound']
                                ).run()
                            
                            elif data["mode"] == "pva":
                                Pva().run()
                            sleep(1)
                            
                        else:
                            remove(game_path + escapeFilePaths([game_files[option]]))
                            continue

                    else: 
                        curr_dir = back(curr_dir, " -> Delete" if delete else " -> Play")
                        select[2] = 0
                        break

            elif option == 2:
                curr_dir = back(curr_dir, " -> Saved Game")
                select[1] = 0
                break

    elif option == 2:
        Pvp_lan_menu().run()
        sleep(1)

    elif option == 3: 
        curr_dir += ' -> Settings'
        while True:
            option = menu.run(
                curr_dir, 
                [
                    'Legacy:      ' + ('Enabled' if active_settings['legacy'] else 'Disabled'), 
                    'Fix Board:   ' + ('Enabled' if active_settings['fixed_board'] else 'Disabled'),
                    'Fix Axis:    ' + ('Enabled' if active_settings['fixed_board'] or active_settings['fixed_axis'] else 'Disabled'), 
                    'Board Sound: ' + ('Enabled' if active_settings['board_sound'] else 'Disabled'),
                    'Music:       ' + active_settings['music'].title(),
                    'Back'
                ], 
                select[1]
            )

            if option == 0: 
                active_settings['legacy'] = not active_settings['legacy']

            elif option == 1: 
                active_settings['fixed_board'] = not active_settings['fixed_board']

            elif option == 2 and not active_settings['fixed_board']:
                active_settings['fixed_axis'] = not active_settings['fixed_axis']

            elif option == 3:
                active_settings['board_sound'] = not active_settings['board_sound']

            elif option == 4: 
                curr_dir += ' -> Music'
                music_path = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','music'])
                music_list = ['Off'] + listdir(music_path) + ['Back']
                music = menu.run(curr_dir, [i.title().strip() for i in music_list], 0)

                if music != len(music_list) - 1:
                    active_settings['music'] = music_list[music]

                if active_settings['music'] == 'Off': 
                    music_event.set()
                else: 
                    music_event.clear()
                    if not music_thread.is_alive(): 
                        music_thread = Thread(target=loop_music)
                        music_thread.start()

                curr_dir = back(curr_dir, " -> Music")

            elif option == 5:
                curr_dir = back(curr_dir, " -> Settings")
                select[1] = 0
                break

            update_settings(active_settings)
            select[1] = option

    elif option == 4: break

# exit message