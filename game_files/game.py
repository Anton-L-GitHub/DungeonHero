from utils.prompts import prompts
from utils.utils import dice_toss, sort_keys


""" Concerned with blabla """


class Game:

    def __init__(self, Character, GameMap):
        self.character = Character
        self.game_map = GameMap
        self._monsters = None
        self._room = None

    # Terminal 
    @classmethod
    def terminal_new_game(cls):
        character, game_map = prompts.new_game()
        new_game = cls(character, game_map)
        new_game.terminal_map_print()
        position = prompts.map_spawn_prompt()
        new_game.map_set_start_position(position)
        return new_game

    def terminal_make_move(self):
        return self.player_move_next_room(prompts.map_move_direction())

    def terminal_map_print(self):
        return f'\n\n{self.game_map.print_map_grid()}'

    # Map / player
    def map_set_start_position(self, position: str):
        return self.game_map.set_start_position(position)

    def player_move_next_room(self, direction: str) -> object:
        self._set_monsters(None)
        next_room = self.game_map.make_move(direction)
        self._set_room(next_room)
        return next_room

    def room_get_mosters(self, room: object):
        monsters = room.content['enemies']
        if monsters:
            return self.decide_turn(monsters)

    # Fight
    def decide_turn(self, monsters: list) -> list:
        result = {}
        result[self.character] = dice_toss(self.character.initiative)
        for monster in monsters:
            result[monster] = dice_toss(monster._initiative)
        sort_keys(result)
        return result

    def fight(self, fighters: list):
        for fighter in fighters:
            if fighter == self.character:
                pass

    def try_to_escape(self):
        pass

    def _set_monsters(self, monsters):
        self._monsters = monsters

    def _set_room(self, room):
        self._room = room
