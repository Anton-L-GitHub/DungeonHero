from game_files import gamemap
from data.database.database import disc_load_character, disc_load_progress, disc_save_character, disc_save_progress
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
        self._room = Room('Dummy')
        self._monsters = []

    @classmethod
    def new_character(cls):
        character, game_map = prompts.new_game()
        new_game = cls(character, game_map)
        new_game.terminal_map_print()
        position = prompts.map_spawn_prompt()
        new_game.game_map.set_start_position(position)
        return new_game

    @classmethod
    def load_game(cls):
        user_choice = prompts.load_game()
        if user_choice == 'CHARACTER':
            character = cls.disc_load_game_character()
            game_map = prompts.create_new_map()
            position = prompts.map_spawn_prompt()
            game_map.set_start_position(position)
            return  cls(character, game_map)
        elif user_choice == 'GAME':
            game_map, character = cls.disc_load_game_progress()
            return cls(character, game_map)

    def terminal_map_print(self):
        return self.game_map.print_map_grid()

    def terminal_walk(self):
        self.terminal_map_print()
        next_room = self.player_move_next_room(prompts.map_move_direction())
        if not next_room:
            return False
        elif next_room == 'exit':
            self.terminal_exit()
        else:
            self._set_room(next_room)
            self._set_monsters()
            return self._room

    def terminal_exit(self):
        # disc_save_character(self.character)
        exit()

    def terminal_print_monster_health(self):
        monsters_hp = [
            f' {monster.get_name()}: {monster.get_health()}/{monster.get_start_health()} HP\n' for monster in self.room_get_monsters()]
        if monsters_hp:
            print(*monsters_hp)

    def terminal_print_fight_stats(self):
        prompts.clear_screen()
        print(f'\nYour health: {self.character.get_health()}/{self.character.get_start_health()} HP\n'
              f'Backpack items: {self.player_get_backpack_items()}\nBackpack value: {self.player_get_backpack_sum()}\n\nMonsters:')
        self.terminal_print_monster_health()

    def player_get_backpack_sum(self):
        return sum()

    def terminal_player_death(self):
        self.terminal_print_fight_stats()
        print('You died 🤕')
        self.terminal_exit()

    def terminal_start_main(self):
        prompts.clear_screen()
        print('The game has started')
        while True:
            next_room = self.terminal_walk()
            if next_room:
                turn_order = self.fight_get_turn_order()
                while self.monster_in_room():
                    fight = self.terminal_combat(turn_order)

                    if fight == 'ESCAPED':
                        break

                else:
                    self.player_gather_treasures()

    def terminal_combat(self, fighters):
        for fighter in fighters:

            if self.player_is_dead():
                self.terminal_player_death()

            elif not self.monster_in_room():
                break

            elif fighter == self.character:
                self.terminal_print_fight_stats()
                choice = prompts.fight_or_flight()
                if choice == 'FIGHT':
                    self.player_try_attack(self._monsters)

                elif choice == 'RUN':
                    if self.player_try_run_away():
                        print('\nYou ran away!')
                        return 'ESCAPED'
                self.terminal_print_fight_stats()
            else:
                self.monster_try_attack(fighter)

    def player_get_backpack_sum(self):
        return sum([item.get_value() for item in self.character.get_backpack()])

    def player_get_backpack_items(self):
        return [item.get_name() for item in self.character.get_backpack()]

    def player_move_next_room(self, direction: str) -> object:
        next_room = self.game_map.make_move(direction)
        self._set_room(next_room)
        self._set_monsters()
        return next_room

    def player_try_run_away(self):
        chance = self.character.get_agility() * 10
        if chance <= randint(1, 101):
            self.game_map.make_step_back()
            return True

    def player_gather_treasures(self):
        for treasure in self.room_get_treasures():
            self.character.add_to_backpack(treasure)

    def player_try_attack(self, monsters):
        for monster in monsters:
            self._player_attack(monster)

    def player_is_dead(self):
        if self.character.get_health() <= 0:
            return True

#########################################################################

    def monster_in_room(self):
        if len(self._monsters) > 0:
            return True
        else:
            return False

    def monster_try_attack(self, monster):
        player_dice_sum = dice_toss(self.character.get_agility())
        monster_dice_sum = dice_toss(monster.get_attack())
        if player_dice_sum < monster_dice_sum:
            self._damage_player()
            return True


#########################################################################

    def room_get_monsters(self):
        try:
            return self._room.content.get('enemies', [])
        except Exception:
            return False

    def room_get_treasures(self):
        return self._room.content.get('treasures', [])

    def fight_get_turn_order(self) -> list:
        result = {}
        result[self.character] = dice_toss(self.character.initiative)
        for monster in self._monsters:
            result[monster] = dice_toss(monster.get_initiative())
        result = sort_keys(result)
        return result


#########################################################################


    def disc_save_character(self):
        disc_save_character(self.character)

    def disc_save_progress(self):
        return disc_save_progress(self.character, self.game_map)

    @staticmethod
    def disc_load_game_character():
        character_name = input('Name hero: ')
        return disc_load_character(character_name)

    @staticmethod
    def disc_load_game_progress():
        character_name = input('Name hero: ')
        return disc_load_progress(character_name)
    

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

    def _damage_monster(self, monster: object):
        if monster.get_health() <= 0:
            return False
        monster.set_health(monster.get_health() - 1)

    def _damage_player(self):
        self.character.set_health(self.character.get_health() - 1)

    def _kill_monster(self, monster):
        try:
            self._monsters.remove(monster)
        except:
            return False

    def _set_room(self, room):
        self._room = room

    def _set_monsters(self):
        if isinstance(self._room, Room):
            self._monsters = self._room.content.get('enemies', [])
