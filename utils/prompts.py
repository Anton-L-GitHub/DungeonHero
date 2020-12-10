from game_files.gamemap import create_map_instance
from game_files.characters import Knight, Thief, Wizard

""" Concerned displaying prompts in terminal """

START_MENU = '\n1: New game\n2: Load game\n0: Exit \n> '
CHARACTER_CHOISE = '\nChoose character:\n1: Knight\n2: Wizard\n3: Thief\n--- \n> '
MAP_MENU = '\nMap Difficulty: \n1: Small \n2: Medium \n2: Large \n---\n0: Exit \n> '
MAP_SPAWN = '\nSpawn: \n1: Bottom left \n2: Botton right \n\n3: Top Left \n4: Top right\n--- \n> '
USER_MOVE = "It's time!\nWhere do you want to go? \nUp(W)  Down(S) \nLeft(A) Right(D)"


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


def map_spawn_prompt(map):
    user_input = input(MAP_SPAWN)
    while user_input != '!QUIT':
        if user_input == '1':
            return map.set_start_position('b-l')
        elif user_input == '2':
            return map.set_start_position('b-r')
        elif user_input == '3':
            return map.set_start_position('t-l')
        elif user_input == '3':
            return map.set_start_position('t-r')
        user_input = input(MAP_MENU)


def user_make_move():
    user_input = input(USER_MOVE)
    while user_input != '!QUIT':
        if user_input == 'W':
            return map.set_start_position('W')
        elif user_input == 'S':
            return map.set_start_position('S')
        elif user_input == 'A':
            return map.set_start_position('A')
        elif user_input == 'D':
            return map.set_start_position('D')

        user_input = input(MAP_MENU)
