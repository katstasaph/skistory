import json

global used_text
used_text = None

global last_distance
last_distance = 0

global last_speed
last_speed = 0

global sentences
sentences = 0

global words
words = 0

global skinovel
skinovel = open("skinovel.txt", "w+")

global flavor_text
flavor_text = open('flavortext.json', "r+", encoding="utf-8")
flavor_strings = json.load(flavor_text)