import unittest
from lib import enemies


class MonsterTests(unittest.TestCase):

    def setUp(self):
        self.enemy = enemies.Enemy()
        self.giant_spider = enemies.Giant_spider()
        self.skeleton = enemies.Skeleton()
        self.orc = enemies.Orc()
        self.troll = enemies.Troll()
    
    def tearDown(self):
        pass

    def test_enemy_setup_ok(self):
        self.assertIsInstance(self.enemy, enemies.Enemy)
        self.assertEqual(self.enemy._health, 0)
        self.assertEqual(self.enemy._name, 'Enemy')
        self.assertEqual(self.enemy._initiative, 0)
        self.assertEqual(self.enemy._attack, 0)
        self.assertEqual(self.enemy._agility, 0)
        self.assertEqual(self.enemy._rarity, 0)

    def test_enemy_set_health_ok(self):
        self.enemy.set_health(10)
        self.assertEqual(self.enemy._health, 10)
        self.giant_spider.set_health(10)
        self.assertEqual(self.giant_spider._health, 10)
        self.skeleton.set_health(500)
        self.assertEqual(self.skeleton._health, 500)
        self.orc.set_health(150)
        self.assertEqual(self.orc._health, 150)
        self.troll.set_health(177)
        self.assertEqual(self.troll._health, 177)

    def test_enemy_set_health_fail(self):
        with self.assertRaises(TypeError):
            self.enemy.set_health("10")
        with self.assertRaises(TypeError):
            self.enemy.set_health(0.1)
    
    def test_enemy_get_health_ok(self):
        self.assertIsInstance(self.enemy.get_health(), int)
        self.assertEqual(self.enemy.get_health(), 0)
        self.assertEqual(self.giant_spider.get_health(), 1)
        self.assertEqual(self.skeleton.get_health(), 2)
        self.assertEqual(self.orc.get_health(), 3)
        self.assertEqual(self.troll.get_health(), 4)

    def test_enemy_set_name_ok(self):
        self.enemy.set_name("Lethal Spiderling")
        self.assertEqual(self.enemy._name, 'Lethal Spiderling')

    def test_enemy_set_name_fail(self):
        with self.assertRaises(TypeError):
            self.enemy.set_name(123)

    def test_enemy_set_initiative_ok(self):
        self.enemy.set_initiative(10)
        self.assertEqual(self.enemy._initiative, 10)

    def test_enemy_set_initiative_fail(self):
        with self.assertRaises(TypeError):
            self.enemy.set_initiative("100")

    def test_enemy_set_attack_ok(self):
        self.enemy.set_attack(55)
        self.assertEqual(self.enemy._attack, 55)

    def test_enemy_set_attack_fail(self):
        with self.assertRaises(TypeError):
            self.enemy.set_attack("100")
        with self.assertRaises(TypeError):
            self.enemy.set_attack(0.1)

    def test_enemy_set_agility_ok(self):
        self.enemy.set_agility(44)
        self.assertEqual(self.enemy._agility, 44)

    def test_enemy_set_agility_fail(self):
        with self.assertRaises(TypeError):
            self.enemy.set_agility("100")
        with self.assertRaises(TypeError):
            self.enemy.set_agility(0.1)

    def test_enemy_set_rarity_ok(self):
        self.enemy.set_rarity(100)
        self.assertEqual(self.enemy._rarity, 100)

    def test_enemy_set_rarity_fail(self):
        with self.assertRaises(TypeError):
            self.enemy.set_rarity("hej")
        with self.assertRaises(TypeError):
            self.enemy.set_rarity(0.1)

    def test_enemy_get_name(self):
        self.assertEqual(self.enemy.get_name(), "Enemy")

    def test_enemy_get_initiative(self):
        self.assertEqual(self.enemy.get_initiative(), 0)

    def test_enemy_get_attack(self):
        self.assertEqual(self.enemy.get_attack(), 0)

    def test_enemy_get_agility(self):
        self.assertEqual(self.enemy.get_agility(), 0)

    def test_enemy_get_rarity(self):
        self.assertEqual(self.enemy.get_rarity(), 0)

    def test_enemies_giant_spider_ok(self):
        self.assertIsInstance(self.giant_spider, enemies.Giant_spider)
        self.assertEqual(self.giant_spider._health, 1)
        self.assertEqual(self.giant_spider._name, 'Giant Spider')
        self.assertEqual(self.giant_spider._initiative, 7)
        self.assertEqual(self.giant_spider._attack, 2)
        self.assertEqual(self.giant_spider._agility, 3)
        self.assertEqual(self.giant_spider._rarity, 20)

    def test_enemies_skeleton_ok(self):
        self.assertIsInstance(self.skeleton, enemies.Skeleton)
        self.assertEqual(self.skeleton._health, 2)
        self.assertEqual(self.skeleton._name, 'Skeleton')
        self.assertEqual(self.skeleton._initiative, 4)
        self.assertEqual(self.skeleton._attack, 3)
        self.assertEqual(self.skeleton._agility, 3)
        self.assertEqual(self.skeleton._rarity, 15)

    def test_enemies_orc_ok(self):
        self.assertIsInstance(self.orc, enemies.Orc)
        self.assertEqual(self.orc._health, 3)
        self.assertEqual(self.orc._name, 'Orc')
        self.assertEqual(self.orc._initiative, 6)
        self.assertEqual(self.orc._attack, 4)
        self.assertEqual(self.orc._agility, 4)
        self.assertEqual(self.orc._rarity, 10)
    
    def test_enemies_troll_ok(self):
        self.assertIsInstance(self.troll, enemies.Troll)
        self.assertEqual(self.troll._health, 4)
        self.assertEqual(self.troll._name, 'Troll')
        self.assertEqual(self.troll._initiative, 2)
        self.assertEqual(self.troll._attack, 7)
        self.assertEqual(self.troll._agility, 2)
        self.assertEqual(self.troll._rarity, 5)
