import random

class Combat:
    def __init__(self, combatants:list):
        self.combatants = [entity for entity in combatants]
        self.turn_order = self.set_turn_order(self.combatants)
        self.turn_cycle = 0

    def flee(self, entity):
        chance_to_flee = entity.get_agility() * 10
        return chance_to_flee

    def attack(self, attacker, defender):
        attack_value = self.dice_toss(attacker.get_attack())
        defend_value = self.dice_toss(defender.get_agility())
        return attack_value, defend_value
           
    def special_attack(self):
        pass

    def set_turn_order(self, entites):
        turn_order = list()
        for entity in self.combatants:
            turn_order.append((entity, self.dice_toss(entity.get_initiative())))
        return sorted(turn_order, key=lambda x:x[1], reverse=True)

    def is_entity_dead(self, entity):
        if entity.get_health() <= 0:
            return True

    def remove_entity(self, entity):
        self.turn_order.remove(entity)
        self.combatants.remove(entity[0])

    def get_next_object_in_turn_order(self):
        if self.turn_cycle >= len(self.turn_order):
            self.turn_cycle = 0
        entity, value = self.turn_order[self.turn_cycle]
        self.turn_cycle += 1
        return entity, value

    def dice_toss(self, ability:int):
        tot = 0
        for _ in range(ability):
            tot += random.randint(1, 7)
        return(tot)

# def a_demo_combat():
#     test_enemies = [enemies.Orc(), characters.Knight(), enemies.Giant_spider()]
#     combat = demo_combat.Combat(test_enemies)
#     total_turn = 0
#     for turn in range(0, 16):
#         try:
#             entity, value = combat.get_next_object_in_turn_order()
#             total_turn += 1
#             print(f"Turn {total_turn}: {entity} with starting value: {value}")
#             # Player demo_loop
#             if isinstance(entity, characters.Character):
#                 print("KNIGHT ATTACK:")
#                 for monster in combat.combatants:
#                     if isinstance(monster, enemies.Enemy):
#                         attack, defend = combat.attack(entity, monster)
#                         print("ATTACK", attack, ". DEFEND", defend)
#                         print("Dealth 1 damage to", monster)
#             # Monster demo_loop
#             if isinstance(entity, enemies.Enemy):
#                 print(entity.get_name(), "ATTACK:")
#                 for player in combat.combatants:
#                     if isinstance(player, characters.Character):
#                         attack, defend = combat.attack(entity, player)
#                         print("ATTACK", attack, ". DEFEND", defend)
#                         if attack > defend:
#                             print("Dealth 1 damage to", player)
#                         else:
#                             print(player.get_name(), "DEFENDED AND TOOK NO DAMAGE")
#         except Exception as e:
#             print(e)
#             pass
#     ## DEMO END

# a_demo_combat()

