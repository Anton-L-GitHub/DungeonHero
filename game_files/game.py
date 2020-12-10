from game_files.combat_system import Combat
from utils.prompts import create_hero_prompt, map_create_prompt, map_spawn_prompt, start_menu_prompt, user_make_move

""" Concerned with creating & loading games """


class Game:
    """ Concerned with keeping track of hero, map and character """

    def __init__(self):
        self.hero_name = ''
        self.character = None
        self.map = None
        self.combat = Combat(self.character, self.map)

    def start_game(self):
        start_menu_prompt(self)
        next_room = self.map.make_move(self)
        if next_room == False:
            next_room = 

    def create_new_hero(self):
        self.hero_name = input('Choose name: ')
        self.character = create_hero_prompt()
        self.map_menu()
        self.map.print_map_grid()
        map_spawn_prompt(self.map)

    def map_menu(self):
        self.map = map_create_prompt()
        map_spawn_prompt(self.map)

    def load_game(self):
        pass

    def build_hero_from_disk(self):
        pass

    def save_hero_to_disk(self):
        pass


class Combat_system:
    """ Concerned with combat stuff """

    def __init__(self, character, map):
        self.map = None
        self.character = None

    def who_starts(self):
        pass

    def randomizer(self):
        pass
