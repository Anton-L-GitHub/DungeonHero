import randomize_encounters as ran_enc_py


# Class for creating maps
class GameMap:
    def __init__(self, x, y):
        self.x_max = x
        self.y_max = y
        self.player_x = 0
        self.player_y = 0
        self.map_grid = []

    # Creating map
    def create_map(self):
        for y in range(0, self.y_max):
            x_axis = []

            for x in range(0, self.x_max):
                x_axis.append(EncounterRoom(f'{y}{x}'))
            self.map_grid.append(x_axis)

    def get_room_at_grid(self):
        return self.map_grid[self.player_y][self.player_x]

    # Prints the map with inverted y axis
    def print_map_grid(self):

        # Fetches grid state and converts...
        # self.map_grid's x axis list into 1 row string, (temp_x_string).
        # Stores temp_x_string in y axis list, (temp_y_list)
        temp_y_list = []
        for y in range(self.y_max):
            temp_x_string = f'{y+1} '
            for x in range(self.x_max):

                temp_x_string += f'{self.map_grid[y][x].get_room_state()} '
            temp_y_list.append(temp_x_string)

        # Prints map with inverted y axis
        for y in range(self.y_max, 0, -1):
            print(temp_y_list[y-1])

        # Prints a x axis bottom row of numbers
        space = ' '
        bottom_info_row = f'0{space}'
        for i in range(1, self.x_max+1):
            bottom_info_row += f'{i}{space}'
        print(bottom_info_row)

    # Check boundaries inside map
    def check_bound(self, x, y):
        if 0 <= y < self.y_max:
            if 0 <= x < self.x_max:
                return True

        return False

    # Handles movement directions
    def make_direction(self, x, y, direction):
        directionsDict = {
            'W': (x, y+1),
            'A': (x-1, y),
            'S': (x, y-1),
            'D': (x+1, y)
        }

        return directionsDict[direction]

    def make_start_position_template(self, corner):
        template = {
            'b-l': (0, 0),
            't-l': (self.y_max-1, 0),
            'b-r': (0, self.x_max-1),
            't-r': (self.y_max-1, self.x_max-1)
        }
        return template[corner]

    def set_start_position(self, corner):
        corner_tuple = self.make_start_position_template(corner)
        self.player_y = corner_tuple[0]
        self.player_x = corner_tuple[1]
        self.map_grid[self.player_y][self.player_x].set_state('X')
        self.set_exit_room(corner_tuple)

    def set_exit_room(self, corner):
        corner1 = - corner[0] + self.y_max - 1
        corner2 = - corner[1] + self.x_max - 1
        self.map_grid[corner1][corner2].set_state('E')

    # Move the player
    def make_move(self, direction):

        new_pos = self.make_direction(self.player_x, self.player_y, direction)
        old_x = self.player_x
        old_y = self.player_y
        x = new_pos[0]
        y = new_pos[1]

        if self.check_bound(x, y):
            self.map_grid[old_y][old_x].set_state('O')
            self.player_x = x
            self.player_y = y
            self.map_grid[y][x].set_state('X')

            return self.get_room_at_grid()
        else:
            print("Not a position, you donkey!")

            return False


class Room:
    def __init__(self, name):
        self.name = name
        self.state = '-'
        self.description = ''
        self.content = {}

    # Retuns state of grid
    def get_room_state(self):
        return self.state

    def get_room_name(self):
        return self.name

    # Changes Room state
    def set_state(self, new_state):
        self.state = new_state

    def is_room_empty(self):
        if len(self.content) > 0:
            return True
        else:
            return False

class EncounterRoom(Room):
    def __init__(self, name):
        super().__init__(name)
        self.enemies = self.spawn_enemies()
        self.treasures = self.spawn_treasures()
        self.content['enemies'] = self.enemies
        self.content['treasure'] = self.treasures

    # Spawns enemyes in room, return list of
    # Enemy objects from enemies.py
    def spawn_enemies(self):
        enemies = ran_enc_py.RandomizeEnemies()
        return enemies.return_content()

    def get_contents(self):
        return self.content

    def spawn_treasures(self):
        treasures = ran_enc_py.RandomizeTreasures()
        return treasures.return_content()

    # Prints name of enemies object
    def enemies_names(self):
        for i in range(len(self.enemies)):
            print(self.enemies[i].get_name())

    def treasures_names(self):
        for i in range(len(self.treasures)):
            print(self.treasures[i].get_name())

    def won_room(self):
        # save to json something to indicate the room is completed
        # chnage json-side map_grid to "x" (completed)

        # chnage client side map_grid to "x" (completed)
        pass


# Create map instance

def create_map_instance(index):
    template = {
        'small': 4,
        'medium': 5,
        'large': 8
    }
    playMap = GameMap(template[index], template[index])
    playMap.create_map()

    return playMap


# test methods
'''
playMap = GameMap(8, 8)
playMap.create_map()
playMap.set_start_position('t-r')
playMap.print_map_grid()
room00 = playMap.get_room_at_grid(0, 0)
print(room00.get_room_name())
print(room00.get_room_state())
'''

'''
playRoom = Room("hej")
playRoom.treasures_name()
playRoom.enemies_name()
'''

playMap = GameMap(8, 8)
playMap.create_map()
playMap.set_start_position('t-r')
input_dir = ''
while input_dir != 'e':
    input_dir = input("choose direction")
    print(playMap.make_move(input_dir))
    playMap.print_map_grid()
    

    

