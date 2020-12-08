arrr = list('abcdefghijklmnop')

# Class for creating maps


class GameMap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = 'X'
        self.player_x = 0
        self.player_y = 0
        self.map_grid = []

    # Creating map
    def create_map(self):
        for _i in range(0, self.y):
            x = []

            for j in range(0, self.x):
                newRoom = Room(arrr[j])
                newTuple = ["-", newRoom]
                x.append(newTuple)
            self.map_grid.append(x)

    def get_map(self):
        return self.map_grid

    # Prints the map with inverted y axis
    def nice_print(self):
        temp_list_y = []
        temp_list_x = []
        for i in range(self.y):
            temp_list_x = []
            for j in range(self.x):
                temp_string = self.map_grid[i][j][0]
                temp_list_x.append(temp_string)

            temp_list_y.append(temp_list_x)

        for i in range(len(temp_list_y), 0, -1):
            string_temp = ' '.join(temp_list_y[i-1])
            print(f'{i} {string_temp}')

        bottom_info_row = ""
        for i in range(self.x+1):
            bottom_info_row += f'{i} '
        print(bottom_info_row)

    # Check boundaries inside map
    def check_bound(self, x, y):
        if (0 <= y < self.y):
            if (0 <= x < self.x):
                return True

        return False

    def set_start_position(self, x, y):
        self.player_x = x
        self.player_y = y
        self.map_grid[y][x] = 'X'

    # Handles movement directions
    def make_direction(self, x, y, direction):
        directionsDict = {
            'u': (x, y+1),
            'r': (x+1, y),
            'd': (x, y-1),
            'l': (x-1, y)
            }

        return directionsDict[direction]

    # Move the player
    def make_move(self, x, y, direction):

        new_pos = self.make_direction(x, y, direction)
        old_x = x
        old_y = y
        x = new_pos[0]
        y = new_pos[1]

        if self.check_bound(x, y):
            self.map_grid[old_y][old_x] = 'O'
            self.player_x = x
            self.player_y = y
            self.open_room(self.map_grid[y][x][1])
            self.map_grid[y][x] = self.player
        else:
            print("Not a position, you donkey!")

    def open_room(self, room):
        print(room.a)


class Room:

    # contructor for room add attributes later
    def __init__(self, att):
        self.a = att

    # Function for calling monsters, insert monster constructor here
    def spawn_monsters(self):
        pass

    # Function for calling treasures, insert treasure constructor here
    def spawn_treasure(self):
        pass

    # Function for escaping battles
    def room_escape(self):
        # insert method for throwing dices
        pass

    def win_room(self):
        pass


# test methods
playMap = GameMap(8, 8)
playMap.create_map()
playMap.set_start_position(0, 0)

input_dir = ''
while input_dir != 'e':
    input_dir = input("choose direction")
    playMap.make_move(playMap.player_x, playMap.player_y, input_dir)
    playMap.nice_print()
