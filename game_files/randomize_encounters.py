import random
from game_files import enemies, treasures


class RandomizeEncounter():

    def __init__(self):
        self.content = []
        self.types = []

    # Prints the enemy_types as object
    def print_types_objects(self):
        for i in range(len(self.types)):
            self.types[i]

    # Spawns enemies based on rarity atribute
    def randomize(self):
        content = []
        for i in range(len(self.types)):
            if random.randint(1, 100) <= self.types[i].get_rarity():
                content.append(self.types[i])
        return content

    # Prints enemies generated from randomise_enemies
    def print_content(self):
        for i in self.content:
            print(self.content[i])

    # Prints enemies generated from randomise_enemies by name
    def print_content_name(self):
        for i in range(len(self.content)):
            print(self.content[i].get_name())

    # Returns enemys
    def return_content(self):
        return self.content


class RandomizeTreasures(RandomizeEncounter):

    def __init__(self):
        self.types = self.make_enemie_types()
        self.content = self.randomize()

    def make_enemie_types(self):
        treasures_types = [
            treasures.Coins(),
            treasures.Coin_pouch(),
            treasures.Gold_jewelry(),
            treasures.Gemstone(),
            treasures.Treasure_chest()
        ]

        return treasures_types


class RandomizeEnemies(RandomizeEncounter):

    def __init__(self):
        self.types = self.make_enemie_types()
        self.content = self.randomize()

    def make_enemie_types(self):
        enemie_types = [
            enemies.Giant_spider(),
            enemies.Skeleton(),
            enemies.Orc(),
            enemies.Troll()
        ]

        return enemie_types


# Test randomiseMonsterEncounter methods
'''
test_enemie = RandomizeEnemies()
test_enemie.print_content_name()


test_treasures = RandomizeTreasure()
test_treasures.print_content_name()
'''
