import os
from game_files.characters import Knight, Thief, Wizard
from game_files.gamemap import create_map_instance


CHARACTER_CHOISE = '\nChoose character:\n1: Knight\n2: Wizard\n3: Thief\n--- \n> '
MAP_MENU = '\nMap Difficulty: \n1: Small \n2: Medium \n3: Large \n--- \n> '
MAP_SPAWN = '\nSpawn on map: \n1: Bottom left \n2: Botton right \n\n3: Top Left \n4: Top right\n--- \n> '
USER_MOVE = '\n\tUp(W)\n Left(A)\tRight(D) \n\tDown(S)\n\r> '
FIGHT_OR_FLIGHT = "\nWhat do you want to do:\n1: FIGHT!\n2: TRY TO RUN AWAY\n> "

class prompts():

    def new_game():
        prompts.clear_screen()
        new_hero = prompts.choose_hero()
        new_hero.set_name(input(f'{new_hero.__class__.__name__} name: '))
        new_map = prompts.create_new_map()
        return new_hero, new_map


    def choose_hero() -> object:
        # prompts.clear_screen()
        user_choise = input(CHARACTER_CHOISE)
        while user_choise != '!QUIT':
            if user_choise == '1':
                return Knight()
            elif user_choise == '2':
                return Wizard()
            elif user_choise == '3':
                return Thief()
            user_choise = input(CHARACTER_CHOISE)
    
    def create_new_map():
        # prompts.clear_screen()
        user_input = input(MAP_MENU)
        while user_input != '!QUIT':
            if user_input == '1':
                return create_map_instance('small')
            elif user_input == '2':
                return create_map_instance('medium')
            elif user_input == '3':
                return create_map_instance('large')
            user_input = input(MAP_MENU)
    
    def map_spawn_prompt():
        # prompts.clear_screen()
        user_input = input(MAP_SPAWN)
        while user_input != '!QUIT':
            if user_input == '1':
                return ('b-l')
            elif user_input == '2':
                return ('b-r')
            elif user_input == '3':
                return ('t-l')
            elif user_input == '3':
                return ('t-r')
            print('Wrong input.. Try again!')
            user_input = input(MAP_SPAWN)
            prompts.clear_screen()


    def map_move_direction():
        user_input = input(USER_MOVE).upper()
        while user_input != '!QUIT':
            if user_input == 'W':
                return ('W')
            elif user_input == 'S':
                return ('S')
            elif user_input == 'A':
                return ('A')
            elif user_input == 'D':
                return ('D')
            user_input = input(USER_MOVE).upper()
            prompts.clear_screen()
            # Save in game.
    
    def fight_or_flight():
        # prompts.clear_screen()
        user_input = input(FIGHT_OR_FLIGHT)
        while user_input != '!QUIT':
            if user_input == '1':
                return ('FIGHT')
            elif user_input == '2':
                return ('RUN')
            user_input = input(FIGHT_OR_FLIGHT)
    
    def clear_screen():
        os.system('cls' if os.name=='nt' else 'clear') 
