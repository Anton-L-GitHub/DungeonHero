import json


#Sample Data to be written
mapSave = {
    "save data" : " save data",
    "save data" : "save data",
    "save data" : "save data",
    "save data" : "save data"
}

with open ("mapSave.json", "w") as s_outfile:
    json.dump(mapSave, s_outfile)


