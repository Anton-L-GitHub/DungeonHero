from game_files.gamemap import create_map_instance
from game_files.characters import Knight, Thief, Wizard

""" Concerned displaying prompts in terminal """

START_MENU = '\n1: New game\n2: Load game\n0: Exit \n> '
CHARACTER_CHOISE = '\nChoose character:\n1: Knight\n2: Wizard\n3: Thief\n--- \n> '
MAP_MENU = '\nMap Difficulty: \n1: Small \n2: Medium \n3: Large \n---\n0: Exit \n> '
MAP_SPAWN = '\nSpawn: \n1: Bottom left \n2: Botton right \n\n3: Top Left \n4: Top right\n--- \n> '
USER_MOVE = "\n\tUp(W)\n Left(A)\tRight(D) \n\tDown(S)\n\r> "


def start_menu_prompt(game):
    user_input = input(START_MENU)
    while user_input != '0':
        if user_input == '1':
            return game.create_new_hero()
        elif user_input == '2':
            return game.load_game()
        user_input = input(START_MENU)


def create_hero_prompt():
    user_choise = input(CHARACTER_CHOISE)
    while user_choise != '0':
        if user_choise == '1':
            return Knight()
        elif user_choise == '2':
            return Wizard()
        elif user_choise == '3':
            return Thief()
        else:
            user_choise = input(CHARACTER_CHOISE)


def map_create_prompt():
    user_input = input(MAP_MENU)
    while user_input != '!QUIT':
        if user_input == '1':
            return create_map_instance('small')
        elif user_input == '2':
            return create_map_instance('medium')
        elif user_input == '3':
            return create_map_instance('large')
        user_input = input(MAP_MENU)


def map_spawn_prompt(the_map):
    user_input = input(MAP_SPAWN)
    while user_input != '!QUIT':
        if user_input == '1':
            return the_map.set_start_position('b-l')
        elif user_input == '2':
            return the_map.set_start_position('b-r')
        elif user_input == '3':
            return the_map.set_start_position('t-l')
        elif user_input == '3':
            return the_map.set_start_position('t-r')
        else:
            print('Wrong input.. Try again!')
        user_input = input(MAP_SPAWN)


def user_make_move(the_map):
    user_input = input(USER_MOVE).upper()
    while user_input != '!QUIT':
        if user_input == 'W':
            return the_map.make_move('W')
        elif user_input == 'S':
            return the_map.make_move('S')
        elif user_input == 'A':
            return the_map.make_move('A')
        elif user_input == 'D':
            return the_map.make_move('D')
        else:
            print('Wrong input.. Try again!')
            the_map.print_map_grid()
        user_input = input(USER_MOVE)
