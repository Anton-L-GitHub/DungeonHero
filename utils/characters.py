class Character:

    ''' Character blalbalbal '''
    
    def __init__(self):
        self.initative = 0
        self.health = 0
        self.attack = 0 
        self.agilty = 0
        self.backpack = []
        # Lägg till special-attack?

    def init_char_from_json(self):
        ''' Communicates with mapclass about player location '''
        pass

    def save_char_to_json(self):
        ''' Communicates with mapclass about player location '''
        pass
    
    def movement(self):
        ''' Communicates with mapclass about player location '''
        pass

    def special_ability(self):
        ''' A distinct ability for the character class '''
        pass



class Knight(Character):

    ''' Knight-class blablablabla '''

    def __init__(self):
        super().__init__()
        self.initative = 5
        self.health = 10
        self.attack = 6 
        self.agilty = 4

    def special_ability(self):
        return 'Sheild block!'


class Wizard(Character):

    ''' Knight-class blablablabla '''

    def __init__(self):
        super().__init__()
        self.initative = 5
        self.health = 10
        self.attack = 6 
        self.agilty = 4

    def special_ability(self):
        return 'Glow!'


class Theif(Character):

    ''' Knight-class blablablabla '''

    def __init__(self):
        super().__init__()
        self.initative = 5
        self.health = 10
        self.attack = 6 
        self.agilty = 4

    def special_ability(self):
        return 'Critical strike!'