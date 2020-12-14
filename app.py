from utils.prompts import prompts
from game_files.game import Game

""" Main module for application """

def main():
    game = Game.terminal_create_hero()
    game.terminal_start_game()


if __name__ == '__main__':
    main()


