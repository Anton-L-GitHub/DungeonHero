class GameMap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map_grid = []
    
    def create_map(self):
        for _i in range(0, self.y):
            x = []
        
            for _j in range(0, self.x):
        
                x.append("-")
            self.map_grid.insert(0, x)
    
    def print_map(self):
        count = self.y
        self.map_grid[0][0] = 'x'
        for x in self.map_grid:
            print(f'{count} {x}')
            count -= 1

playMap = GameMap(5, 5)
playMap.create_map()

playMap.print_map()