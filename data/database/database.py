import json
from game_files import characters

""" Concerned with storing and retrieving media-objects from a JSON-file. """

json_file = 'data/database/data.json'


def disc_get(json_file):
    """ Returns a list of all instances in db-file """
    with open(json_file, 'r') as file:
        return json.load(file)

def disc_save_character(player):
    print(player.__dict__)
    json_path = f'data/database/characters/character_{player.name}.json'
    with open(json_path, 'w+') as f:
        json.dump(player.__dict__, f, indent=4)


def disc_save_map(list_of_dicts):
    """ Takes list of instances attributes in form of a py-dict and writes it to a json file """
    with open(json_file, 'w') as file:
        json.dump(list_of_dicts, file)

newPlayer = characters.Knight()
newPlayer.name = 'Pelle'

disc_save_character(newPlayer)
