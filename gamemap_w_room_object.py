#Class for creating maps
class GameMap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = 'O'
        self.map_grid = []
    

    #Create a room for monster/tresure encounter
    def create_room(self):
        return Room()

    
    #Creating map
    def create_map(self):
        for _i in range(0, self.y):
            x_axis = []
        
            for _j in range(0, self.x):
        
                room = self.create_room()
                x_axis.append(room)
            self.map_grid.append(x_axis)
        
    def change_grid_sate(self, y, x, state):
        self.map_grid[y][x].change_state(state)


    #Prints map_grid in readable form
    def print_map_grid(self):

        temp_list = []
        for y in range(self.y):
            temp_string = f'{y+1} '
            for x in range(self.x):
                temp_string += f'{self.map_grid[y][x].get_state()} '
            temp_list.append(temp_string)
        
        for y in range(self.y, 0, -1):
            print(temp_list[y-1])

        space = ' '
        bottom_info_row = f'0{space}'
        for i in range(1, self.x+1):
            bottom_info_row += f'{i}{space}'
        print(bottom_info_row)
    

    #Prints out all objects in map_grid
    def print_object(self):
        for y in range(0, self.y):
            for x in range(0, self.x):
                print(self.map_grid[y][x])

    
    #Check boundaries inside map
    def check_bound(self, x, y):
        if (0 <= y < self.y):
            if (0 <= x < self.x):
                return True
    
        return False
    
    #Handles movement directions
    def make_direction(self, x, y, direction):
        directionsDict = {
            'U': (x, y+1),
            'R': (x+1, y),
            'D': (x, y-1),
            'L': (x-1, y)
            }
        
        return directionsDict[direction]
    
    #Move the player
    def make_move(self, x, y, direction):
        
        new_pos = self.make_direction(x, y, direction)
        self.map_grid[y][x] = self.player
        x = new_pos[0]
        y = new_pos[1]

        if self.check_bound(x, y) == True:
            self.map_grid[y][x] = self.player
        else:
            print("Not a position, you donkey!")
    
class Room:
    def __init__(self):
        self.state = '-'
    
    def change_state(self, new_state):
        self.state = new_state

    def spawn_monsters(self):
        #call funtion to generate monsters
        #save monsters to map
        pass

    def spawn_tressure(self):
        #call funtion to generate tresure
        #save tresure to map
        pass
    
    def won_room(self):
        #save to json something to indicate the room is completed
        #chnage json-side map_grid to "x" (completed)
        
        #chnage client side map_grid to "x" (completed)
        pass
    
    def get_state(self):
        return self.state


    

#test methods
playMap = GameMap(5, 5)
playMap.create_map()
playMap.change_grid_sate(0, 0, "X")
playMap.change_grid_sate(1, 1, "X")
playMap.change_grid_sate(2, 1, "X")
playMap.print_map_grid()
#playMap.print_object()