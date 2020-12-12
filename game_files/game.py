from game_files import treasures
from utils.prompts import prompts
from utils.utils import dice_toss, sort_keys


""" Concerned with blabla """


class Game:

    """ Concerned with blabla """

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
        return f'{self.game_map.print_map_grid()}'

    def terminal_fight_or_flight(self):
        return prompts.fight_or_flight()

    def terminal_print_monster_health(self):
        monsters_hp = [f'{monster.get_name()}: {monster.get_health()} HP\n' for monster in self._monsters]
        print(*monsters_hp)

    def terminal_print_player_health(self):
        return f'You have {self.player_get_health()}'

    # Map / player

    def map_set_start_position(self, position: str):
        return self.game_map.set_start_position(position)

    def player_move_next_room(self, direction: str) -> object:
        next_room = self.game_map.make_move(direction)
        self._set_room(next_room)
        self._set_monsters()
        return next_room

    def player_get_backpack_sum(self):
        return sum([treasure.get_value() for treasure in self.character.backpack])

    def player_steal_treasures(self):
        [self.character.backpack.append(treasure)
        for treasure in self._room.room.get_contents()]

    def room_get_monsters(self):
        monsters = self._room.content['enemies']
        return monsters

    def fight_get_turn_order(self) -> list:
        result = {}
        result[self.character] = dice_toss(self.character.initiative)
        for monster in self._monsters:
            result[monster] = dice_toss(monster.get_initiative())
        result = sort_keys(result)
        return result


    def player_try_attack(self, monsters):
        for monster in monsters:
            self._player_attack(monster)


    def _player_attack(self, monster):
        player_dice_sum = dice_toss(self.character.get_attack())
        monster_dice_sum = dice_toss(monster.get_agility())
        if player_dice_sum > monster_dice_sum:
            self._damage_monster(monster)
            if monster.get_health() <= 0:
                self._kill_monster(monster)
        else: 
            return False

    def player_get_health(self):
        return self.character.get_health()


    def monster_try_attack(self, monster):
        player_dice_sum = dice_toss(self.character.get_agility())
        monster_dice_sum = dice_toss(monster.get_attack())
        if player_dice_sum > monster_dice_sum:
            self._damage_player()
            return True
        else: 
            return False

    def player_run_away(self):
        pass


    def _monsters_get_all_health(self):
        monsters = {}
        for monster in self._monsters:
            monsters[monster.get_name()] = monster.get_health()
        return monsters

    def _damage_monster(self, monster:object):
        if monster.get_health() <= 0:
            return False
        monster.set_health(monster.get_health() - 1)

    def _kill_monster(self, monster):
        try:
            self._monsters.remove(monster)
        except:
            return False
    
    def _damage_player(self):
        self.character.set_health(self.character.get_health() - 1)

    def _set_monsters(self):
        self._monsters = self.room_get_monsters()

    def _set_room(self, room):
        self._room = room


# set_room_cleared = om du vinner
# make_step_back = om du flyr
