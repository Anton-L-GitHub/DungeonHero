import json
from types import SimpleNamespace
from game_files import characters, gamemap
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
    player_dict['player'] = player.__dict__
    try:
        with open(json_path, 'w+') as f:
            json.dump(player_dict, f, indent=4)
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
    json.loads(json.dumps(player_dict['player']), object_hook=newPlayer.parse_data) 

    return newPlayer


def disc_save_map(list_of_dicts):
    """ Takes list of instances attributes in form of a py-dict and writes it to a json file """
    with open(json_file, 'w') as file:
        json.dump(list_of_dicts, file)

def create_dump():
    newPlayer = characters.Knight()
    # newPlayer2 = characters.Knight()
    newPlayer.name = 'Mike'
    # newPlayer2.name = 'Leo'
    # tempMap = gamemap.create_map_instance('medium')
    # tempMap.set_start_position('t-l')

    # disc_save_progress(newPlayer, tempMap)
    test = disc_load_character(newPlayer.name)
    # test2 = disc_load_character(newPlayer2.name)
    print(f'{test.name}')

