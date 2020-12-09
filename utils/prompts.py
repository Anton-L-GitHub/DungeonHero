from lib.characters import Knight, Thief, Wizard

""" Concerned with input/utput in terminal """

CHARACTER_CHOISE = '\nChoose character:\n1: Knight\n2: Wizard\n3: Thief\n> '


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
