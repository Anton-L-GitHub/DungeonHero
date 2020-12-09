from lib.characters import Knight, Thief, Wizard

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
                # get small map obj
                pass GameMap.add_new_map('Small')
            elif user_input == '2':
                # get medium map obj
                pass
            elif user_input == '3':
                # get large map obj
                pass
            user_input = input(MAP_MENU)



