from utils.prompts import create_hero_prompt, map_create_prompt, map_spawn_prompt, start_menu_prompt

""" Concerned with creating & loading games """


class Game:
    """ Concerned with game stuff """

    def __init__(self):
        self.hero = ''
        self.character = None
        self.map = None

    def start_game(self):
        start_menu_prompt(self)
        map_spawn_prompt(self.map)

    def create_new_hero(self):
        self.hero = input('Choose name: ')
        self.character = create_hero_prompt()
        self.map_menu()
        self.map.print_map_grid()

    def load_game(self):
        pass

    def map_menu(self):
        self.map = map_create_prompt()
        map_spawn_prompt(self.map)

    def set_start_position(self):
        pass

    def build_hero_from_disk(self):
        pass

    def save_hero_to_disk(self):
        pass
