from utils.prompts import prompts
from game_files.game import Game

""" Main module for application """


def main():

    choice = prompts.new_or_load_game()
    if choice == 'LOAD':
        game = Game.load_game()
        game.terminal_start_main()        
    elif choice == 'NEW':
        game = Game.new_character()
        game.terminal_start_main()

if __name__ == '__main__':
    main()
