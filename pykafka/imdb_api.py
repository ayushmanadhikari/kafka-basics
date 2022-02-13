import requests
import json

url = "https://imdb8.p.rapidapi.com/auto-complete"

querystring = {"q":"the"}

headers = {
    'x-rapidapi-key': "dc208176f1mshf9dce5fdb32ac52p1cf561jsn29edbc65da4e",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

response_json = json.dumps(response.text)

print(response_json)

out_file = open('json_data', 'w')
json.dump(response_json, out_file)