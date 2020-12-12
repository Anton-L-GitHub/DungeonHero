from game_files.game import Game


""" Main module for application """


def main():
    # OBS! IF new game
    game = Game.terminal_new_game()

    print('The game has begun!')
    while True:
        game.terminal_map_print()
        next_room = game.terminal_make_move()
        monsters = game.room_get_monsters()

        if not next_room:
            print('Invalid move')
        elif monsters:
            print('Gulp! Monsters!')
            turn_order = game.fight_get_turn_order()
            while len(monsters) > 0 and game.player_get_health() > 0:
                print(monsters)
                for fighter in turn_order:
                    if fighter == game.character:
                        player_choice = game.terminal_fight_or_flight()
                        if player_choice == 'FIGHT':
                            game.player_try_attack(monsters)
                            game.terminal_print_monster_health()
                        elif player_choice == 'RUN':
                            print('Trying to run away!')
                    elif fighter in monsters:
                        game.monster_try_attack(fighter)
                        print(f'You got hit\nYour HP:{game.player_get_health()}')


if __name__ == '__main__':
    main()
