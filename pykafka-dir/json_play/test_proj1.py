#pulling in data from IMDB site about ratings of different movies and storing them in relational and non-relational format

import requests
import json
import pprint

url = "https://imdb8.p.rapidapi.com/auto-complete"
querystring = {"q":"spiderman"}
headers = {
    'x-rapidapi-key': "dc208176f1mshf9dce5fdb32ac52p1cf561jsn29edbc65da4e",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }
response = requests.request("GET", url, headers=headers, params=querystring)


pprint.pprint(response.json())
#print(type(response))

out_file = open('test_proj1_json_data', 'w')
json.dump(response.json(), out_file, indent=4)
print(response.text)