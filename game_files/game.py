from utils.utils import dice_toss
from utils.prompts import create_hero_prompt, map_create_prompt, map_spawn_prompt, start_menu_prompt, user_make_move
from data.database import database

""" Concerned with creating & loading games """


class Game:
    """ Concerned with keeping track of hero, map and character """

    def __init__(self):
        self.character = None
        self.map = None

    def start_game(self):
        start_menu_prompt(self)
        self.main_game()

    def main_game(self):
        print('The game has begun!')
        while True:
            print('\n')
            self.map.print_map_grid()
            room = user_make_move(self.map)
            if room == False:
                print('Invalid move!')
                continue
            elif room.enemies:
                print('MONSTERS')
                print(self.fight_enemy(room))
                

    def create_new_hero(self, hero_name):
        self.character = create_hero_prompt()
        self.character.name = hero_name
        self.new_map()

    def new_map(self):
        self.map = map_create_prompt()
        map_spawn_prompt(self.map)

    def fight_enemy(self, room):
        monsters = room.content['enemies']
        return self.decide_turn(monsters)

    def decide_turn(self, monsters):
        result = {}
        result[self.character] = dice_toss(self.character.initiative)
        for monster in monsters:
            result[monster] = dice_toss(monster._initiative)
        result = list(dict(sorted(result.items(), key=lambda item: item[1], reverse=True)).keys())
        return result


    def load_game(self):
        pass

    def build_hero_from_disk(self):
        pass

    def save_hero_to_disk(self):
        database.disc_save_character(self.character)


class Combat_system:
    """ Concerned with combat stuff """

    def __init__(self, room):
        self.map = None
        self.character = None

    def who_starts(self):
        pass

    def randomizer(self):
        pass
