from utils.prompts import hero_prompt, map_prompt

""" Concerned with creating &  loading games """


START_MENU = '\n1: New game\n2: Load game\n0: Exit \n> '


class Game:
    """ Concerned with game stuff """

    def __init__(self):
        self.hero = ''
        self.character = None
        self.map = None

    def start_game(self):
        self.start_menu()
        self.map_menu()

    def create_hero(self, name):
        self.hero = name
        self.character = hero_prompt()

    def start_menu(self):
        user_input = input(START_MENU)
        while user_input != '0':
            if user_input == '1':
                return self.create_hero(input('Choose name: '))
            elif user_input == '2':
                # Load from json
                break
            user_input = input(START_MENU)

    def map_menu(self):
        self.map = map_prompt()
        self.map.set_start_position()

    def build_hero_from_disk(self):
        pass

    def save_hero_to_disk(self):
        pass
