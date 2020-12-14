from game_files.game import Game
from utils import prompts

""" Main module for application """


def main():
    game = Game.terminal_game()
    game.terminal_start_main()


if __name__ == '__main__':
    main()
