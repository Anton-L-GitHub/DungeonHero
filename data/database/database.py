import json
from game_files import characters

""" Concerned with storing and retrieving media-objects from a JSON-file. """

json_file = 'data/database/data.json'


print("Test test")

def disc_get(json_file):
    """ Returns a list of all instances in db-file """
    with open(json_file, 'r') as file:
        return json.load(file)

def disc_save_character(player):
    newPlayer = player.__dict__
    print(newPlayer)

def disc_save_map(list_of_dicts):
    """ Takes list of instances attributes in form of a py-dict and writes it to a json file """
    with open(json_file, 'w') as file:
        json.dump(list_of_dicts, file)
