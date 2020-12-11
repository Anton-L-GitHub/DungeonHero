
""" Ememies module """


class Enemy:
    """ Character blalbalbal """

    def __init__(self):
        self._health = 0
        self._name = "Enemy"
        self._initiative = 0
        self._attack = 0
        self._agility = 0
        self.image = 'data/images/orc.png'
        self._rarity = 0

    def get_image(self):
        return self.image

    def set_health(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Health has to be of type Integer.")
        self._health = new_value

    def set_name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("Name has to be of type String.")
        self._name = new_name

    def set_initiative(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Initiative has to be of type Integer.")
        self._initiative = new_value

    def set_attack(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Attack has to be of type Integer.")
        self._attack = new_value

    def set_agility(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Agility has to be of type Integer.")
        self._agility = new_value

    def set_rarity(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Rarity has to be of type Integer.")
        self._rarity = new_value

    def get_health(self):
        return self._health

    def get_name(self):
        return self._name

    def get_initiative(self):
        return self._initiative

    def get_attack(self):
        return self._attack

    def get_agility(self):
        return self._agility

    def get_rarity(self):
        return self._rarity


class Giant_spider(Enemy):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._health = 1
        self._name = "Giant Spider"
        self._initiative = 7
        self._attack = 2
        self._agility = 3
        self._rarity = 20
        self.image = 'data/images/giant_spider.png'


class Skeleton(Enemy):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._health = 2
        self._name = "Skeleton"
        self._initiative = 4
        self._attack = 3
        self._agility = 3
        self._rarity = 15
        self.image = 'data/images/skeleton.png'


class Orc(Enemy):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._health = 3
        self._name = "Orc"
        self._initiative = 6
        self._attack = 4
        self._agility = 4
        self._rarity = 10
        self.image = 'data/images/orc.png'


class Troll(Enemy):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._health = 4
        self._name = "Troll"
        self._initiative = 2
        self._attack = 7
        self._agility = 2
        self._rarity = 5
        self.image = 'data/images/troll.png'
