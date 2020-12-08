import random
import utils.enemies as enemies_py

class randomiseMonsterEncounter():
    def __init__(self):
        self.enemie_types = self.make_enemie_types()
        self.enemies = self.randomise_enemies()

    #Import enemies, mabye from json later?
    def make_enemie_types(self):
        enemie_types = [
            enemies_py.Giant_spider(),
            enemies_py.Skeleton(),
            enemies_py.Orc(),
            enemies_py.Troll()
            ]
        
        return enemie_types

    def print_enemie_types_objects(self):
        for i in range(len(self.enemie_types)):
            self.enemie_types[i]

    #Spawns enemies based on rarity atribute
    def randomise_enemies(self):
        enemies = []
        for i in range(len(self.enemie_types)):
            if random.randint(1, 100) <= self.enemie_types[i].get_rarity():
                enemies.append(self.enemie_types[i])
        return enemies
    
    def print_enemies(self):
        for i in self.enemies:
            print(self.enemies[i])
    
    def print_enemies_name(self):
        for i in range(len(self.enemies)):
            print(self.enemies[i].get_name())
    
    #Returns enemys
    def return_enemies(self):
        return self.enemies


#test = randomiseMonsterEncounter()
#test.print_enemies_name()
