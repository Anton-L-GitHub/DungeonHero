from time import sleep
from utils.prompts import prompts
from game_files.game import Game

""" Main module for application """


def fight(turn_order):
    pass


def main():
    # OBS! IF new game
    game = Game.terminal_new_game()
    prompts.clear_screen()
    print('The game has begun!')
    while True:
        game.terminal_map_print()
        next_room = game.terminal_make_move()
        monsters = game.room_get_monsters()

        if not next_room:
            print('Invalid move')
        elif monsters:
            print('You can see something moving in the shadows!')
            game.terminal_print_fight_stats()
            turn_order = game.fight_get_turn_order()
            while len(monsters) > 0:
                for fighter in turn_order:

                    if fighter == game.character:
                        choice = game.terminal_fight_or_flight()

                        if choice == 'FIGHT':
                            print(choice)
                            game.player_try_attack(monsters)
                            game.terminal_print_monster_health()

                        elif choice == 'RUN':
                            print(choice)
                            game.player_try_run_away()
                        game.terminal_print_fight_stats()

                    elif fighter in monsters:
                        if game.player_is_dead():
                            print('YOU DIED! :(')
                            sleep(1)
                            exit()

                        monster_hit = game.monster_try_attack(fighter)
                        if monster_hit:
                            print(
                                f'{fighter.get_name()} injured you 1HP! 📛')
                        else:
                            print(f'Close call, the {fighter.get_name()} almost hit you! 😲')
                    
                    
                    elif len(monsters) <= 0:
                        print('You have killed them all!')
                        game.terminal_print_fight_stats()
                        break

                    

            game.player_gather_treasures()
            game.terminal_print_fight_stats()

if __name__ == '__main__':
    main()
