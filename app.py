from game_files.game import Game
from time import sleep

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
            while len(monsters) > 0:
                sleep(1)
                for fighter in turn_order:
                    if fighter == game.character:
                        player_choice = game.terminal_fight_or_flight()
                        if player_choice == 'FIGHT':
                            sleep(1)
                            print(f'AARRHH!!')
                            sleep(3)
                            game.player_try_attack(monsters)
                            game.terminal_print_monster_health()
                        elif player_choice == 'RUN':
                            print('Trying to run away!')
                            game.player_run_away()
                    elif fighter in monsters:
                        print(f'{fighter.get_name()} attacks you!\n')
                        sleep(3)
                        game.monster_try_attack(fighter)
                        print(f'You got hit\nYour HP:{game.player_get_health()}')
                        if game.player_get_health() >= 0:
                            print('YOU DIED! :(')
                            exit()
            game.player_steal_treasures()
            print('You cleared the room!')

if __name__ == '__main__':
    main()



