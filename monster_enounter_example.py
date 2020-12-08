import random

class randomiseMonsterEncounter():
    def __init__(self):
        self.monster_ecounter_list = []


    def randomise_monster(self):

        monsters_rarity = {'spider': 20, 'skeleton': 15, 'orch': 10, 'troll': 5}
        
        for key, value in monsters_rarity.items():
            if random.randint(1, 101) <= value :
                self.monster_ecounter_list.append(key)
    
        print(self.monster_ecounter_list)
    

test = randomiseMonsterEncounter()
test.randomise_monster()

