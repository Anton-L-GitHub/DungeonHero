import json
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
    try:
        with open(json_path, 'w+') as f:
            json.dump(player.__dict__, f, indent=4)
    except FileNotFoundError as F:
        print(F)
        

def disc_save_progress(player, map):
    json_path_orig = f'data/database/characters'
    onlyfiles = [f for f in listdir(json_path_orig) if isfile(join(json_path_orig, f))]
    tempString = f'character_{player.name}.json'
    if tempString in onlyfiles:
        json_path_orig += f'/{tempString}'
        remove(json_path_orig)
    else:
        print("Couldn't find file.")
    # json_path = f'data/database/characters_ongoing/character_{player.name}.json'

def disc_save_map(list_of_dicts):
    """ Takes list of instances attributes in form of a py-dict and writes it to a json file """
    with open(json_file, 'w') as file:
        json.dump(list_of_dicts, file)

newPlayer = characters.Knight()
newPlayer.name = 'Stor pelle'
tempMap = gamemap.create_map_instance('medium')
tempMap.set_start_position('t-l')

disc_save_progress(newPlayer, tempMap)
