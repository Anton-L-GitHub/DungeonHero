class Noughts_And_Crosses:
    def __init__(self, arena_size, in_rows_to_win):
        self.arena_size = arena_size
        self.in_rows_to_win = in_rows_to_win
        self.arena = []
        self.symbols = ['x', 'o']
        self.rounds_played = 0
        self.arena_slots = int(pow(arena_size, 2))
        self.players_list = []
        self.debug_dir_list = ["up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left"]
        self.axle_symbol = ["y", "x"]
    
# Arena related-------------------------------------
    def create_arena(self):
        x_axle = []
    
        self.arena.clear()
        for y in range(self.arena_size):
            for x in range(self.arena_size):
                x_axle.append(' ')
            self.arena.append(list(x_axle.copy()))
            x_axle.clear()
    
    def nice_print(self):
        temp_list = []
        for i in range(self.arena_size):
            temp_string = ' '.join(self.arena[i])
            temp_list.append(temp_string)
    
        for i in range(self.arena_size, 0, -1):
            print(f'{i} {temp_list[i-1]}')

        bottom_info_row = ""
        for i in range(self.arena_size+1):
            bottom_info_row += f'{i} '
        print(bottom_info_row)

#  Inputs----------------------------------------------
    def try_input(self, player, axle):
        temp_input_text = f'Player \"{self.symbols[player]}\" enter cordinate for \"{axle}\": '
        print(temp_input_text, end="")
        while True:
            temp_input = input()
            try:
                temp_input = int(temp_input)
                return temp_input-1
            except ValueError:
                print(f'\"{temp_input}\" is not an interger, try again:', end = " ")
       
    def try_inside_arena(self, y, x):
        if(0 <= y <= self.arena_size):
            if(0 <= x <= self.arena_size):
                return True
            else:
                print("Cordinate outside arena, try again:", end = " ")
                return False
        else:
            print("Cordinate outside arena, try again:", end = " ")
            return False

    '''
    def try_inside_arena(self, y, x):
        if(0 <= y, x <= self.arena_size):
            return True
        else:
            print("Cordinate outside arena, try again:", end = " ")
            return False
    '''

    def try_empty_slot(self, y, x):
        if(self.arena[y][x] == ' '):
            return True
        else:
            print("Slot already taken, try again.")
            return False

    def save_play(self, y, x, player):
        player = self.symbols[player]
        self.arena[y][x] = player

    def make_play(self, player):
        while True:
            x_cord = self.try_input(player, "x")
            y_cord = self.try_input(player, "y")
            if(self.try_inside_arena(y_cord, x_cord) is not True):
                continue
            if(self.try_empty_slot(y_cord, x_cord) is not True):
                continue
            break
        self.save_play(y_cord, x_cord, player)

        self.nice_print()

        win_or_continue = self.in_a_row_searcher(y_cord, x_cord, player)

        return win_or_continue


# Winner search related-----------------------------------------
    def y_step_generator(self, y, direction_index, i):
        if(direction_index in {0, 1, 7}): #up
            return y-i
        if(direction_index in {3, 4, 5}): #down
            return y+i
        else: #none
            return y
    
    def x_step_generator(self, x, direction_index, i):
        if(direction_index in {1, 2, 3}): #right
            return x+i
        if(direction_index in {5, 6, 7}): #left
            return x-i
        else: #none
            return x

    def direction_searcher_setup(self, y, x):

        up = y - (self.in_rows_to_win-1)
        right = x + (self.in_rows_to_win)
        down = y + (self.in_rows_to_win)
        left = x - (self.in_rows_to_win-1)

        up_right = [up, right]
        down_right = [down, right]
        down_left = [down, left]
        up_left = [up, left]

        up = [up]
        right = [right]
        down = [down]
        left = [left]
        
        directions = [up, up_right, right, down_right, down, down_left, left, up_left]
        
        return directions

    def in_a_row_searcher(self, y, x, player):

        directions = self.direction_searcher_setup(y, x)

        for i_1 in range(0, len(directions)): #picks diraction
            
            for i_2 in range(0, len(directions[i_1])): #loops through y and x
                if(0 <= directions[i_1][i_2] <= self.arena_size):
                    within_arena = True
                else:
                    within_arena = False
                    break
            
            if(within_arena is True):
                in_row_counter = 0
                for i in range(0, self.in_rows_to_win):

                    y_step = self.y_step_generator(y, i_1, i) 
                    x_step = self.x_step_generator(x, i_1, i)
                    
                    if(self.arena[y_step][x_step] == self.symbols[player]):
                        in_row_counter += 1
                
                if(in_row_counter == self.in_rows_to_win):
                    return True
        
        return False


        
                    



match = Noughts_And_Crosses(3, 3)
match.create_arena()
match.nice_print()


while True:
    win = match.make_play(0)
    if win is True:
        print("Winner")
        break
'''
match.save_play(0, 0, 0)
match.save_play(0, 1, 0)
match.save_play(0, 2, 0)
match.nice_print()
'''
