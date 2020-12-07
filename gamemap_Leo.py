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
        x = new_pos[0]
        y = new_pos[1]

        if self.check_bound(x, y) == True:
            self.map_grid[x][y] = self.player
        else:
            print("Not a position, you donkey!")



playMap = GameMap(5, 5)
playMap.create_map()
playMap.make_move(0, 0, 'U')
