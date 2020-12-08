import monster_enounter_example as MSE

#Class for creating maps
class GameMap:
    def __init__(self, y, x):
        self.y = y # <--- chnage to self.y_max?
        self.x = x # <--- change to self.x_max?
        self.player = 'O'
        self.map_grid = []
    
    #Creates map with stored Room object in each grid
    def create_map(self):
        for y in range(0, self.y):
            x_axis = []
        
            for x in range(0, self.x):
                x_axis.append(Room(f'{y}{x}'))
            self.map_grid.append(x_axis)

    # Changes state of a grid 
    def change_grid_sate(self, y, x, state):
        self.map_grid[y][x].change_state(state)

    # Prints map_grid in readable form
    def print_map_grid(self):

        # Fetches grid state and converts...
        # self.map_grid's x axis list into 1 row string, (temp_x_string).
        # Stores temp_x_string in y axis list, (temp_y_list)
        temp_y_list = []
        for y in range(self.y):
            temp_x_string = f'{y+1} '
            for x in range(self.x):
                temp_x_string += f'{self.map_grid[y][x].get_room_state()} ' # <-- .get_room_sate could be switched for .get_room_name to get room name
            temp_y_list.append(temp_x_string)
        
        # Prints map with inverted y axis
        for y in range(self.y, 0, -1):
            print(temp_y_list[y-1])

        #Prints a x axis bottom row of numbers
        space = ' '
        bottom_info_row = f'0{space}'
        for i in range(1, self.x+1):
            bottom_info_row += f'{i}{space}'
        print(bottom_info_row)
    
    # Prints out all objects in map_grid
    def print_room_object(self):
        for y in range(0, self.y):
            for x in range(0, self.x):
                print(self.map_grid[y][x])
    
    # Prints out all objects name in map_grid
    def print_room_name(self):
        temp_list = []
        for y in range(0, self.y):
            for x in range(0, self.x):
                temp_list.append(self.map_grid[y][x].get_room_name())
        print(temp_list)

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
    
    #Move the player basic, prob outdated.
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
    def __init__(self, name):
        self.name = name
        self.state = '-'
        self.enemies = self.spawn_enemies()
    
    #Spawns enemyes in room, return list of 
    # Enemy objects from enemies.py
    def spawn_enemies(self):
        enemies = MSE.randomiseMonsterEncounter()
        return enemies.return_enemies()
    
    def get_room_name(self):
        return self.name
    
    # Prints name of enemies object  
    def enemies_name(self):
        for i in range(len(self.enemies)):
            print(self.enemies[i].get_name())
    
    # Changes Room state, example: explored = "X", unexplored = "-", looted = "O"?
    def change_state(self, new_state):
        self.state = new_state

    def spawn_tressure(self):
        #call funtion to generate tresure
        #save tresure to map
        pass
    
    def won_room(self):
        #save to json something to indicate the room is completed
        #chnage json-side map_grid to "x" (completed)
        
        #chnage client side map_grid to "x" (completed)
        pass
    
    # Retuns state of grid, example: explored = "X", unexplored = "-", looted = "O"?
    def get_room_state(self):
        return self.state


    

#test GameMap methods 

playMap = GameMap(5, 5)
playMap.create_map()
playMap.change_grid_sate(0, 0, "X")
playMap.change_grid_sate(1, 1, "X")
playMap.change_grid_sate(2, 1, "X")
playMap.print_map_grid()
playMap.print_room_name()
#playMap.print_object()


#Test Room methods 
'''
playRoom = Room("hej")
playRoom.spawn_enemies()
playRoom.enemies_name()
print(playRoom.get_room_name())
'''
