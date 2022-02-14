#working with json
import json
import requests


data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

json_string = json.dumps(data, indent = 4)
print(json_string)

with open('json_play_data.json', 'r') as file:
    json_loaded = json.load(file)

print(json_loaded)