

class Treasure():
    def __init__(self):
        self._name = "Treasure"
        self._value = 0
        self._rarity = 0

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
    def __init__(self):
        super().__init__()
        self._name = "Coins"
        self._value = 2
        self._rarity = 40


class Coin_pouch(Treasure):
    def __init__(self):
        super().__init__()
        self._name = "Coin pouch"
        self._value = 6
        self._rarity = 20


class Gold_jewelry(Treasure):
    def __init__(self):
        super().__init__()
        self._name = "Gold jewelry"
        self._value = 10
        self._rarity = 15


class Gemstone(Treasure):
    def __init__(self):
        super().__init__()
        self._name = "Gemstone"
        self._value = 14
        self._rarity = 10


class Treasure_chest(Treasure):
    def __init__(self):
        super().__init__()
        self._name = "Treasure chest"
        self._value = 20
        self._rarity = 5

