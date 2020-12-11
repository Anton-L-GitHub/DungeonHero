from game_files.game import Game
from data.database import database 

""" Main module for application """


def main():
    game = Game()
    game.start_game()


if __name__ == '__main__':
    main()


