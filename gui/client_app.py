import tkinter as tk
from tkinter import messagebox
from game_files import gamemap
from game_files import characters
from game_files import enemies
from game_files import treasures
from game_files import demo_combat
from tkinter import messagebox
from data.database import database
import random
import time
import winsound
import os
import sys

path = os.path.abspath(os.getcwd())
path += '/data/music/the_cave.wav'
winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)


class Game:
    def __init__(self):
        self.player = None
        self.game_map = None
        self.current_turn = None

    def get_backpack_value(self):
        return sum([treasure.get_value() for treasure in self.player.backpack])

    def loot_treasures(self, room):
        content = room.get_contents()
        for treasure in content['treasures']:
            self.player.backpack.append(treasure)


class Root(tk.Tk):
    def __init__(self, root, game):
        super().__init__(root)
        self.game = game
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.minsize(1280, 720)
        self.maxsize(1280, 720)
        self.color_mapping = {
            'flavour_text_color': '#fff757',
            'combat_yellow': '#ffdc00',
            'combat_red': '#ec1c24',
            'dead': '#ec1c24',
            'attack': '#f06422',
            'victory_grey': '#2c2c2c',
            'agility': '#01b696',
            'initiative': '#0094db',
            'health': '#8bc53f',
            'treasure_green': '#8bc53f'
        }
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        self.geometry("+%d+%d" % (0+(width/2)-640, (0+height/2)-360))

