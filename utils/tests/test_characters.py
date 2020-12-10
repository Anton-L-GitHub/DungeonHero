import unittest
from lib import characters


class CharactersTests(unittest.TestCase):


    def setUp(self):
        self.Character = characters.Character()
        self.Knight = characters.Knight()
        self.Wizard = characters.Wizard()
        self.Theif = characters.Theif()


    def tearDown(self):
        pass

    def test_Character(self):
        self.assertIsInstance(self.Character, characters.Character)
        self.assertEqual(str(self.Character), self.Character.__class__.__name__)
    
    def test_Knight(self):
        self.assertIsInstance(self.Knight, characters.Knight)
        self.assertEqual(str(self.Knight), self.Knight.__class__.__name__)
    
    def test_Wizard(self):
        self.assertIsInstance(self.Wizard, characters.Wizard)
        self.assertEqual(str(self.Wizard), self.Wizard.__class__.__name__)
    
    def test_Theif(self):
        self.assertIsInstance(self.Theif, characters.Theif)
        self.assertEqual(str(self.Theif), self.Theif.__class__.__name__)
    