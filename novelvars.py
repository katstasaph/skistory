import json
import collections

# I know I know I know

global used_text
used_text = None

global last_time
global last_time_delta
last_time = 0
last_time_delta = 0

global last_distance
global last_distance_delta
last_distance = 0
last_distance_delta = 0

global last_speeds
last_speeds = collections.deque((0, 0, 0))

global on_route
on_route = False

global post_ski
post_ski = False

global sentences
sentences = 0

global words
words = 0

global skinovel
skinovel = open("skinovel.txt", "w+")

global flavor_text
flavor_text = open('flavortext.json', "r+", encoding="utf-8")
flavor_strings = json.load(flavor_text)

global starter_text
starter_text = {
    "Time:": "I told myself I wasn't going to ski long.",
    "Dist:": "Or ski far.",
    "Speed:": "Or ski too fast.",
    "Style:": "I don't know how to ski.\n"
}

global crash_preambles
crash_preambles = ["Crashed. ", "I'm downed. ", "I've collapsed. "]