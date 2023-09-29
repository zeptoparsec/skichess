from pvp import Pvp
import menu
from time import sleep
from os import listdir, path, remove
import argparse
import json
from settings import settings
from osCompat import escapeFilePaths

parser = argparse.ArgumentParser(description='Simple chess game')
parser.add_argument('-t',type=int,default=600)
args = parser.parse_args()


back = lambda path, remove: path[:-len(remove)] if path.endswith(remove) else path

# menu tree
curr_dir = " _   _           _              ____                _                   _   _\n| | | |_ __   __| | ___ _ __   / ___|___  _ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __\n| | | | '_ \\ / _` |/ _ \\ '__| | |   / _ \\| '_ \\/ __| __| '__| | | |/ __| __| |/ _ \\| '_ \\ \n| |_| | | | | (_| |  __/ |    | |__| (_) | | | \\__ \\ |_| |  | |_| | (__| |_| | (_) | | | |\n \\___/|_| |_|\\__,_|\\___|_|     \\____\\___/|_| |_|___/\\__|_|   \\__,_|\\___|\\__|_|\\___/|_| |_|\n\n Home"
select = [0, 0, 0]
while True:
    option = menu.run(curr_dir, ['New Game', 'Saved Game', 'Settings', 'Exit'], select[0])
    select[0] = option

    if option == 0: 
        curr_dir += ' -> New Game'
        Pvp(
            [args.t, args.t], 
            True, 
            False, 
            settings.active_settings['legacy'], 
            settings.active_settings['fixed_board'],
            settings.active_settings['fixed_axis'],
            settings.active_settings['board_sound'],
        ).run()
        sleep(1)
        curr_dir = back(curr_dir, ' -> New Game')

    elif option == 1:
        curr_dir += " -> Saved Game"
        while True:
            option = menu.run(curr_dir, ['Play', 'Delete', 'Back'], select[1])
            select[1] = option

            if option != 2:
                delete = False if option == 0 else True
                curr_dir += ' -> Play' if option == 0 else ' -> Delete'
                
                while True:
                    game_path = path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games'])
                    game_files = listdir(game_path)
                    game_files.append('Back')

                    option = menu.run(curr_dir, [back(i, '.json').title().strip() for i in game_files], select[2])
                    select[2] = option

                    if game_files[option] != 'Back': 
                        if delete:
                            remove(game_path + escapeFilePaths([game_files[option]]))
                            continue

                        else:
                            with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['..','data','games', game_files[option]]),'r') as file:
                                data = json.load(file)
                            
                                Pvp([args.t, args.t], 
                                    True, 
                                    game_files[option], 
                                    settings.active_settings['legacy'],
                                    settings.active_settings['fixed_board'],
                                    settings.active_settings['fixed_axis'],
                                    settings.active_settings['board_sound']
                                ).run()

                    else: 
                        curr_dir = back(curr_dir, " -> Delete" if delete else " -> Play")
                        select[2] = 0
                        break

            elif option == 2:
                curr_dir = back(curr_dir, " -> Saved Game")
                select[1] = 0
                break

    elif option == 2: 
        curr_dir += ' -> Settings'
        setf = lambda x: ('Enabled' if settings.active_settings[x] else 'Disabled')
        while True:
            option = menu.run(
                curr_dir, 
                [
                    'Legacy:      ' + setf('legacy'),
                    'Fix Board:   ' + setf('fixed_board'),
                    'Fix Axis:    ' + setf('fixed_axis'),
                    'Board Sound: ' + setf('board_sound'),
                    'Idle Compat: ',
                    'Back'
                ], 
                select[1]
            )
            select[1] = option

            if option == 0: 
                settings.active_settings['legacy'] = not settings.active_settings['legacy']

            elif option == 1: 
                settings.active_settings['fixed_board'] = not settings.active_settings['fixed_board']
                if settings.active_settings['fixed_board']: 
                    settings.active_settings['fixed_axis'] = True

            elif option == 2 and not settings.active_settings['fixed_board']:
                settings.active_settings['fixed_axis'] = not settings.active_settings['fixed_axis']

            elif option == 3:
                settings.active_settings['board_sound'] = not settings.active_settings['board_sound']

            elif option == 4:
                curr_dir = back(curr_dir, " -> Settings")
                select[1] = 0
                break

            settings.updateSettings(settings.active_settings)

    elif option == 3: break
