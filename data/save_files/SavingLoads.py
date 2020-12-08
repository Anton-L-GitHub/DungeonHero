import json


class load():
    #Loading from Json file
    def Loading():
        with open('example.json') as f:
            sample_data = json.load(f)


class save():
    #Saving to Json file
    def saving():
        with open('name_of_file', 'w') as f:
            json.dump(sample_data, f, indent=2)