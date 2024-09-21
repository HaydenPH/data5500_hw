# XML (extensable mark up language) VS. JSON (Java Scrpit Object Notation)
# XML is unpopular beacuse its verbose, a lot of structural info, hard on the eyes
# HTML Hyper Text Markup Language
# JavaScript is used for creating websites 
# API (application programming interface)

# GETTING DATA FOR WEB JSON API

import requests
import json

url = "https://api.datamuse.com/words?m1=duck"

word_key = "word"
score_key = "score"

req = requests.get(url)
txt = req.text
print(txt)

lst_dct = json.loads(txt)

for dct in lst_dct:
    if dct[word_key] == "aggies":
        print(dct[score_key])