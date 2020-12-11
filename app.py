from game_files.game import Game


""" Main module for application """


def main():
    # OBS! IF new game
    game = Game.terminal_new_game()

    print('The game has begun!')
    while True:
        game.terminal_map_print()
        new_room = game.terminal_make_move()
        monsters = game.room_get_mosters(new_room)

        if not new_room:
            print('Invalid move')
        elif monsters:
            game.fight(monsters)

if __name__ == '__main__':
    main()
