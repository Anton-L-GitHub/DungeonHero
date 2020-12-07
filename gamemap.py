class GameMap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = 'X'
        self.map_grid = []
    
    def create_map(self):
        for _i in range(0, self.y):
            x = []
        
            for _j in range(0, self.x):
        
                x.append("-")
            self.map_grid.append(x)
    
    def print_map(self):
        count = 1
        for x in self.map_grid:
            print(f'{count} {x}')
            count += 1
    
    def check_bound(self, x, y):
        if (0 <= y <= self.y):
            if (0 <= x <= self.x):
                return True
    
        return False
    
    #temporary
    def movement(self, x, y):
        if self.check_bound(x, y) == False:
            self.map_grid[x][y] = self.player
        else:
            print("Not a position, you donkey!")



playMap = GameMap(5, 5)
playMap.create_map()
print(playMap.check_bound(0, 0))

playMap.print_map()