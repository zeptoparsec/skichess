from pvp import Pvp
from pvp_lan import Pvp_lan_menu
from pva import Pva
from menu import Menu
from time import sleep
from os import listdir, getcwd
import argparse

parser = argparse.ArgumentParser(description='Simple chess game')
parser.add_argument('-t',type=int,default=600)
args = parser.parse_args()

# menu tree
curr_dir = 'Chess Engine'
start_menu = Menu(curr_dir, ['Player vs Player', 'Player vs Ai', 'Exit'])

while True:
    option = start_menu.run()
    if option == 0: 
        curr_dir += '/Player vs Player'
        while True:
            choice_pvp = Menu(curr_dir, ['New game', 'Load game', 'Lan game', 'Back'])
            option = choice_pvp.run()

            if option == 0: 
                Pvp([args.t, args.t], True, False).run()
                sleep(1)

            elif option == 1:
                curr_dir += '/Load game'
                while True:
                    load_menu = Menu(curr_dir, ['Play', 'Delete', 'Back'])
                    option = load_menu.run()

                    if option == 0:
                        curr_dir += '/Play'
                        while True:
                            cache_files = listdir(getcwd() + "//cache//")
                            cache_files.append('Back')

                            load_game = Menu(curr_dir, cache_files)
                            option = load_game.run()

                            if cache_files[option] != 'Back': 
                                Pvp([args.t, args.t], True, cache_files[option]).run()
                                sleep(1)

                            elif cache_files[option] == 'Back': 
                                curr_dir = curr_dir.removesuffix('/Play')
                                break

                    elif option == 1:
                        pass #Delete selected file

                    elif option == 2:
                        curr_dir = curr_dir.removesuffix('/Load game')
                        break

            elif option == 2: 
                Pvp_lan_menu().run()
                sleep(1)

            elif option == 3: 
                curr_dir = curr_dir.removesuffix('/Player vs Player')
                break

    elif option == 1: 
        Pva().run()
        sleep(1)

    elif option == 2: exit()