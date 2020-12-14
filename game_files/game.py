from game_files.gamemap import Room
from utils.prompts import prompts
from utils.utils import dice_toss, sort_keys
from random import randint

""" Concerned with blabla """


class Game:

    """ Concerned with blabla """

    def __init__(self, Character, GameMap):
        self.character = Character
        self.game_map = GameMap
        self._room = Room('ERROR_ROOM')
        self._monsters = self._room.content.get('enemies')
        

    # Terminal methods
    @classmethod
    def terminal_create_hero(cls):
        character, game_map = prompts.new_game()
        new_game = cls(character, game_map)
        new_game.terminal_map_print()
        position = prompts.map_spawn_prompt()
        new_game.map_set_start_position(position)
        return new_game

    def terminal_make_move(self):
        next_room = self.player_move_next_room(prompts.map_move_direction())
        if next_room == 'exit':
            self.terminal_exit()
        else:
            self._set_room(next_room)
            self._set_monsters()
            return next_room
            

    def terminal_exit(self):
        # disc_save_character(self.character)
        exit()

    def terminal_map_print(self):
        return f'{self.game_map.print_map_grid()}'

    def terminal_fight_or_flight(self):
        return prompts.fight_or_flight()

    def terminal_print_monster_health(self):
        monsters_hp = [f' {monster.get_name()}: {monster.get_health()}/{monster.get_start_health()} HP\n' for monster in self.room_get_monsters()]
        if monsters_hp:
            print(*monsters_hp) 

    def terminal_print_player_health(self):
        print(f'You have {self.player_get_health()}/{self.player_get_start_health()}') 

    def terminal_print_player_backpack(self):
        print(f'You have {self.player_get_backpack_sum()} worth of treasures') 

    def terminal_print_fight_stats(self):
        prompts.clear_screen()
        print(f'You are in trouble! \nYour health: {self.character.get_health()}/{self.character.get_start_health()} HP\n'
            f'Backpack items: {self.player_get_backpack_items()}\nBackpack value: {self.player_get_backpack_sum()}\n\nMonsters:')
        self.terminal_print_monster_health()

    def terminal_player_death(self):
        prompts.clear_screen()
        print('You died 🤕')
        self.terminal_exit()

    def terminal_start_game(self):
        print('The game has begun!')
        while True:
            self.terminal_map_print()
            next_room = self.terminal_make_move()
            if not next_room:
                continue
            else:
                turn_order = self.fight_get_turn_order()
                while len(self._monsters) > 0:
                    if self.terminal_combat(turn_order) == 'ESCAPED':
                        print('\nYou have escaped the dungeon!')
                        break 
                    self.player_gather_treasures()
                    print('\nYou killed the monsters')

        
    def terminal_combat(self, turn_order):
            for fighter in turn_order:

                if self.player_check_is_dead():
                    self.terminal_player_death()

                elif fighter == self.character:
                    choice = self.terminal_fight_or_flight()
                    
                    if choice == 'FIGHT':
                        self.player_try_attack(self._monsters)

                    elif choice == 'RUN':
                        if self.player_try_run_away():
                            print('\nYou ran away!')
                            return 'ESCAPED'

                    self.terminal_print_fight_stats()
                else:
                    self.monster_try_attack(fighter)


    # Map methods

    def map_set_start_position(self, position: str):
        return self.game_map.set_start_position(position)

    def room_get_monsters(self):
        try:
            return self._room.content.get('enemies', [])
        except Exception:
            return False

    def room_get_treasures(self):
        return self._room.content.get('treasures', [])

    def room_set_empty(self):
        self._room.set_room_cleared()

    # Player methods

    def player_move_next_room(self, direction: str) -> object:
        next_room = self.game_map.make_move(direction)
        self._set_room(next_room)
        self._set_monsters()
        return next_room

    def player_get_backpack_sum(self):
        return sum([item.get_value() for item in self.character.get_backpack()])

    def player_get_backpack_items(self):
        return [item.get_name() for item in self.character.get_backpack()]

    def player_gather_treasures(self):
        for treasure in self.room_get_treasures():
            self.character.add_to_backpack(treasure)

    def player_get_start_health(self):
        return self.character.get_start_health()

    def player_get_health(self):
        return self.character.get_health()

    def player_try_attack(self, monsters):
        for monster in monsters:
            self._player_attack(monster)

    def player_try_run_away(self):
        chance = self.character.get_agility() * 10
        if chance <= randint(1,101):
            self.game_map.make_step_back()
            return True
        else:
            return False

    def player_check_is_dead(self):
        return self.character.is_dead()

    # Combat methods

    def monster_try_attack(self, monster):
        player_dice_sum = dice_toss(self.character.get_agility())
        monster_dice_sum = dice_toss(monster.get_attack())
        if player_dice_sum < monster_dice_sum:
            self._damage_player()
            return True
        else: 
            return False

    def fight_get_turn_order(self) -> list:
        result = {}
        result[self.character] = dice_toss(self.character.initiative)
        for monster in self._monsters:
            result[monster] = dice_toss(monster.get_initiative())
        result = sort_keys(result)
        return result

    def _player_attack(self, monster):
        player_dice_sum = dice_toss(self.character.get_attack())
        monster_dice_sum = dice_toss(monster.get_agility())
        if player_dice_sum > monster_dice_sum:
            self._damage_monster(monster)
            if monster.get_health() <= 0:
                self._kill_monster(monster)

    def _monsters_get_all_health(self):
        monsters = {}
        for monster in self._monsters:
            monsters[monster.get_name()] = monster.get_health()
        return monsters

    def _damage_monster(self, monster:object):
        if monster.get_health() <= 0:
            return False
        monster.set_health(monster.get_health() - 1)

    def _damage_player(self):
        if self.character.get_health() <= 0:
            return 'TEMP You dead man TEMP'
        self.character.set_health(self.character.get_health() - 1)

    def _kill_monster(self, monster):
        try:
            self._monsters.remove(monster)
        except:
            return False
    
    # Cls setters

    def _set_monsters(self):
        self._monsters = self.room_get_monsters()

    def _set_room(self, room):
        self._room = room


# set_room_cleared = om du vinner
# make_step_back = om du flyr
# exit_room = retunerar 'exit'