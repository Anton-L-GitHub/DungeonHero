
""" Treasures module """


class Treasure:
    """ blalbalbal """

    def __init__(self):
        self._name = "Treasure"
        self._value = 0
        self._rarity = 0
        self.image = 'data/images/coins.png'

    def get_image(self):
        return self.image

    def set_name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("Name has to be of type String.")
        self._name = new_name

    def set_value(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Value has to be of type Integer.")
        self._value = new_value

    def set_rarity(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Rarity has to be of type Integer.")
        self._rarity = new_value

    def get_name(self):
        return self._name

    def get_value(self):
        return self._value

    def get_rarity(self):
        return self._rarity


class Coins(Treasure):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._name = "Coins"
        self._value = 2
        self._rarity = 40
        self.image = 'data/images/coins.png'


class Coin_pouch(Treasure):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._name = "Coin pouch"
        self._value = 6
        self._rarity = 20
        self.image = 'data/images/coin_pouch.png'


class Gold_jewelry(Treasure):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._name = "Gold jewelry"
        self._value = 10
        self._rarity = 15
        self.image = 'data/images/gold_jewelry.png'


class Gemstone(Treasure):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._name = "Gemstone"
        self._value = 14
        self._rarity = 10
        self.image = 'data/images/gemstone.png'


class Treasure_chest(Treasure):
    """ blalbalbal """

    def __init__(self):
        super().__init__()
        self._name = "Treasure chest"
        self._value = 20
        self._rarity = 5
        self.image = 'data/images/treasure_chest.png'
