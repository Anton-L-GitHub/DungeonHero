import tkinter as tk
from game_files import characters
from game_files import enemies
from game_files import treasures
import random


class Room:
    def __init__(self):
        self.state = '-'
        self.enemies = [enemies.Orc(), enemies.Giant_spider()]
        self.treasures = [treasures.Coin_pouch(), treasures.Coin_pouch(), treasures.Coin_pouch()]

    def get_state(self):
        return self.state

    def set_room_cleared(self):
        self.state = 'O'
        self.enemies = []
        self.treasures = []

    def set_state(self, new_state):
        self.state = new_state


class Game:
    def __init__(self):
        self.start_room = Room()    #TEMP
        self.start_room.state = 'P' #TEMP
        self.player = characters.Wizard()
        self.game_map = self.create_map()   #TEMP createmap
        self.game_map[0][0] = self.start_room   #temp
        self.game_map[0][3] = Room()    #temp
        self.current_pos = (0, 0) 

    def get_backpack_value(self):
        return sum([treasure.get_value() for treasure in self.player.backpack])

    def loot_treasures(self):
        x, y = self.current_pos
        room = self.game_map[x][y]
        for index, treasure in enumerate(room.treasures):
            self.player.backpack.append(treasure)

    def attack(self):
        x, y = self.current_pos
        room = self.game_map[x][y]
        for enemy in room.enemies:
            if random.randrange(1, 4) == 2:
                enemy.set_health(0)
                room.enemies.remove(enemy)
            if random.randrange(1, 10) == 2:
                self.player.health -= 1

    def make_move(self, direction):
        x, y = self.current_pos
        self.game_map[x][y].set_room_cleared()
        if direction == 'D' and y < 7:
            y += 1
        elif direction == 'R' and x < 7:
            x += 1
        elif direction == 'L' and x != 0:
            x -= 1
        elif direction == 'U' and y != 0:
            y -= 1
        self.current_pos = (x, y)
        self.game_map[x][y].set_state('P')

    def create_map(self):
        map_grid = list()
        for i in range(8):
            map_grid.append(list())
            for j in range(8):
                map_grid[i].append(Room())
        return map_grid


class Root(tk.Tk):
    def __init__(self, root, game):
        super().__init__(root)
        self.game = game
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.minsize(1200, 900)