class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="GREY")
        self.root = root
        self.build_start_screen()
        self.update()
        self.set_rowconfigure()
        self.set_columnconfigure()
        self.grid(sticky="nswe")

    def switch_frame(self, to_show, to_destroy):
        to_show()
        to_destroy.destroy()
        
    def exit_popup(self):
        self.exit_popup_image = tk.PhotoImage(file='data/images/exit_popup.png')
        win = tk.Toplevel(bg="GREY")
        win.wm_title("EXIT?")
        win.grid()
        win.grab_set()
        win.columnconfigure(0, weight=1)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        heigth = self.root.winfo_height()
        win.geometry("+%d+%d" % (x+(width/2)-200, (y+(heigth/2)-75)))
        #exit
        exit_label = tk.Label(win, image=self.exit_popup_image, bg="GREY", font=(16))
        exit_label.grid(row=0, column=0, columnspan=2)
        #quit
        quit_button = tk.Button(win, text="Yes",  bg="GREY", font=("Times", 14, 'bold'), command=lambda:sys.exit())
        quit_button.grid(row=1, column=0, sticky="we")
        #return
        return_button = tk.Button(win, text="No", bg="GREY", font=("Times", 14, 'bold'), command=lambda:win.destroy())
        return_button.grid(row=1, column=1, sticky="we")
    
    def end_won_game(self, to_show):
        self.app_frame.destroy()
        del self.root.game
        self.root.game = None
        to_show()

    def create_game_won_frames(self):
        self.game_won_image = tk.PhotoImage(file='data/images/game_won.png')
        self.win_container = tk.Frame(self.app_frame, bg=self.root.color_mapping['victory_grey'], relief=tk.RAISED, borderwidth=5)
        self.win_container.grid(row=0, rowspan=4, column=0, columnspan=5, sticky="nswe")
        self.win_container.rowconfigure(0, weight=0)
        self.win_container.rowconfigure(1, weight=0)
        self.win_container.columnconfigure(0, weight=1)
        self.win_container.columnconfigure(1, weight=1)
        self.win_container.columnconfigure(2, weight=1)
        #win label
        self.win_label = tk.Label(self.win_container, image=self.game_won_image, text="GAME WON!", font=("Times", 20, 'bold'), relief=tk.RAISED, borderwidth=2)
        self.win_label.grid(row=0, column=0, columnspan=3)
        #Exit_to_menu
        self.exit_room_button = tk.Button(self.win_container, text="Main Menu", font=('Arial', 13, 'bold'), command=lambda:self.end_won_game(self.build_start_menu))
        self.exit_room_button.grid(column=1, row=2, sticky="nswe")
        #Exit_button
        #self.exit_room_button = tk.Button(self.win_container, text="Exit Game", font=('Arial', 13, 'bold'), command=lambda:self.switch_frame(None, self.root))
        #self.exit_room_button.grid(column=1, row=3, sticky="nswe")

    def save_game_progress(self, return_to, to_destroy):
        database.disc_save_progress(self.root.game.player, self.root.game.game_map)
        del self.root.game
        self.root.game = None
        self.switch_frame(return_to, self.app_frame)
        to_destroy.destroy()

    def save_game_character(self, return_to, to_destroy):
        json_path = f'data/database/characters_ongoing/character_{self.root.game.player.name}.json'
        if os.path.exists(json_path):
            os.remove(json_path)
        database.disc_save_character(self.root.game.player)
        del self.root.game
        self.root.game = None
        self.switch_frame(return_to, to_destroy)
        to_destroy.destroy()

    def delete_game_progress(self, return_to, to_destroy):
        json_path = f'data/database/characters_ongoing/character_{self.root.game.player.name}.json'
        json_path_character = f'data/database/characters/character_{self.root.game.player.name}.json'
        if os.path.exists(json_path):
            os.remove(json_path)
        if os.path.exists(json_path_character):
            os.remove(json_path_character)
        del self.root.game
        self.root.game = None
        if return_to:
            self.switch_frame(return_to, self.app_frame)
        try:
            to_destroy.destroy()
        except:
            to_destroy()

    def finish_dungeon_popup(self):
        self.finish_dungeon_popup_image = tk.PhotoImage(file='data/images/exit_dungeon.png')
        win = tk.Toplevel(bg="GREY")
        win.wm_title("EXIT DUNGEON?")
        win.grid()
        win.grab_set()
        win.columnconfigure(0, weight=1)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        heigth = self.root.winfo_height()
        win.geometry("+%d+%d" % (x+(width/2)-200, (y+(heigth/2)-75)))
        #exit
        exit_label = tk.Label(win, image=self.finish_dungeon_popup_image, bg="GREY", font=(16))
        exit_label.grid(row=0, column=0, columnspan=2)
        #quit
        quit_button = tk.Button(win, text="Yes",  bg="GREY", font=("Times", 14, 'bold'),
            command=lambda:self.save_game_character(self.create_game_won_frames, win)
        )
        quit_button.grid(row=1, column=0, sticky="we")
        #return
        return_button = tk.Button(win, text="No", bg="GREY", font=("Times", 14, 'bold'), command=lambda:win.destroy())
        return_button.grid(row=1, column=1, sticky="we")

    def exit_dungeon_popup(self):
        self.exit_dungeon_popup_image = tk.PhotoImage(file='data/images/exit_dungeon.png')
        win = tk.Toplevel(bg="GREY")
        win.wm_title("EXIT DUNGEON?")
        win.grid()
        win.grab_set()
        win.columnconfigure(0, weight=1)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        heigth = self.root.winfo_height()
        win.geometry("+%d+%d" % (x+(width/2)-200, (y+(heigth/2)-75)))
        #exit
        exit_label = tk.Label(win, image=self.exit_dungeon_popup_image, bg="GREY", font=(16))
        exit_label.grid(row=0, column=0, columnspan=2)
        #quit
        quit_button = tk.Button(win, text="Yes",  bg="GREY", font=("Times", 14, 'bold'),
            command=lambda:self.save_game_progress(self.build_start_menu, win)
        )
        quit_button.grid(row=1, column=0, sticky="we")
        #return
        return_button = tk.Button(win, text="No", bg="GREY", font=("Times", 14, 'bold'), command=lambda:win.destroy())
        return_button.grid(row=1, column=1, sticky="we")
    
    def set_start_position(self, direction):
        self.start_corner_frame.destroy()
        self.after(350, self.temp_move_label.destroy)
        self.root.game.game_map.set_start_position(direction)
        room = self.root.game.game_map.get_room_at_grid()
        self.place_holder = self.game_map
        self.game_map = GuiGameMap(self.root, self.game_map_frame)
        self.place_holder.destroy()
        
    def enter_room(self, room, frame_to_destroy):
        frame_to_destroy.destroy()
        self.build_room_frame(room)

    def update(self):
        self.root.after(1000//30, self.update)
        try:
            self.player.update()
        except Exception:
            pass
        try:
            self.room.update()
        except Exception:
            pass
        
    def build_temp_lbl(self, container):
        self.temp_move_label = tk.Frame(container, bg="GREY")
        self.temp_move_label.grid(row=1, column=0, columnspan=2, sticky="nswe")

    def build_app(self):
        self.root.game.game_map.create_map()
        self.app_frame = tk.Frame(self)
        self.build_game_map_frame(self.app_frame)
        self.build_player_frame(self.app_frame)
        self.build_movement_frame(self.player_frame)
        self.build_save_exit_frame(self.player_frame)
        self.build_temp_lbl(self.player_frame)
        self.build_start_corner_frame(self.player_frame)
        self.app_frame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        self.app_frame.rowconfigure(0, weight=1)
        self.app_frame.columnconfigure(0, weight=1)
        self.app_frame.columnconfigure(1, weight=1)
        self.app_frame.lower()

    def build_start_menu(self):
        self.banner_image = tk.PhotoImage(file='data/images/banner.png')
        self.new_game_image = tk.PhotoImage(file='data/images/new_game.png')
        self.load_game_image = tk.PhotoImage(file='data/images/load_game.png')
        self.exit_game_image = tk.PhotoImage(file='data/images/exit.png')
        self.menu_screen_frame = tk.Frame(self, bg="GREY")
        self.menu_screen_frame.grid(row=0, columnspan=2, sticky="snew")
        self.menu_screen_frame.columnconfigure(0, weight=1)
        self.menu_screen_frame.rowconfigure(0, weight=1)
        self.menu_screen_frame.rowconfigure(1, weight=0)
        self.menu_screen_frame.rowconfigure(2, weight=0)
        self.menu_screen_frame.rowconfigure(3, weight=0)
        self.menu_screen_frame.rowconfigure(4, weight=1)
        self.menu_screen_frame.rowconfigure(5, weight=1)
        self.menu_screen_frame.columnconfigure(0, weight=1)
        self.menu_screen_frame.columnconfigure(1, weight=1)
        self.menu_screen_frame.columnconfigure(2, weight=1)
        #BANNER
        self.banner_label = tk.Label(self.menu_screen_frame, image=self.banner_image, bg="GREY")
        self.banner_label.grid(row=0, columnspan=3)
        #NEW GAME
        self.new_game_button = tk.Button(self.menu_screen_frame, image=self.new_game_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_new_game_menu, self.menu_screen_frame)
        )
        self.new_game_button.grid(row=1, column=1, pady=10)
        #LOAD GAME
        self.load_game_button = tk.Button(self.menu_screen_frame, image=self.load_game_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_load_game_menu, self.menu_screen_frame)
        )
        self.load_game_button.grid(row=2, column=1, pady=10)
        #EXIT GAME
        self.exit_game_button = tk.Button(self.menu_screen_frame, image=self.exit_game_image, bg="GREY",
            command=lambda:self.exit_popup()
        )
        self.exit_game_button.grid(row=3, column=1, pady=10)

    def build_new_game_menu(self):
        self.banner_image = tk.PhotoImage(file='data/images/banner.png')
        self.new_character_image = tk.PhotoImage(file='data/images/new_character.png')
        self.load_character_image = tk.PhotoImage(file='data/images/load_character.png')
        self.back_image = tk.PhotoImage(file='data/images/back.png')

        self.new_game_frame = tk.Frame(self, bg="GREY")
        self.new_game_frame.grid(row=0, columnspan=2, sticky="snew")
        self.new_game_frame.columnconfigure(0, weight=1)
        self.new_game_frame.rowconfigure(0, weight=1)
        self.new_game_frame.rowconfigure(1, weight=0)
        self.new_game_frame.rowconfigure(2, weight=0)
        self.new_game_frame.rowconfigure(3, weight=0)
        self.new_game_frame.rowconfigure(4, weight=1)
        self.new_game_frame.rowconfigure(5, weight=1)
        self.new_game_frame.columnconfigure(0, weight=1)
        self.new_game_frame.columnconfigure(1, weight=1)
        self.new_game_frame.columnconfigure(2, weight=1)
        #BANNER
        banner_label = tk.Label(self.new_game_frame, image=self.banner_image, bg="GREY")
        banner_label.grid(row=0, columnspan=3)
        #NEW CHARACTER
        new_character_button = tk.Button(self.new_game_frame, image=self.new_character_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_new_character_menu, self.new_game_frame)
        )
        new_character_button.grid(row=1, column=1, pady=10)
        #LOAD CHARACTER
        load_character_button = tk.Button(self.new_game_frame, image=self.load_character_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_load_character_menu, self.new_game_frame)
        )
        load_character_button.grid(row=2, column=1, pady=10)
        #BACK OPTION
        back_button = tk.Button(self.new_game_frame, image=self.back_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_start_menu, self.new_game_frame)
        )
        back_button.grid(row=3, column=1, pady=10)

    def handle_load_character_input(self, player_name, map_size):
        json_path = f'data/database/characters_ongoing/'
        existing_names = []
        for file in os.listdir(json_path):
            file = file.replace('character_', '')
            file = file.replace('.json', '')
            existing_names.append(file)
        if player_name in existing_names:
            messagebox.showwarning("Error", "Name already taken")
            print("Name already taken")
        if player_name == "":
            messagebox.showwarning("Error", "Name cannot be empty")
            print("Name cannot be empty")
        if map_size == '0':
            messagebox.showwarning("Error", "No map size selected")
            print("Map cannot be empty")
        if player_name != "" and player_name not in existing_names and map_size != '0':
            self.input_frame.destroy()
            
            try:
                self.load_character_frame.destroy()
            except:
                pass
            try:
                self.new_character_frame.destroy()
            except:
                pass
            finally:
                map_sizes = {
                    'small': (4, 4),
                    'medium': (6, 6),
                    'large': (8, 8)
                }
                x, y = map_sizes[map_size]
                self.root.game.game_map = gamemap.GameMap(x, y)
                self.root.game.player.name = player_name
                self.build_app()

    def handle_new_game_input(self, player_name, map_size):
        json_path1 = f'data/database/characters_ongoing/'
        json_path2 = f'data/database/characters/'
        existing_names = []
        for file in os.listdir(json_path1):
            file = file.replace('character_', '')
            file = file.replace('.json', '')
            existing_names.append(file)
        for file in os.listdir(json_path2):
            file = file.replace('character_', '')
            file = file.replace('.json', '')
            existing_names.append(file)
        if player_name in existing_names:
            messagebox.showwarning("Error", "Name already taken")
            print("Name already taken")
        if player_name == "":
            messagebox.showwarning("Error", "Name cannot be empty")
            print("Name cannot be empty")
        if map_size == '0':
            messagebox.showwarning("Error", "No map size selected")
            print("Map cannot be empty")
        if player_name != "" and player_name not in existing_names and map_size != '0':
            self.input_frame.destroy()
            
            try:
                self.load_character_frame.destroy()
            except:
                pass
            try:
                self.new_character_frame.destroy()
            except:
                pass
            finally:
                map_sizes = {
                    'small': (4, 4),
                    'medium': (6, 6),
                    'large': (8, 8)
                }
                x, y = map_sizes[map_size]
                self.root.game.game_map = gamemap.GameMap(x, y)
                self.root.game.player.name = player_name
                self.build_app()

    def build_input_new_game(self):
        self.input_player_image = tk.PhotoImage(file=self.root.game.player.get_image())
        self.start_image = tk.PhotoImage(file='data/images/start_game.png')
        self.small_map = tk.PhotoImage(file='data/images/game_4x4.png')
        self.medium_map = tk.PhotoImage(file="data/images/game_6x6.png")
        self.large_map = tk.PhotoImage(file="data/images/game_8x8.png")
        self.input_frame = tk.Toplevel(self.root, bg="GREY")
        self.input_frame.grid()
        self.input_frame.columnconfigure(0, weight=10)
        self.input_frame.columnconfigure(1, weight=0)
        self.input_frame.columnconfigure(2, weight=0)
        self.input_frame.columnconfigure(3, weight=0)
        self.input_frame.columnconfigure(4, weight=10)
        self.input_frame.rowconfigure(0, weight=0)
        self.input_frame.rowconfigure(1, weight=0)
        self.input_frame.rowconfigure(2, weight=0)
        self.input_frame.rowconfigure(3, weight=0)
        self.input_frame.grab_set()
        self.input_frame.minsize(700, 600)
        self.input_frame.maxsize(700, 600)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        heigth = self.root.winfo_height()
        self.input_frame.geometry("+%d+%d" % (x+(width/2)-350, (y+(heigth/2)-285)))

        hero_label = tk.Label(self.input_frame, image=self.input_player_image)
        hero_label.grid(column=2, row=0, pady=15)
        if not self.root.game.player.name:
            hero_name_label = tk.Label(self.input_frame, text="Enter name:", bg="GREY", font=("times", 16, "bold"))
            hero_name_label.grid(column=1, row=1, sticky="nwe", pady=15, padx=2)
            hero_name = tk.Entry(self.input_frame, font=("times", 15))
            hero_name.grid(column=2, row=1, sticky="nsew", pady=15, ipady=2, ipadx=10, padx=2)
        else:
            hero_name_label = tk.Label(self.input_frame, text=self.root.game.player.name, bg="GREY", font=("times", 16, "bold"))
            hero_name_label.grid(column=2, row=1, sticky="nwe", pady=15, padx=2)
            hero_name = tk.StringVar(value=self.root.game.player.name)

        map_size = tk.StringVar(value="small")
        map_small = tk.Checkbutton(self.input_frame, image=self.small_map, variable=map_size, onvalue='small', bg="GREY")
        map_small.grid(column=1, row=2, sticky="n", pady=10, padx=5)
        map_medium = tk.Checkbutton(self.input_frame, image=self.medium_map, variable=map_size, onvalue='medium', bg="GREY")
        map_medium.grid(column=2, row=2, sticky="n", pady=10, padx=5)
        map_large = tk.Checkbutton(self.input_frame, image=self.large_map, variable=map_size, onvalue='large', bg="GREY")
        map_large.grid(column=3, row=2, sticky="n", pady=10, padx=5)

        if not self.root.game.player.name:
            hero_submit = tk.Button(self.input_frame, text="Submit and continue", image=self.start_image, bg="grey",
                command=lambda:self.handle_new_game_input(hero_name.get(), map_size.get())
            )
            hero_submit.grid(column=3, row=1)
        else:
            hero_submit = tk.Button(self.input_frame, text="Submit and continue", image=self.start_image, bg="grey",
                command=lambda:self.handle_load_character_input(hero_name.get(), map_size.get())
            )
            hero_submit.grid(column=3, row=1)

    def handle_load_character(self, player_name):
        new_player = database.disc_load_character(player_name)
        self.root.game = Game()
        self.root.game.player = new_player
        self.build_input_new_game()

    def build_load_character_menu(self):
        self.banner_image = tk.PhotoImage(file='data/images/banner.png')
        self.load_character_image = tk.PhotoImage(file='data/images/load_character.png')
        self.back_image = tk.PhotoImage(file='data/images/back.png')

        self.load_character_frame = tk.Frame(self, bg="GREY")
        self.load_character_frame.grid(row=0, columnspan=2, sticky="snew")
        self.load_character_frame.columnconfigure(0, weight=1)
        self.load_character_frame.rowconfigure(0, weight=1)
        self.load_character_frame.rowconfigure(1, weight=0)
        self.load_character_frame.rowconfigure(2, weight=0, minsize=125)
        self.load_character_frame.rowconfigure(3, weight=0)
        self.load_character_frame.rowconfigure(4, weight=1)
        self.load_character_frame.rowconfigure(5, weight=1)
        self.load_character_frame.columnconfigure(0, weight=1)
        self.load_character_frame.columnconfigure(1, weight=1)
        self.load_character_frame.columnconfigure(2, weight=1)
        self.load_character_frame.columnconfigure(3, weight=1)
        self.load_character_frame.columnconfigure(4, weight=1)
        #BANNER
        banner_label = tk.Label(self.load_character_frame, image=self.banner_image, bg="GREY")
        banner_label.grid(row=0, columnspan=5)
        #LOAD CHARACTER
        load_character_button = tk.Button(self.load_character_frame, image=self.load_character_image, bg="GREY",
            command=lambda:self.handle_load_character(self.checked_file.get())
        )
        load_character_button.grid(row=1, column=0, pady=10)
        #BACK OPTION
        back_button = tk.Button(self.load_character_frame, image=self.back_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_new_game_menu, self.load_character_frame)
        )
        back_button.grid(row=3, column=0, pady=10)
        #FILE FRAME
        self.save_files_frame = tk.Frame(self.load_character_frame, bg="BLACK")
        self.save_files_frame.grid(row=1, rowspan=3, column=1, columnspan=3, sticky="wnes")
        self.save_files_frame.columnconfigure(0, weight=1)
        self.save_files_frame.columnconfigure(1, weight=0)
        save_files_label = tk.Label(self.save_files_frame, text="Saved Characters", font=("times", 22), fg="white", bg="black")
        save_files_label.grid(row=0, columnspan=2, sticky="we")
        self.checked_file = tk.StringVar(value=0)

        for row, filename in enumerate(os.listdir('data/database/characters/')):
            char_name = filename.replace('character_', '')
            char_name = char_name.replace('.json', '')
            temp_frame = tk.Frame(self.save_files_frame, relief=tk.RAISED, borderwidth=2)
            temp_frame.grid(row=row+1, columnspan=2, sticky="we")
            temp_frame.columnconfigure(0, minsize=210)
            file_checkbutton = tk.Checkbutton(temp_frame, variable=self.checked_file, onvalue=char_name, offvalue=None)
            file_checkbutton.grid(row=row, column=0, sticky="e")
            file_label = tk.Label(temp_frame, text=char_name, font=(18))
            file_label.grid(row=row, column=1, sticky="we")

    def handle_load_game(self, player_name):
        new_gamemap, player = database.disc_load_progress(player_name)
        x = new_gamemap.player_x
        y = new_gamemap.player_y
        new_gamemap.map_grid[y][x].set_state('X')
        self.root.game = Game()
        self.root.game.player = player
        self.root.game.game_map = new_gamemap
        self.app_frame = tk.Frame(self)
        self.build_game_map_frame(self.app_frame)
        self.build_player_frame(self.app_frame)
        self.build_movement_frame(self.player_frame)
        self.build_save_exit_frame(self.player_frame)
        self.app_frame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        self.app_frame.rowconfigure(0, weight=1)
        self.app_frame.columnconfigure(0, weight=1)
        self.app_frame.columnconfigure(1, weight=1)
        self.app_frame.lower()

    def build_load_game_menu(self):
        self.banner_image = tk.PhotoImage(file='data/images/banner.png')
        self.load_game_image = tk.PhotoImage(file='data/images/load_game.png')
        self.back_button_image = tk.PhotoImage(file='data/images/back.png')
        self.load_game_frame = tk.Frame(self, bg="GREY")
        self.load_game_frame.grid(row=0, columnspan=2, sticky="snew")
        self.load_game_frame.columnconfigure(0, weight=1)
        self.load_game_frame.rowconfigure(0, weight=1)
        self.load_game_frame.rowconfigure(1, weight=0)
        self.load_game_frame.rowconfigure(2, weight=0, minsize=125)
        self.load_game_frame.rowconfigure(3, weight=0)
        self.load_game_frame.rowconfigure(4, weight=1)
        self.load_game_frame.rowconfigure(5, weight=1)
        self.load_game_frame.columnconfigure(0, weight=1)
        self.load_game_frame.columnconfigure(1, weight=1)
        self.load_game_frame.columnconfigure(2, weight=1)
        self.load_game_frame.columnconfigure(3, weight=1)
        self.load_game_frame.columnconfigure(4, weight=1)
        #BANNER
        self.banner_label = tk.Label(self.load_game_frame, image=self.banner_image, bg="GREY")
        self.banner_label.grid(row=0, columnspan=5)
        #LOAD GAME
        self.load_game_button = tk.Button(self.load_game_frame, image=self.load_game_image, bg="GREY",
            command=lambda:self.switch_frame(lambda:self.handle_load_game(self.checked_file.get()), self.load_game_frame)
        )
        self.load_game_button.grid(row=1, column=0, pady=10)
        #BACK OPTION
        back_button = tk.Button(self.load_game_frame, image=self.back_button_image, bg="GREY",
            command=lambda:self.switch_frame(self.build_start_menu, self.load_game_frame)
        )
        back_button.grid(row=3, column=0, pady=10)
        #FILE FRAME
        self.save_files_frame = tk.Frame(self.load_game_frame, bg="BLACK")
        self.save_files_frame.grid(row=1, rowspan=3, column=1, columnspan=3, sticky="wnes")
        self.save_files_frame.columnconfigure(0, weight=1)
        self.save_files_frame.columnconfigure(1, weight=0)
        save_files_label = tk.Label(self.save_files_frame, text="Saved Games", font=("times", 22), fg="white", bg="black")
        save_files_label.grid(row=0, columnspan=2, sticky="we")
        self.checked_file = tk.StringVar(value=0)

        for row, filename in enumerate(os.listdir('data/database/characters_ongoing/')):
            char_name = filename.replace('character_', '')
            char_name = char_name.replace('.json', '')
            temp_frame = tk.Frame(self.save_files_frame, relief=tk.RAISED, borderwidth=2)
            temp_frame.grid(row=row+1, columnspan=2, sticky="we")
            temp_frame.columnconfigure(0, minsize=210)
            file_checkbutton = tk.Checkbutton(temp_frame, variable=self.checked_file, onvalue=char_name, offvalue=None)
            file_checkbutton.grid(row=row, column=0, sticky="e")
            file_label = tk.Label(temp_frame, text=char_name, font=(18))
            file_label.grid(row=row, column=1, sticky="we")

    def build_new_character_menu(self):
        self.root.game = Game()
        self.select_hero_image = tk.PhotoImage(file='data/images/select_hero.png')
        self.hero_select_knight_image = tk.PhotoImage(file='data/images/hero_select_knight.png')
        self.hero_select_thief_image = tk.PhotoImage(file='data/images/hero_select_thief.png')
        self.hero_select_wizard_image = tk.PhotoImage(file='data/images/hero_select_wizard.png')

        self.new_character_frame = tk.Frame(self, bg="GREY")
        self.new_character_frame.grid(row=0, columnspan=2, sticky="snew")
        self.new_character_frame.columnconfigure(0, weight=1)
        self.new_character_frame.columnconfigure(1, weight=0)
        self.new_character_frame.columnconfigure(2, weight=0)
        self.new_character_frame.columnconfigure(3, weight=0)
        self.new_character_frame.columnconfigure(4, weight=1)
        self.new_character_frame.rowconfigure(0, weight=1)
        self.new_character_frame.rowconfigure(1, weight=1)
        self.new_character_frame.rowconfigure(2, weight=1)

        def set_player_hero(hero_name):
            hero_chart = {
                'knight': characters.Knight(),
                'wizard': characters.Wizard(),
                'thief': characters.Thief()
            }
            self.root.game.player = hero_chart[hero_name]
            self.build_input_new_game()


        #SELECT HERO LABEL
        self.select_hero_label = tk.Label(self.new_character_frame, image=self.select_hero_image, bg="grey")
        self.select_hero_label.grid(row=0, column=1, columnspan=3)
        #hero_select_knight
        self.hero_select_knight_button = tk.Button(self.new_character_frame, image=self.hero_select_knight_image, bg="grey",
            command=lambda:set_player_hero('knight')
        )
        self.hero_select_knight_button.grid(row=1, column=1, padx=10)
        #hero_select_thief
        self.hero_select_thief_button = tk.Button(self.new_character_frame, image=self.hero_select_thief_image, bg="grey",
            command=lambda:set_player_hero('thief')
            )
        self.hero_select_thief_button.grid(row=1, column=2, padx=10)
        #hero_select_wizard
        self.hero_select_wizard_button = tk.Button(self.new_character_frame, image=self.hero_select_wizard_image, bg="grey",
            command=lambda:set_player_hero('wizard')
        )
        self.hero_select_wizard_button.grid(row=1, column=3, padx=10)

    def build_start_screen(self):
        self.btn_image = tk.PhotoImage(file='data/images/welcome.png')
        self.start_screen_frame = tk.Frame(self, bg="GREY")
        self.start_screen_frame.grid(columnspan=2, sticky="snew")
        self.start_screen_frame.columnconfigure(0, weight=1)
        self.start_screen_frame.rowconfigure(0, weight=1)
        self.start_screen_frame.rowconfigure(1, weight=1)
        self.start_screen_frame.rowconfigure(2, weight=1)
        self.start_game_button = tk.Button(self.start_screen_frame, image=self.btn_image,
        command=lambda:self.switch_frame(self.build_start_menu, self.start_screen_frame)
        )
        self.start_game_button.grid(row=1)

    def movement(self, direction):
        if not direction:
            self.place_holder = self.game_map
            self.game_map = GuiGameMap(self.root, self.game_map_frame)
            self.place_holder.destroy()
        else:
            room = self.root.game.game_map.make_move(direction)
            if room == 'exit':
                self.finish_dungeon_popup()
            if isinstance(room, gamemap.Room):
                self.place_holder = self.game_map
                self.game_map = GuiGameMap(self.root, self.game_map_frame)
                self.place_holder.destroy()
                if not room.cleared:
                    self.get_room_content(room)

    def get_room_content(self, room):
        if room.get_contents():
            self.build_room_description_prompt(room)
        
    def set_rowconfigure(self):
        self.rowconfigure(0, weight=1)

    def set_columnconfigure(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
    def build_game_map_frame(self, container):
        self.game_map_frame = tk.Frame(container, borderwidth=2, relief=tk.SUNKEN, bg="GREY")
        self.game_map_frame.grid(row=0, column=1, sticky="nswe")
        self.game_map_frame.rowconfigure(0, weight=1)
        self.game_map_frame.columnconfigure(0, weight=1)
        self.game_map = GuiGameMap(self.root, self.game_map_frame)

    def build_player_frame(self, container):
        self.player_frame = tk.Frame(container, borderwidth=2, relief=tk.SUNKEN, bg="GREY")
        self.player_frame.grid(row=0, column=0, sticky="nwes")
        self.player_frame.rowconfigure(0, weight=0)
        self.player_frame.rowconfigure(1, weight=1)
        self.player_frame.columnconfigure(0, weight=1)
        self.player_frame.columnconfigure(1, weight=1)
        self.player_frame.columnconfigure(2, weight=1)
        self.player = GuiPlayer(self.root, self.player_frame)
    
    def build_save_exit_frame(self, container):
        self.save_exit_image = tk.PhotoImage(file="data/images/save_and_exit2.png")
        self.save_exit_frame = tk.Frame(container, bg="GREY")
        self.save_exit_frame.grid(row=1, column=0, sticky="n", pady=20)
        self.save_exit_frame.rowconfigure(0, weight=0)
        self.save_exit_frame.rowconfigure(1, weight=0)
        self.save_exit_frame.rowconfigure(2, weight=0)
        self.save_exit_frame.columnconfigure(0, weight=0)
        self.save_exit_frame.columnconfigure(1, weight=0)
        self.save_exit_frame.columnconfigure(2, weight=0)
        #EXIT_BUTTON
        self.save_exit_button = tk.Button(self.save_exit_frame, text="EXIT", image=self.save_exit_image, bg="GREY",
            command=lambda:self.exit_dungeon_popup()
            )
        self.save_exit_button.grid(column=1, row=1, sticky="nsew")

    def build_movement_frame(self, container):
        self.up_image = tk.PhotoImage(file="data/images/arrow_up.png")
        self.down_image = tk.PhotoImage(file="data/images/arrow_down.png")
        self.left_image = tk.PhotoImage(file="data/images/arrow_left.png")
        self.right_image = tk.PhotoImage(file="data/images/arrow_right.png")
        self.movement_frame = tk.Frame(container, bg="GREY")
        self.movement_frame.grid(row=1, column=1, sticky="n", pady=10)
        self.movement_frame.rowconfigure(0, weight=1)
        self.movement_frame.rowconfigure(1, weight=1)
        self.movement_frame.rowconfigure(2, weight=1)
        self.movement_frame.columnconfigure(0, weight=0)
        self.movement_frame.columnconfigure(1, weight=0)
        self.movement_frame.columnconfigure(2, weight=0)
        #UP_BUTTON
        self.movement_up_button = tk.Button(self.movement_frame, image=self.up_image, bg="BLACK",
            command=lambda:self.movement("A")
            )
        self.movement_up_button.grid(column=1, row=0, sticky="nsew")
        #DOWN_BUTTON
        self.movement_down_button = tk.Button(self.movement_frame, image=self.down_image, bg="BLACK",
            command=lambda:self.movement("D")
            )
        self.movement_down_button.grid(column=1, row=2, sticky="nswe")
        #LEFT_BUTTON
        self.movement_left_button = tk.Button(self.movement_frame, image=self.left_image, bg="BLACK",
            command=lambda:self.movement("S")
            )
        self.movement_left_button.grid(column=0, row=1, sticky="nswe")
        #RIGHT BUTTON
        self.movement_right_button = tk.Button(self.movement_frame, image=self.right_image, bg="BLACK",
            command=lambda:self.movement("W")
            )
        self.movement_right_button.grid(column=2, row=1, sticky="nswe")

    def build_start_corner_frame(self, container):
        self.start_corner_frame = tk.Frame(container, bg="GREY")
        self.start_corner_frame.grid(row=1, column=0, columnspan=2, sticky="nwe", pady=10)
        self.start_corner_frame.rowconfigure(0, weight=0, minsize=50)
        self.start_corner_frame.rowconfigure(1, weight=0, minsize=50)
        self.start_corner_frame.rowconfigure(2, weight=0, minsize=50)
        self.start_corner_frame.rowconfigure(3, weight=0, minsize=50)
        self.start_corner_frame.columnconfigure(0, weight=0, minsize=50)
        self.start_corner_frame.columnconfigure(1, weight=0, minsize=50)
        self.start_corner_frame.columnconfigure(2, weight=0, minsize=50)
        self.start_corner_label = tk.Label(self.start_corner_frame, text="Choose a corner to start on!", font=("Times", 14), bg="GREY")
        self.start_corner_label.grid(row=0, column=2, columnspan=2, sticky="nwe")
        #TOP_LEFT_BUTTON
        self.top_left_button = tk.Button(self.start_corner_frame, text="TOP LEFT",
            command=lambda: self.set_start_position('b-l')
            )
        self.top_left_button.grid(column=2, row=1, sticky="nsew")
        #TOP_RIGHT_BUTTON
        self.top_right_button = tk.Button(self.start_corner_frame, text="TOP RIGHT",
            command=lambda: self.set_start_position('t-l')
            )
        self.top_right_button.grid(column=3, row=1, sticky="nsew")
        #BOTTOM_RIGHT_BUTTON
        self.bottom_right_button = tk.Button(self.start_corner_frame, text="BOTTOM RIGHT",
            command=lambda: self.set_start_position('t-r'))
        self.bottom_right_button.grid(column=3, row=2, sticky="NSWE")
        #BOTTOM_LEFT_BUTTON
        self.bottom_left_button = tk.Button(self.start_corner_frame, text="BOTTOM LEFT",
            command=lambda: self.set_start_position('b-r'))
        self.bottom_left_button.grid(column=2, row=2, sticky="nswe")

    def build_room_frame(self, room):
        self.room_frame = tk.Frame(self.app_frame, bg="#2c2c2c")
        self.room_frame.grid(row=0, column=0, columnspan=3, sticky="nswe")
        self.room_frame.rowconfigure(0, weight=1)
        self.room_frame.columnconfigure(0, weight=1)
        self.room = GuiRoom(self.root, self.room_frame, room, self)

    def build_room_description_prompt(self, room):
        self.room_image = tk.PhotoImage(file='data/images/room_image.png')
        self.room_description_frame = tk.Frame(self, bg="GREY")
        self.room_description_frame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        self.room_description_frame.columnconfigure(0, weight=1)
        self.room_description_frame.rowconfigure(0, weight=1)
        self.room_description_frame.rowconfigure(1, weight=1)
        self.room_description_frame.rowconfigure(2, weight=0)
        self.room_description_frame.rowconfigure(3, weight=1)
        #flavör
        self.room_description_label = tk.Label(
            self.room_description_frame,
            text=room.description,
            image=self.room_image, 
            bg="GREY",
            font=("Times", 30), fg=self.root.color_mapping['flavour_text_color'],
            relief=tk.RAISED,
            borderwidth=2,
            compound='center'
            )
        self.room_description_label.grid(row=1)
        self.enter_room_button = tk.Button(
            self.room_description_frame,
            text="Continue",
            font=("Times", 14, 'bold'),
            command=lambda:self.enter_room(room, self.room_description_frame)
            )
        self.enter_room_button.grid(row=2, sticky="nswe")
        

class GuiGameMap(tk.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.room_scheme = {
            'O': tk.PhotoImage(file='data/images/open_door.png'),
            '-': tk.PhotoImage(file='data/images/closed_door.png'),
            'X': tk.PhotoImage(file=root.game.player.room_image),
            'E': tk.PhotoImage(file='data/images/half_open_door.png')
        }
        self.game_map = root.game.game_map
        self.create_game_map()
        self.grid(sticky="nswe", row=0, column=0)

    def update(self):
        self.create_game_map()

    def create_game_map(self):
        for col_num, column in enumerate(self.game_map.map_grid):
            self.columnconfigure(col_num, weight=1, minsize=75)
            for row_num, room in enumerate(column):
                self.rowconfigure(row_num, weight=1, minsize=75)
                label = tk.Label(self, image=self.room_scheme[room.get_room_state()], bg="GREY")
                label.grid(row=row_num, column=col_num, sticky="nswe")


class GuiPlayer(tk.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.root = root
        self.player = root.game.player
        self.player_image = tk.PhotoImage(file=self.player.image)
        self.backpack_image = tk.PhotoImage(file=self.player.backpack_image)
        self.create_player()
        self.grid(sticky="nwe", columnspan=3)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def update(self):
        if self.player.get_health() > 0:
            self.player_health_label.config(text = f"Health: {self.player.health}")
        elif self.player.get_health() == 0:
            self.player_health_label.config(text = f"DEAD", bg=self.root.color_mapping['combat_red'])
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
        self.player_initiative_label = tk.Label(self.create_player_details_frames, text="PLAYER INITIATIVE", bg="#0094db")
        self.player_initiative_label.grid(row=4, sticky="new")
        #player_backpack_frame
        self.player_backpack_frame = tk.Frame(self.create_player_details_frames, relief=tk.RAISED, borderwidth=2)
        self.player_backpack_frame.grid(row=5, sticky="nwes")
        self.player_backpack_frame.rowconfigure(0, weight=1, minsize=150)
        self.player_backpack_frame.rowconfigure(1, weight=1)
        self.player_backpack_frame.rowconfigure(2, weight=1)
        self.player_backpack_frame.columnconfigure(0, weight=1, minsize=100)
        #player_backback
        self.player_backback_label = tk.Label(self.player_backpack_frame, image=self.backpack_image, bg="GREY")
        self.player_backback_label.grid(row=0, rowspan=3, column=0, sticky="wens")
        self.player_backback_value_label = tk.Label(self.player_backpack_frame, font=('Times', 14), bg="GREY")
        self.player_backback_value_label.grid(column=0, row=0, sticky="s")


class GuiRoom(tk.Frame):
    def __init__(self, root, parent, room, app):
        super().__init__(parent, bg="GREY")
        self.root = root
        self.app = app
        self.parent = parent
        self.room_obj = room
        self.rowconfigure(0, weight=0, minsize=250)
        self.rowconfigure(1, weight=1, minsize=50)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)
        self.columnconfigure(4, weight=1)
        self.create_room()
        self.grid(sticky="nwes")

    def room_flee(self):
        self.parent.destroy()
        self.root.game.game_map.make_step_back()
        del self.combat
        del self.root.game.combat_session
        self.app.movement(None)

    def room_kill(self):
        self.root.game.loot_treasures(self.room_obj)
        self.room_obj.set_room_cleared()
        self.parent.destroy()

    def update(self):
        self.combat_status_label.config(text=f"{self.root.game.combat_session.current_turn.get_name()}'s turn!")
        for entity_frame in self.all_entity_frames:
            entity_frame.update()
        if self.combat.is_combat_won():
            self.create_room_won_frames()
            del self.combat
            del self.root.game.combat_session
        elif self.combat.is_combat_lost():
            self.create_room_lost_frames()
            del self.combat
            del self.root.game.combat_session
        elif self.combat.combat_escaped:
            self.room_flee()
        
    def create_room(self):
        self.all_entity_frames = list()
        self.create_enemy_frames()
        self.create_player_frames()
        self.create_combat_frames()

    def create_combat_session(self, combatants):
        self.root.game.combat_session = demo_combat.Combat(combatants)

    def create_combat_frames(self):
        combatants = [self.root.game.player]
        enemies = self.room_obj.content['enemies']
        combatants.extend(enemies)
        self.create_combat_session(combatants)
        self.combat_status_frame = tk.Frame(self,  bg=self.root.color_mapping['attack'])
        self.combat_status_frame.grid(row=1, columnspan=5, sticky="nswe")
        self.combat_status_frame.rowconfigure(0, weight=1)
        self.combat_status_frame.columnconfigure(0, weight=1)
        self.combat_status_frame.columnconfigure(1, weight=1)
        self.combat_status_frame.columnconfigure(2, weight=1)
        self.combat_status_label = tk.Label(
            self.combat_status_frame,
            font=("Times", 22, 'bold'),
            bg=self.root.color_mapping['attack']
            )
        self.combat_status_label.grid(column=1, stick="wesn")
        self.combat_container = tk.Frame(self, bg="GREY")
        self.combat_container.grid(row=2, column=1, columnspan=len(self.all_entity_frames), sticky="nwe")
        self.combat_container.columnconfigure(0, weight=1)
        self.combat_container.rowconfigure(0, weight=1)
        self.combat = GuiCombat(self.root, self.combat_container, self.room_obj.content['enemies'])

    def create_player_frames(self):
        self.player_container = tk.Frame(self, bg='GREY')
        self.player_container.grid(row=2, column=0, sticky="nwe")
        self.player_container.rowconfigure(0, weight=1)
        self.player_container.columnconfigure(0, weight=0)
        self.all_entity_frames.append(GuiEntity(self.root, self.player_container, self.root.game.player, 0))

    def create_enemy_frames(self):
        self.enemy_container = tk.Frame(self, bg='GREY')
        self.enemy_container.grid(row=0, column=3, sticky="en")
        self.enemy_container.rowconfigure(0, weight=1)
        self.enemy_container.columnconfigure(0, weight=1)
        for entity_num, enemy in enumerate(self.room_obj.content['enemies']):
            self.all_entity_frames.append(GuiEntity(self.root, self.enemy_container, enemy, entity_num))

    def create_room_lost_frames(self):
        self.game_over_image = tk.PhotoImage(file='data/images/game_over.png')
        self.lose_container = tk.Frame(self, bg=self.root.color_mapping['victory_grey'], relief=tk.RAISED, borderwidth=5)
        self.lose_container.grid(row=0, rowspan=4, column=0, columnspan=5, sticky="nswe")
        self.lose_container.rowconfigure(0, weight=0)
        self.lose_container.rowconfigure(1, weight=0)
        self.lose_container.columnconfigure(0, weight=1)
        self.lose_container.columnconfigure(1, weight=1)
        self.lose_container.columnconfigure(2, weight=1)
        #app.delete_game_progress
        #lose label
        self.lose_label = tk.Label(self.lose_container, image=self.game_over_image, text="GAME OVER!", font=("Times", 20, 'bold'), relief=tk.RAISED, borderwidth=2)
        self.lose_label.grid(row=0, column=0, columnspan=3)
        #Exit_to_menu
        self.exit_room_button = tk.Button(self.lose_container, text="Exit: Main Menu", font=('Arial', 13, 'bold'), command=lambda:self.app.delete_game_progress(self.app.build_start_menu, self.app.app_frame))
        self.exit_room_button.grid(column=1, row=2, sticky="nswe")
        #Exit_button
        self.exit_room_button = tk.Button(self.lose_container, text="Exit: Game", font=('Arial', 13, 'bold'), command=lambda:self.app.delete_game_progress(None, sys.exit))
        self.exit_room_button.grid(column=1, row=3, sticky="nswe")

    def create_room_won_frames(self):
        self.all_treasure_images = list()
        self.victory_container = tk.Frame(self, bg=self.root.color_mapping['victory_grey'], relief=tk.RAISED, borderwidth=5)
        self.victory_container.grid(row=1, rowspan=3, column=0, columnspan=5, sticky="nswe")
        self.victory_container.rowconfigure(0, weight=0)
        self.victory_container.rowconfigure(1, weight=0)
        self.victory_container.rowconfigure(2, weight=0)
        self.victory_container.rowconfigure(3, weight=0)
        self.victory_container.columnconfigure(0, weight=1)
        self.victory_container.columnconfigure(1, weight=1)
        self.victory_container.columnconfigure(2, weight=1)

        #victory label
        self.victory_label = tk.Label(self.victory_container, text="Room Cleared", font=("Times", 20, 'bold'), relief=tk.RAISED, borderwidth=2)
        self.victory_label.grid(row=1, column=0, columnspan=3,  sticky="nwe")
        #treasures
        self.victory_treasure_frame = tk.Frame(self.victory_container, bg=self.root.color_mapping['treasure_green'])
        self.victory_treasure_frame.grid(row=2, column=1, sticky="nwe")
        self.victory_treasure_frame.rowconfigure(0, weight=1)
        self.victory_treasure_frame.columnconfigure(0, weight=1)
        self.victory_treasure_frame.columnconfigure(1, weight=1)
        self.victory_treasure_frame.columnconfigure(2, weight=0)
        self.victory_treasure_frame.columnconfigure(3, weight=1)
        self.treasure_label = tk.Label(self.victory_treasure_frame, text="Treasures Found:", font=("Times", 15), bg=self.root.color_mapping['treasure_green'], relief=tk.RAISED, borderwidth=2)
        self.treasure_label.grid(row=0, columnspan=4, sticky='nwe')
        self.treasure_sum = 0
        for row_num, treasure in enumerate(self.room_obj.content['treasures']):
            self.treasure_sum += treasure.get_value()
            #filler_num
            num_item_label = tk.Label(
                self.victory_treasure_frame,
                relief=tk.RAISED,
                borderwidth=2,
                text=row_num+1,
                bg=self.root.color_mapping['treasure_green']
            )
            num_item_label.grid(row=row_num+1, column=0, sticky="nswe")
            #name
            treasure_name_label = tk.Label(
                self.victory_treasure_frame,
                relief=tk.RAISED,
                borderwidth=2,
                text=treasure.get_name(),
                bg=self.root.color_mapping['treasure_green']
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
                bg=self.root.color_mapping['treasure_green']
                )
            treasure_value_label.grid(row=row_num+1, column=3, sticky="nswe")
        self.treasure_sum_label = tk.Label(
            self.victory_treasure_frame,
            relief=tk.RAISED,
            borderwidth=2,
            text=f'Total value: {self.treasure_sum}',
            bg=self.root.color_mapping['treasure_green'],
            font=("Times", 15)
            )
        self.treasure_sum_label.grid(row=len(self.room_obj.content['treasures'])+1, column=0, columnspan=4, sticky="nswe")
        #Exit_button
        self.exit_room_button = tk.Button(self.victory_container, text="Loot Treasures & Continue", font=('Arial', 13, 'bold'), command=lambda:self.room_kill())
        self.exit_room_button.grid(column=1, row=3, sticky="nswe")


class GuiEntity(tk.Frame):
    def __init__(self, root, parent, entity, entity_num):
        super().__init__(parent, borderwidth=2, relief=tk.RAISED, bg="GREY")
        self.root = root
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
            self.entity_health.config(bg=self.root.color_mapping['dead'], text="DEAD")

    def build_entity_frame(self):
        color = "GREY"
        #image
        self.entity_image = tk.Label(self, image=self.image, bg=color)
        self.entity_image.grid(row=0, sticky="snwe")
        #name
        self.entity_name = tk.Label(self, text=self.entity.get_name(), bg=color, font=('Times', 12, 'bold'))
        self.entity_name.grid(sticky="snwe")
        #health
        self.entity_health = tk.Label(self, text=f'Health: {self.entity.get_health()}', bg=self.root.color_mapping['health'])
        self.entity_health.grid(sticky="snwe")
        #attack
        self.entity_attack = tk.Label(self, text=f'Attack: {self.entity.get_attack()}', bg=self.root.color_mapping['attack'])
        self.entity_attack.grid(sticky="snwe")
        #agility
        self.entity_agility = tk.Label(self, text=f'Agility: {self.entity.get_agility()}', bg=self.root.color_mapping['agility'])
        self.entity_agility.grid(sticky="snwe")
        #initiative
        self.entity_initiative = tk.Label(self, text=f'Initiative: {self.entity.get_initiative()}', bg=self.root.color_mapping['initiative'])
        self.entity_initiative.grid(sticky="snwe")


class GuiCombat(tk.Frame):
    def __init__(self, root, parent, enemies):
        super().__init__(parent, bg="GREY")
        self.root = root
        self.combat_session = self.root.game.combat_session
        self.parent = parent
        self.enemies = enemies
        self.create_combat()
        self.grid(sticky="nswe")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.combat_escaped = False
        self.block = False
        if self.root.game.player.special_ability == 'Sheild block':
            self.block = True
       
    def next_turn(self):
        self.enemy_turn_action(self.combat_session.current_turn)
        entity, value = self.combat_session.get_next_object_in_turn_order()
        self.combat_session.current_turn = entity

    def enemy_turn_action(self, enemy):
        player = self.root.game.player
        message = ""
        attack_value, defend_value = self.combat_session.attack(enemy, player)
        rolls = f"{enemy.get_name()} attacked for {attack_value} and {player.get_name()} defended for {defend_value}"
        if attack_value > defend_value:
            special = ""
            damage = 1
            if self.block:
                self.block = False
                damage = 0
                special = "Shield Block: "
            new_health = player.get_health() - damage
            player.set_health(new_health)
            message = f"{special}{enemy.get_name()} dealt {damage} damage to {player.get_name()}."
            if self.combat_session.is_entity_dead(player):
                self.update_text_field(f'{player.get_name()} died!')
        else:
            message = f"{player.get_name()} sucessfully defended and took no damage."
        self.update_text_field(message)
        self.update_text_field(rolls)
        self.update_text_field(f'{"="*10}Turn {self.combat_session.total_turns}{"="*10}')

    def player_turn_action(self, action):
        if action == 'Flee':
            chance = self.combat_session.flee(self.root.game.player)
            if self.is_combat_escaped(chance):
                self.combat_escaped = True
                for enemy in self.combat_session.combatants:
                    if isinstance(enemy, enemies.Enemy):
                        enemy.set_health(enemy.max_hp)
            else:
                self.update_text_field(f'{self.root.game.player.get_name()} did not escape.')
                self.update_text_field(f'{"="*10}Turn {self.combat_session.total_turns}{"="*10}')
        if action == 'Attack':
            for enemy, value in self.combat_session.turn_order:
                if isinstance(enemy, enemies.Enemy):
                    attack_value, defend_value = self.combat_session.attack(self.combat_session.current_turn, enemy)
                    rolls = f"{self.combat_session.current_turn.get_name()} attacked for {attack_value} and {enemy.get_name()} defended for {defend_value}"
                    if attack_value > defend_value:
                        damage = 1
                        special = ""
                        if self.root.game.player.special_ability == 'Critical strike!':
                            if random.randrange(0, 4) == 1:
                                damage *= 2
                                special = "Critical Strike: "
                        message = f"{special}{self.combat_session.current_turn.get_name()} dealt {damage} damage to {enemy.get_name()}."
                        new_health = enemy.get_health() - damage
                        enemy.set_health(new_health)
                        if self.combat_session.is_entity_dead(enemy):
                            self.update_text_field(f'{enemy.get_name()} died!')
                            self.combat_session.remove_entity((enemy, value))
                        self.update_text_field(message)
                    else:
                        message = f"{enemy.get_name()} sucessfully defended and took no damage."
                        self.update_text_field(message)
                    self.update_text_field(rolls)
                    self.update_text_field(f'{"="*10}Turn {self.combat_session.total_turns}{"="*10}')
        entity, value = self.combat_session.get_next_object_in_turn_order()
        self.combat_session.current_turn = entity

    def is_combat_escaped(self, chance):
        if chance > random.randint(1, 100):
            return True

    def is_combat_won(self):
        total = sum([enemy.get_health() for enemy in self.enemies])
        if total == 0:
            return True

    def is_combat_lost(self):
        if self.root.game.player.health <= 0:
            return True

    def update_text_field(self, text):
        self.combat_text_field.config(state='normal')
        self.combat_text_field.insert(1.0, f'>> {text}\n')
        self.combat_text_field.config(state='disabled')

    def update(self):
        if isinstance(self.combat_session.current_turn, characters.Character):
            self.combat_next_turn_frame.lower()
            self.combat_menu_frame.lift()
        elif isinstance(self.combat_session.current_turn, enemies.Enemy):
            self.combat_menu_frame.lower()
            self.combat_next_turn_frame.lift()
        self.after(100, self.update)

    def create_combat(self):
        self.create_player_combat_options()
        self.create_next_combat_turn_options()
        self.create_combat_text()
        #SHOW TURN_ORDER
        display_order = f"{'='*10}Turn order{'='*10}\n"
        for turn, entity in enumerate(self.combat_session.turn_order):
            display_order += f'Turn {turn+1}: {entity[0].get_name()} with start value: {entity[1]}\n'
        self.update_text_field(display_order)
        self.update()

    def create_combat_text(self):
        self.combat_text_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.combat_text_frame.grid(row=1, column=1, columnspan=2, sticky="nswe")
        self.combat_text_frame.rowconfigure(0, weight=0)
        self.combat_text_frame.rowconfigure(1, weight=1)
        self.combat_text_frame.columnconfigure(0, weight=1)
        self.combat_text_label = tk.Label(self.combat_text_frame, text="Terminal", bg="BLACK", fg="WHITE")
        self.combat_text_label.grid(row=0, column=0, sticky="nwe")
        self.combat_text_field = tk.Text(self.combat_text_frame, bg="BLACK", height=17, fg="WHITE")
        self.combat_text_field.grid(row=1, column=0, sticky="nwes")

    def create_next_combat_turn_options(self):
        self.combat_next_turn_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.combat_next_turn_frame.grid(row=0, column=1, columnspan=2, sticky="nwes")
        self.combat_next_turn_frame.rowconfigure(0, weight=1)
        self.combat_next_turn_frame.columnconfigure(0, weight=1)
        #Next turn button
        self.next_turn_button = tk.Button(self.combat_next_turn_frame, text="Next Turn",
            command=lambda:self.next_turn()
            )
        self.next_turn_button.grid(row=0, column=0, sticky="nswe")
        self.combat_next_turn_frame.lower()

    def create_player_combat_options(self):
        self.combat_menu_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.combat_menu_frame.grid(row=0, column=1, columnspan=2, sticky="nwe")
        self.combat_menu_frame.rowconfigure(0, weight=1)
        self.combat_menu_frame.rowconfigure(1, weight=1)
        self.combat_menu_frame.rowconfigure(2, weight=1)
        self.combat_menu_frame.columnconfigure(0, weight=1)
        #Menu_label
        self.combat_menu_label = tk.Label(self.combat_menu_frame, text="Combat Menu")
        self.combat_menu_label.grid(row=0, column=0, columnspan=2, sticky="wne")
        #Attack_button
        self.combat_attack_button = tk.Button(self.combat_menu_frame, text="Attack",
            command=lambda:self.player_turn_action('Attack')
            )
        self.combat_attack_button.grid(row=1, column=0, sticky="nwe")     
        #Flee_button
        self.combat_flee_button = tk.Button(self.combat_menu_frame, text="Flee", 
            command=lambda:self.player_turn_action('Flee')
        )
        self.combat_flee_button.grid(row=2, column=0, sticky="nwe")
