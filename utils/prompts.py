from game_files.gamemap import create_map_instance
from game_files.characters import Knight, Thief, Wizard

""" Concerned displaying prompts in terminal """

CHARACTER_CHOISE = '\nChoose character:\n1: Knight\n2: Wizard\n3: Thief\n---\n0: Exit \n> '
MAP_MENU = '\nMap Difficulty: \n1: Small \n2: Medium \n2: Large \n---\n0: Exit \n> '


def hero_prompt():
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

def map_prompt():
        user_input = input(MAP_MENU)
        while user_input != '0':
            if user_input == '1':
                return create_map_instance('small')
            elif user_input == '2':
                return create_map_instance('medium')
            elif user_input == '3':
                return create_map_instance('large')
            user_input = input(MAP_MENU)