class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="GREY")
        self.root = root
        self.build_app()
        self.update()
        
    def build_app(self):
        self.set_rowconfigure()
        self.set_columnconfigure()
        self.build_game_map_frame()
        self.build_player_frame()
        self.build_movement_frame(self.player_frame)
        self.grid(sticky="nswe")

    def movement(self, direction):
        self.root.game.make_move(direction)
        self.place_holder = self.game_map
        self.game_map = GuiGameMap(self.root, self.game_map_frame)
        self.place_holder.destroy()
        self.get_room_content()

    def get_room_content(self):
        x, y = self.root.game.current_pos
        room = self.root.game.game_map[x][y]
        if room.enemies or room.treasures:
            self.build_room_frame(room)
        
    def update(self):
        self.root.after(1000//30, self.update)
        self.player.update()
        try:
            self.room.update()
        except Exception:
            pass
        
    def set_rowconfigure(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def set_columnconfigure(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
    def build_game_map_frame(self):
        self.game_map_frame = tk.Frame(self, borderwidth=2, relief=tk.SUNKEN, bg="GREY")
        self.game_map_frame.grid(row=1, column=1, sticky="nswe")
        self.game_map_frame.rowconfigure(0, weight=1)
        self.game_map_frame.columnconfigure(0, weight=1)
        self.game_map = GuiGameMap(self.root, self.game_map_frame)

    def build_player_frame(self):
        self.player_frame = tk.Frame(self, borderwidth=2, relief=tk.SUNKEN)
        self.player_frame.grid(row=1, column=0, sticky="nwes")
        self.player_frame.rowconfigure(0, weight=0)
        self.player_frame.rowconfigure(1, weight=1)
        self.player_frame.columnconfigure(0, weight=1)
        self.player = GuiPlayer(self.root, self.player_frame)
    
    def build_movement_frame(self, container):
        self.movement_frame = tk.Frame(container, borderwidth=2, relief=tk.SUNKEN, bg="GREY")
        self.movement_frame.grid(row=1, column=0, sticky="nsew")
        self.movement_frame.rowconfigure(0, weight=1)
        self.movement_frame.rowconfigure(1, weight=1)
        self.movement_frame.rowconfigure(2, weight=1)
        self.movement_frame.columnconfigure(0, weight=1)
        self.movement_frame.columnconfigure(1, weight=1)
        self.movement_frame.columnconfigure(2, weight=1)
        #UP_BUTTON
        self.movement_up_button = tk.Button(self.movement_frame, text="UP",
            command=lambda:self.movement("U")
            )
        self.movement_up_button.grid(column=1, row=0, sticky="nsew")
        #DOWN_BUTTON
        self.movement_down_button = tk.Button(self.movement_frame, text="DOWN",
            command=lambda:self.movement("D")
            )
        self.movement_down_button.grid(column=1, row=2, sticky="nswe")
        #LEFT_BUTTON
        self.movement_left_button = tk.Button(self.movement_frame, text="LEFT",
            command=lambda:self.movement("L")
            )
        self.movement_left_button.grid(column=0, row=1, sticky="nswe")
        #RIGHT BUTTON
        self.movement_right_button = tk.Button(self.movement_frame, text="RIGHT",
            command=lambda:self.movement("R")
            )
        self.movement_right_button.grid(column=2, row=1, sticky="nswe")

    def build_room_frame(self, room):
        self.room_frame = tk.Frame(self, bg="#2c2c2c")
        self.room_frame.grid(row=1, column=0, columnspan=3, sticky="nswe")
        self.room_frame.rowconfigure(0, weight=1)
        self.room_frame.columnconfigure(0, weight=1)
        self.room = GuiRoom(self.root, self.room_frame, room)


class GuiGameMap(tk.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.room_scheme = {
            'O': tk.PhotoImage(file='data/images/open_door.png'),
            '-': tk.PhotoImage(file='data/images/closed_door.png'),
            'P': tk.PhotoImage(file=root.game.player.room_image)
        }
        self.game_map = root.game.game_map
        self.create_game_map()
        self.grid(sticky="nswe", row=0, column=0)

    def update(self):
        self.create_game_map()

    def create_game_map(self):
        for col_num, column in enumerate(self.game_map):
            self.columnconfigure(col_num, weight=1, minsize=75)
            for row_num, room in enumerate(column):
                self.rowconfigure(row_num, weight=1, minsize=75)
                label = tk.Label(self, image=self.room_scheme[room.get_state()], bg="GREY")
                label.grid(row=row_num, column=col_num, sticky="nswe")


class GuiPlayer(tk.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.root = root
        self.player = root.game.player
        self.player_image = tk.PhotoImage(file=self.player.image)
        self.backpack_image = tk.PhotoImage(file=self.player.backpack_image)
        self.create_player()
        self.grid(sticky="nwe")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def update(self):
        if self.player.get_health() > 0:
            self.player_health_label.config(text = f"Health: {self.player.health}")
        elif self.player.get_health() == 0:
            self.player_health_label.config(text = f"DEAD", bg="#ec1c24")
        self.player_attack_label.config(text = f"Attack: {self.player.attack}")
        self.player_agility_label.config(text = f"Agility: {self.player.agility}")
        self.player_initiative_label.config(text = f"Initiative: {self.player.initiative}")
        self.player_backback_value_label.config(text = f'Value: {self.root.game.get_backpack_value()}')

    def create_player(self):
        self.create_player_details_frames()

    def create_player_details_frames(self):
        #player_frame
        self.create_player_details_frames = tk.Frame(self)
        self.create_player_details_frames.grid(row=0, rowspan=2, sticky="new")
        self.create_player_details_frames.rowconfigure(0, weight=1)
        self.create_player_details_frames.rowconfigure(1, weight=1)
        self.create_player_details_frames.rowconfigure(2, weight=1)
        self.create_player_details_frames.rowconfigure(3, weight=1)
        self.create_player_details_frames.rowconfigure(4, weight=1)
        self.create_player_details_frames.rowconfigure(5, weight=1)
        self.create_player_details_frames.columnconfigure(0, weight=1)
        #player_portrait_frame
        self.player_portrait_frame = tk.Frame(self.create_player_details_frames)
        self.player_portrait_frame.grid(row=0, sticky="nwe")
        self.player_portrait_frame.rowconfigure(0, weight=1, minsize=150)
        self.player_portrait_frame.columnconfigure(0, weight=1)
        #player_image
        self.player_portrait_label = tk.Label(self.player_portrait_frame, image=self.player_image, bg="GREY")
        self.player_portrait_label.grid(sticky="wens")
        #player_health
        self.player_health_label = tk.Label(self.create_player_details_frames, text="PLAYER HEALTH", bg="#8bc53f")
        self.player_health_label.grid(row=1, sticky="new")
        #player_attack
        self.player_attack_label = tk.Label(self.create_player_details_frames, text="PLAYER ATTACK", bg="#f06422")
        self.player_attack_label.grid(row=2, sticky="new")
        #player_agility
        self.player_agility_label = tk.Label(self.create_player_details_frames, text="PLAYER AGILITY", bg="#01b696")
        self.player_agility_label.grid(row=3, sticky="new")
        #player_initiative
        self.player_initiative_label = tk.Label(self.create_player_details_frames, text="PLAYER INITIATIVE", bg="#0094d6")
        self.player_initiative_label.grid(row=4, sticky="new")
        #player_backpack_frame
        self.player_backpack_frame = tk.Frame(self.create_player_details_frames, relief=tk.RAISED, borderwidth=2)
        self.player_backpack_frame.grid(row=5, sticky="nwes")
        self.player_backpack_frame.rowconfigure(0, weight=1, minsize=150)
        self.player_backpack_frame.rowconfigure(1, weight=1)
        self.player_backpack_frame.rowconfigure(2, weight=1)
        self.player_backpack_frame.columnconfigure(0, weight=1)
        #player_backback
        self.player_backback_label = tk.Label(self.player_backpack_frame, image=self.backpack_image, bg="GREY")
        self.player_backback_label.grid(row=0, rowspan=3, column=0, sticky="wens")
        self.player_backback_value_label = tk.Label(self.player_backpack_frame, font=('Times', 14), bg="GREY")
        self.player_backback_value_label.grid(column=0, row=0, sticky="s")


class GuiRoom(tk.Frame):
    def __init__(self, root, parent, room):
        super().__init__(parent, bg="GREY")
        self.root = root
        self.parent = parent
        self.room_obj = room
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.create_room()
        self.grid(sticky="nwes")

    def room_kill(self):
        self.root.game.loot_treasures()
        self.parent.destroy()

    def update(self):
        for entity_frame in self.all_entity_frames:
            entity_frame.update()
        if self.combat.is_combat_won():
            self.create_room_won_frames()
            del self.combat
        elif self.combat.is_combat_lost():
            self.create_room_lost_frames()
            del self.combat
        
    def create_room(self):
        self.all_entity_frames = list()
        self.create_enemy_frames()
        self.create_player_frames()
        self.create_combat_frames()

    def create_combat_frames(self):
        self.combat_status_label = tk.Label(self, text=f"Combat: {self.root.game.player.get_name()}'s turn!", font=("Times", 16, 'bold'), bg="DARKRED")
        self.combat_status_label.grid(row=1, columnspan=5, sticky="nswe")
        self.combat_container = tk.Frame(self, bg="#2c2c2c")
        self.combat_container.grid(row=2, column=1, rowspan=2, columnspan=4, sticky="nswe")
        self.combat_container.rowconfigure(0, weight=1, minsize=50)
        self.combat_container.columnconfigure(0, weight=1)
        self.combat = GuiCombat(self.root, self.combat_container, self.room_obj.enemies)

    def create_player_frames(self):
        self.player_container = tk.Frame(self, bg='GREY')
        self.player_container.grid(row=3, column=0, sticky="sw")
        self.player_container.rowconfigure(0, weight=1)
        self.player_container.columnconfigure(0, weight=1)
        self.all_entity_frames.append(GuiEntity(self.player_container, self.root.game.player, 0))

    def create_enemy_frames(self):
        self.enemy_container = tk.Frame(self, bg='GREY')
        self.enemy_container.grid(row=0, column=3, sticky="en")
        self.enemy_container.rowconfigure(0, weight=1)
        self.enemy_container.columnconfigure(0, weight=1)
        for entity_num, enemy in enumerate(self.room_obj.enemies):
            self.all_entity_frames.append(GuiEntity(self.enemy_container, enemy, entity_num))

    def create_room_lost_frames(self):
        self.lose_container = tk.Frame(self, bg='#2c2c2c', relief=tk.RAISED, borderwidth=5)
        self.lose_container.grid(row=1, rowspan=3, column=0, columnspan=5, sticky="nswe")
        self.lose_container.rowconfigure(0, weight=0)
        self.lose_container.rowconfigure(1, weight=0)
        self.lose_container.columnconfigure(0, weight=1)
        self.lose_container.columnconfigure(1, weight=1)
        self.lose_container.columnconfigure(2, weight=1)
        #lose label
        self.lose_label = tk.Label(self.lose_container, text="GAME OVER!", font=("Times", 20, 'bold'), relief=tk.RAISED, borderwidth=2)
        self.lose_label.grid(row=0, column=0, columnspan=3,  sticky="nwe")
        #Exit_to_menu
        self.exit_room_button = tk.Button(self.lose_container, text="Exit: Main Menu", font=('Arial', 13, 'bold'), command=lambda:self.room_kill())
        self.exit_room_button.grid(column=1, row=2, sticky="nswe")
        #Exit_button
        self.exit_room_button = tk.Button(self.lose_container, text="Exit: Game", font=('Arial', 13, 'bold'), command=lambda:exit())
        self.exit_room_button.grid(column=1, row=3, sticky="nswe")

    def create_room_won_frames(self):
        self.all_treasure_images = list()
        self.victory_container = tk.Frame(self, bg='#2c2c2c', relief=tk.RAISED, borderwidth=5)
        self.victory_container.grid(row=1, rowspan=3, column=0, columnspan=5, sticky="nswe")
        self.victory_container.rowconfigure(0, weight=0)
        self.victory_container.rowconfigure(1, weight=0)
        self.victory_container.columnconfigure(0, weight=1)
        self.victory_container.columnconfigure(1, weight=1)
        self.victory_container.columnconfigure(2, weight=1)
        #victory label
        self.victory_label = tk.Label(self.victory_container, text="Room Cleared", font=("Times", 20, 'bold'), relief=tk.RAISED, borderwidth=2)
        self.victory_label.grid(row=0, column=0, columnspan=3,  sticky="nwe")
        #treasures
        self.victory_treasure_frame = tk.Frame(self.victory_container, bg="#2c2c2c")
        self.victory_treasure_frame.grid(row=1, column=1, sticky="nwe")
        self.victory_treasure_frame.rowconfigure(0, weight=1)
        self.victory_treasure_frame.columnconfigure(0, weight=1)
        self.victory_treasure_frame.columnconfigure(1, weight=1)
        self.victory_treasure_frame.columnconfigure(2, weight=0)
        self.victory_treasure_frame.columnconfigure(3, weight=1)
        self.treasure_label = tk.Label(self.victory_treasure_frame, text="Treasures Found:", font=("Times", 15), bg="#01b696", relief=tk.RAISED, borderwidth=2)
        self.treasure_label.grid(row=0, columnspan=4, sticky='nwe')
        self.treasure_sum = 0
        for row_num, treasure in enumerate(self.room_obj.treasures):
            self.treasure_sum += treasure.get_value()
            #filler_num
            num_item_label = tk.Label(
                self.victory_treasure_frame,
                relief=tk.RAISED,
                borderwidth=2,
                text=row_num+1,
                bg="#01b696"
            )
            num_item_label.grid(row=row_num+1, column=0, sticky="nswe")
            #name
            treasure_name_label = tk.Label(
                self.victory_treasure_frame,
                relief=tk.RAISED,
                borderwidth=2,
                text=treasure.get_name(),
                bg="#01b696"
                )
            treasure_name_label.grid(row=row_num+1, column=1, sticky="nswe")
            #image
            self.all_treasure_images.append(tk.PhotoImage(file=treasure.get_image()))
            treasure_image = tk.Label(
                self.victory_treasure_frame,
                image=self.all_treasure_images[row_num],
                relief=tk.RAISED,
                borderwidth=2
                )
            treasure_image.grid(row=row_num+1, column=2, sticky="nswe")
            #value
            treasure_value_label = tk.Label(
                self.victory_treasure_frame,
                relief=tk.RAISED,
                borderwidth=2,
                text=f'Value: {treasure.get_value()}',
                bg="#01b696"
                )
            treasure_value_label.grid(row=row_num+1, column=3, sticky="nswe")
        self.treasure_sum_label = tk.Label(
            self.victory_treasure_frame,
            relief=tk.RAISED,
            borderwidth=2,
            text=f'Total value: {self.treasure_sum}',
            bg="#01b696",
            font=("Times", 15)
            )
        self.treasure_sum_label.grid(row=len(self.room_obj.treasures)+1, column=0, columnspan=4, sticky="nswe")
        #Exit_button
        self.exit_room_button = tk.Button(self.victory_container, text="Loot Treasures & Continue", font=('Arial', 13, 'bold'), command=lambda:self.room_kill())
        self.exit_room_button.grid(column=1, row=2, sticky="nswe")


class GuiEntity(tk.Frame):
    def __init__(self, parent, entity, entity_num):
        super().__init__(parent, borderwidth=2, relief=tk.RAISED, bg="GREY")
        self.entity = entity
        self.image = tk.PhotoImage(file=self.entity.get_image())
        self.build_entity_frame()
        self.grid(column=entity_num, row=0, padx=15)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def update(self):
        if self.entity.get_health() >= 1:
            self.entity_health.config(text= f"Health: {self.entity.get_health()}")
            self.entity_attack.config(text= f"Attack: {self.entity.get_attack()}")
            self.entity_agility.config(text= f"Agility: {self.entity.get_agility()}")
            self.entity_initiative.config(text= f"Initiative: {self.entity.get_initiative()}")
        else:
            self.entity_health.config(bg="#ec1c24", text="DEAD")

    def build_entity_frame(self):
        color = "GREY"
        #image
        self.entity_image = tk.Label(self, image=self.image, bg=color)
        self.entity_image.grid(row=0, sticky="snwe")
        #name
        self.entity_name = tk.Label(self, text=self.entity.get_name(), bg=color, font=('Times', 12, 'bold'))
        self.entity_name.grid(sticky="snwe")
        #health
        self.entity_health = tk.Label(self, text=f'Health: {self.entity.get_health()}', bg='#8bc53f')
        self.entity_health.grid(sticky="snwe")
        #attack
        self.entity_attack = tk.Label(self, text=f'Attack: {self.entity.get_attack()}', bg='#f06422')
        self.entity_attack.grid(sticky="snwe")
        #agility
        self.entity_agility = tk.Label(self, text=f'Agility: {self.entity.get_agility()}', bg='#01b696')
        self.entity_agility.grid(sticky="snwe")
        #initiative
        self.entity_initiative = tk.Label(self, text=f'Initiative: {self.entity.get_initiative()}', bg='#0094d6')
        self.entity_initiative.grid(sticky="snwe")


class GuiCombat(tk.Frame):
    def __init__(self, root, parent, enemies):
        super().__init__(parent, bg="GREY")
        self.root = root
        self.parent = parent
        self.enemies = enemies
        self.create_combat()
        self.grid(sticky="nswe")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, weight=1)

    def is_combat_won(self):
        total = sum([enemy.get_health() for enemy in self.enemies])
        if total == 0:
            return True

    def is_combat_lost(self):
        if self.root.game.player.health <= 0:
            return True

    def update(self):
        pass

    def create_combat(self):
        self.create_player_combat_options()
        self.create_combat_text()
        self.update()

    def create_combat_text(self):
        self.combat_text_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.combat_text_frame.grid(row=2, column=0, columnspan=3, sticky="nswe")
        self.combat_text_frame.rowconfigure(0, weight=0)
        self.combat_text_frame.rowconfigure(1, weight=1)
        self.combat_text_frame.columnconfigure(0, weight=1)
        self.combat_text_label = tk.Label(self.combat_text_frame, text="Terminal", bg="BLACK", fg="WHITE")
        self.combat_text_label.grid(row=0, sticky="nwe")
        self.combat_text_field = tk.Text(self.combat_text_frame, bg="BLACK")
        self.combat_text_field.grid(row=1, sticky="nswe")

    def create_player_combat_options(self):
        self.combat_menu_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.combat_menu_frame.grid(row=1, column=0, sticky="nwe")
        self.combat_menu_frame.rowconfigure(0, weight=1)
        self.combat_menu_frame.rowconfigure(1, weight=1)
        self.combat_menu_frame.rowconfigure(2, weight=1)
        self.combat_menu_frame.columnconfigure(0, weight=1)
        #Menu_label
        self.combat_menu_label = tk.Label(self.combat_menu_frame, text="Combat Menu")
        self.combat_menu_label.grid(row=0, column=0, columnspan=2, sticky="wne")
        #Attack_button
        self.combat_attack_button = tk.Button(self.combat_menu_frame, text="Attack",
            command=lambda:self.root.game.attack()
            )
        self.combat_attack_button.grid(row=1, column=0, sticky="nwe")     
        #Flee_button
        self.combat_flee_button = tk.Button(self.combat_menu_frame, text="Flee")
        self.combat_flee_button.grid(row=2, column=0, sticky="nwe")
        #Exit_room_button
        self.combat_exit_room_button = tk.Button(self.combat_menu_frame, text="Leave",
            command=lambda:print("exit?")
            )
        self.combat_exit_room_button.grid(row=3, column=0, sticky="nwe")

    


        
