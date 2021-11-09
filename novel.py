import json
import random
import novelvars

extra_text_chance = 50

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
        flavor_text = get_tailored_text("generic")
        if "intro" in flavor_text["tags"] and novelvars.on_route:
            continue
        text_roll = random.randint(0, 100)
        if flavor_text["probability"] < text_roll:
            continue
        chosen_text = flavor_text["text"]
        chosen_text += roll_for_extra_text("generic2", chosen_text)
        break
    if "onetime" in flavor_text["tags"]:
        for i in range(len(novelvars.flavor_strings)):
            if novelvars.flavor_strings[i]["text"] == flavor_text["text"]:
                novelvars.flavor_strings[i]["usable"] = False
                break
    write_text(chosen_text)

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
        if novelvars.on_route:
            return get_tailored_text("notime")["text"]

        else:
            return get_tailored_text("notimeintro")["text"]
    else:
        return ("I've been out here %s." %(text))

def get_speed_text(text):
    speed = get_skifree_number(text)
    if speed > 21:
        speed_text = get_tailored_text("airborne")["text"]
        speed_text += roll_for_extra_text("airborne2")
        return speed_text
    else:
        return ("I'm going %s." %(text))

def get_distance_text(text):
    distance = get_skifree_number(text)
    distance_delta = novelvars.last_distance - distance
    novelvars.last_distance = distance
    if distance > 2000:
        return "I've gone too far..."
    update_distance_state(distance, distance_delta)
    distance_text = ("I've gone %s now." %(text))
    if distance_delta < 0 and novelvars.on_route:
        distance_text += (" " + get_tailored_text("backward")["text"])
    return distance_text

def update_distance_state(distance, delta):
    if distance > 1001:
        novelvars.on_route = False
    if abs(delta) > 400: # When you choose a route (slalom etc), distance jumps from ~30 to ~500/1000/~1200
        novelvars.on_route = True

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
    while True:
        filtered_text = [text for text in novelvars.flavor_strings if tag in text["tags"]]
        tailored_text = random.choice(filtered_text)
        if not tailored_text["usable"]:
            continue
        break
    return tailored_text

def roll_for_extra_text(specific_tag, repeatable_text = None):
    extra_text_roll = random.randint(0, 100)
    if extra_text_chance > extra_text_roll:
        extra_text = get_tailored_text(specific_tag)["text"]
        if repeatable_text and repeatable_text == extra_text:
            return ""
        else:
            return (" " + extra_text)
    else:
        return ""