import sys
import os
os.system(sys.executable + " -m pip install requests")

import requests
import json
import time
from datetime import datetime

file_path = "/Users/haydenhatch/data5500/hw5/states_territories.txt"
states_t = [ line.strip() for line in open(file_path).readlines() ]
print(states_t)

url1 = "https://api.covidtracking.com/v1/states/"
url2 = "/daily.json"

for state in states_t:
    url = url1 + state + url2
    req = requests.get(url)
    data = json.loads(req.text)

    folder_path = "/Users/haydenhatch/data5500/hw5/StateJSONs"
    filename = os.path.join(folder_path,f"{state}.json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

