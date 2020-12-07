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
        count = len(self.map_grid)

        bottom_info_row = ""
        for i in range(self.x+1):
            bottom_info_row += f'{i}    '
        print(bottom_info_row)

        for x in range(len(self.map_grid), 0, -1):
            print(f'{x} {self.map_grid[x-1]}')
            count -= 1
    
    def check_bound(self, x, y):
        if (0 <= y <= self.y):
            if (0 <= x <= self.x):
                return True
    
        return False
    
    def make_direction(self, x, y, direction):
        directionsDict = {
            'U': (x, y+1),
            'R': (x+1, y),
            'D': (x, y-1),
            'L': (x-1, y)
            }
        
        return directionsDict[direction]
    
    def make_move(self, x, y, direction):
        
        new_pos = self.make_direction(x, y, direction)
        self.map_grid[y][x] = 'O'
        x = new_pos[0]
        y = new_pos[1]

        if self.check_bound(x, y) == True:
            self.map_grid[y][x] = self.player
        else:
            print("Not a position, you donkey!")



playMap = GameMap(8, 8)
playMap.create_map()
playMap.make_move(0, 0, 'U')
playMap.make_move(0, 1, 'R')
playMap.print_map()