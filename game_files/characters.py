""" Character module """


class Character:
    """ Character blalbalbal """

    def __init__(self):
        self.name = None
        self.initiative = 0
        self.health = 0
        self.attack = 0
        self.agility = 0
        self.image = 'data/images/knight.png'
        self.room_image = 'data/images/knight_on_room.png'
        self.backpack_image = 'data/images/backpack.png'
        self.special_ability = None
        self.backpack = []
        self.start_health = self.health

    def set_health(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Health has to be of type Integer")
        if new_value <= 0:
            new_value = 0
        self.health = new_value

    def get_image(self):
        return self.image

    def get_name(self):
        return self.name

    def get_initiative(self):
        return self.initiative

    def get_health(self):
        return self.health
    
    def get_start_health(self):
        return self.start_health

    def get_attack(self):
        return self.attack

    def get_backpack(self):
        return self.backpack

    def get_agility(self):
        return self.agility

    def set_name(self, name):
        self.name = name

    def add_to_backpack(self, item:object):
        return self.backpack.append(item)

    def is_dead(self):
        if self.get_health() == 0:
            return True
        else:
            return False

    def parse_data(self, player_dict):
        self.__dict__.update(player_dict)

    # def __repr__(self):
    #     return self.__class__.__name__


class Knight(Character):
    """ Knight-class blablablabla """

    def __init__(self):
        super().__init__()
        self.initiative = 5
        self.health = 9
        self.attack = 6
        self.agility = 4
        self.image = 'data/images/knight.png'
        self.room_image = 'data/images/knight_on_room.png'
        self.special_ability = 'Sheild block'
        self.start_health = self.health

class Wizard(Character):
    """ Wizard-class blablablabla """

    def __init__(self):
        super().__init__()
        self.initiative = 6
        self.health = 4
        self.attack = 9
        self.agility = 5
        self.image = 'data/images/wizard.png'
        self.room_image = 'data/images/wizard_on_room.png'
        self.special_ability = 'Glow!'
        self.start_health = self.health


class Thief(Character):
    """ Thief-class blablablabla """

    def __init__(self):
        super().__init__()
        self.initiative = 7
        self.health = 5
        self.attack = 5
        self.agility = 7
        self.image = 'data/images/thief.png'
        self.room_image = 'data/images/thief_on_room.png'
        self.special_ability = 'Critical strike!'
        self.start_health = self.health