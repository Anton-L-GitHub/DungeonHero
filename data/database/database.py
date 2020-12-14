import json
from types import SimpleNamespace
from game_files import characters, gamemap, enemies, treasures
from os import listdir, remove
from os.path import isfile, join

""" Concerned with storing and retrieving media-objects from a JSON-file. """


json_file = 'data/database/data.json'


def disc_get(json_file):
    """ Returns a list of all instances in db-file """
    with open(json_file, 'r') as file:
        return json.load(file)

def disc_save_character(player):
    json_path = f'data/database/characters/character_{player.name}.json'
    player_dict = {}
    player_dict['player'] = player
    try:
        with open(json_path, 'w+') as f:
            f.write(to_json(player_dict))
    except FileNotFoundError as F:
        print(F)

def to_json(obj):

    return json.dumps(obj, default=lambda obj: obj.__dict__, indent=4, separators=(",", " : "))

def disc_save_progress(player, player_map):
    json_path_orig = f'data/database/characters'
    
    onlyfiles = [f for f in listdir(json_path_orig) if isfile(join(json_path_orig, f))]
    tempString = f'character_{player.name}.json'
    if tempString in onlyfiles:
        json_path_orig += f'/{tempString}'
        remove(json_path_orig)

    mapDict = {}
    mapDict['map'] = player_map
    mapDict['player'] = player

    json_path = f'data/database/characters_ongoing/character_{player.name}.json'
    with open(json_path, 'w+') as file:
        file.write(to_json(mapDict))
        

def disc_load_character(player_name):
    json_path = f'data/database/characters/character_{player_name}.json'

    with open(json_path, 'r') as f:
        player_dict = json.load(f)

    newPlayer = characters.Character()
    temp_backpack = []
    for backpack in player_dict['player']['backpack']:
        temp_treasure = treasures.Treasure()
        json.loads(json.dumps(backpack), object_hook=temp_treasure.parse_data)
        temp_backpack.append(temp_treasure)

    json.loads(json.dumps(player_dict['player']), object_hook=newPlayer.parse_data) 

    newPlayer.backpack = temp_backpack

    return newPlayer

def disc_load_progress(player_name):
    json_path = f'data/database/characters_ongoing/character_{player_name}.json'

    with open(json_path, 'r') as f:
        data_dict = json.load(f)
    
    newPlayer = characters.Character()
    temp_backpack = []
    for backpack in data_dict['player']['backpack']:
        temp_treasure = treasures.Treasure()
        json.loads(json.dumps(backpack), object_hook=temp_treasure.parse_data)
        temp_backpack.append(temp_treasure)

    newMap = gamemap.GameMap(0, 0)
    newMap.create_map()
    map_dict = data_dict['map']
    y = []
    type_dict = {'exit_room': gamemap.ExitRoom, 'room': gamemap.EncounterRoom, 'enemies': enemies.Enemy, 'treasures': treasures.Treasure}
    for room_y in map_dict['map_grid']:
        x = []
        for room_x in room_y:

            temp_content = {'enemies': [], 'treasures': []}
            if len(room_x['content']['enemies']) > 0:
                for e in range(0, len(room_x['content']['enemies'])):
                    temp_content['enemies'].append(update_content(type_dict, 'enemies', room_x['content']['enemies'][e]))

            if len(room_x['content']['treasures']) > 0:
                for e in range(0, len(room_x['content']['treasures'])):
                    temp_content['treasures'].append(update_content(type_dict, 'treasures', room_x['content']['treasures'][e]))
            
            if room_x['state'] == "E":
                room_x = update_content(type_dict, 'exit_room', room_x)
            else:
                room_x = update_content(type_dict, 'room', room_x)
            
            room_x.content = temp_content
            x.append(room_x)
        y.append(x)
    
    json.loads(json.dumps(map_dict), object_hook=newMap.parse_data)
    newMap.map_grid = y

    json.loads(json.dumps(data_dict['player']), object_hook=newPlayer.parse_data) 

    newPlayer.backpack = temp_backpack
    
    return (newMap, newPlayer)
    

def update_content(type_dict, index, val):
    if index == 'room' or index == 'exit_room':
        td = type_dict[index]("temp")
    else:
        td = type_dict[index]()
    json.loads(json.dumps(val), object_hook=td.parse_data)
    return td

def disc_save_map(list_of_dicts):
    """ Takes list of instances attributes in form of a py-dict and writes it to a json file """
    with open(json_file, 'w') as file:
        json.dump(list_of_dicts, file)
