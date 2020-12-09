class Character:
    """ Character blalbalbal """

    def __init__(self):
        self.initiative = 0
        self.health = 0
        self.attack = 0
        self.agility = 0
        self.backpack = []
        # Lägg till special-attack?

    def movement(self):
        """ Communicates with map-class about player location """
        pass

    def special_ability(self):
        """ A distinct ability for the character class """
        # Måste troligtvis utveckla utveckla stridssystem innan
        pass

    def __repr__(self):
        return self.__class__.__name__


class Knight(Character):
    """ Knight-class blablablabla """

    def __init__(self):
        super().__init__()
        self.initiative = 5
        self.health = 10
        self.attack = 6
        self.agility = 4

    def special_ability(self):
        # Måste troligtvis utveckla utveckla stridssystem innan 
        return 'Sheild block!'


class Wizard(Character):
    """ Wizard-class blablablabla """

    def __init__(self):
        super().__init__()
        self.initiative = 6
        self.health = 4
        self.attack = 9
        self.agility = 5

    def special_ability(self):
        """ A distinct ability for the character class """
        # Måste troligtvis utveckla utveckla stridssystem innan
        return 'Glow!'


class Thief(Character):
    """ Thief-class blablablabla """

    def __init__(self):
        super().__init__()
        self.initiative = 7
        self.health = 5
        self.attack = 5
        self.agility = 7

    def special_ability(self):
        """ A distinct ability for the character class """
        # Måste troligtvis utveckla utveckla stridssystem innan
        return 'Critical strike!'
