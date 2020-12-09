import json

""" Concerned with storing and retrieving media-objects from a JSON-file. """

json_file = 'data/lib_register.json'

class Database:
    
    def __init__(self):
        self.check_json_file()


    def check_json_file(self):
        pass

    def disc_get():
        """ Returns a list of all instances in db-file """
        with open(json_file, 'r') as file:
            return json.load(file)


    def disc_save(list_of_dicts):
        """ Takes list of instances attributes in form of a py-dict and writes it to a json file """
        with open(json_file, 'w') as file:
            json.dump(list_of_dicts, file)
