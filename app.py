from game_files import characters
from utils.prompts import prompts
from game_files.game import Game

""" Main module for application """


def main():

    choice = prompts.new_or_load_game()
    if choice == 'LOAD':
        game_map, character = Game.load_game()
        hero = Game(character, game_map)
        hero.terminal_start_main()        
    elif choice == 'NEW':
        hero = Game.new_character()
        hero.terminal_start_main()

if __name__ == '__main__':
    main()
