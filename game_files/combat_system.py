import random

""" Concerned with combatsystem """


class Combat:

    def __init__(self):
        self.player = None
        self.monsters = None

    def get_turn_order(self, combatants):
        pass

    def roll_dice_per_char(self, char):
        dices = char.initiative
        for _ in range(dices):
            pass

    def sort_char_dict(self):
        pass


class Dice:
    def new(self):
        self.value = random.randint(1, 6)
        return self.value
