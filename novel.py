import json
import random
import novelvars

starter_text = {
    "Time:": "I told myself I wasn't going to ski long.",
    "Dist:": "Or ski far.",
    "Speed:": "Or ski too fast.",
    "Style:": "I don't know how to ski."
}

def write_text(text):
    novelvars.skinovel.write("%s \n" % (text))
    novelvars.sentences += 1
    novelvars.words += len(text.split())

def print_flavor_text():
    while True:
        flavor_text = random.choice(novelvars.flavor_strings)
        if not flavor_text["usable"]:
            continue
        if "intro" in flavor_text["tags"] and novelvars.on_route:
            continue
        text_roll = random.randint(0, 100)
        if flavor_text["probability"] < text_roll:
            continue
        break
    if "onetime" in flavor_text["tags"]:
        for i in range(len(novelvars.flavor_strings)):
            if novelvars.flavor_strings[i]["text"] == flavor_text["text"]:
                novelvars.flavor_strings[i]["usable"] = False
                break
    write_text(flavor_text["text"])

def parse_text(text):
    if text in starter_text:
        return starter_text.get(text)
    elif ":" in text:  # only shows up in time...
        return get_time_text(text)
    elif "m/s" in text:  # speed...
        return get_speed_text(text)
    elif "m" in text:  # distance (we do speed first since m/s contains m)
        return get_distance_text(text)
    else:  # style
        return get_style_text(text)

def get_time_text(text):
    if "0:00:00.00" in text:
        return "I don't know how long I've been out here."
    else:
        return ("I've been out here %s." %(text))

def get_speed_text(text):
    speed = get_skifree_number(text)
    if speed > 21:
        return get_tailored_text("airborne")
    else:
        return ("I'm going %s." %(text))

def get_distance_text(text):
    distance = get_skifree_number(text)
    distance_delta = novelvars.last_distance - distance
    novelvars.last_distance = distance
    if distance > 2000:
        return "I've gone too far..."
    if abs(distance_delta) > 400: # When you choose a route (slalom etc), distance jumps from ~30 to ~500/1000/~1200
        novelvars.on_route = True
    distance_text = ("I've gone %s now." %(text))
    if distance_delta < 0 and novelvars.on_route:
        distance_text += " It takes all my energy to hoist my skis upward and go back."
    return distance_text

def get_style_text(text):
    style = get_skifree_number(text)
    if style < 0:
        return "I suck at skiing."
    elif style > 0:
        return "Check out my sick moves."
    else:
        return "Am I skiing well?"

def get_skifree_number(text):
    text = text.strip().strip("m/s").strip("m")
    if text != "0" and text != "00": # check for possible strings of just 0
        return int(text.lstrip("0"))
    else:
        return int(text)

def get_tailored_text(tag):
    filtered_text = [text for text in novelvars.flavor_strings if tag in text["tags"]]
    return random.choice(filtered_text)["text"]