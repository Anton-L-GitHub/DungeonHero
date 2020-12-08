import json

class Save(

#Sample Data to be written
game_save = {
    "save data" : " save data",
    "save data" : "save data",
    "save data" : "save data",
    "save data" : "save data"
}

with open ("sample.json", "w") as s_outfile:
    json.dump(game_save, s_outfile)

)
