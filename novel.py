import json
import random
import novelvars

extra_text_chance = 50
max_ground_speed = 21 # Any speed > 21 means we've jumped
max_safe_distance = 2000 # After this distance the yeti appears
post_route_distance = 1020 # The post-route stretch is 1000 on
new_route_delta = 400 # When you choose a route (slalom etc), distance jumps from ~30 to ~500-1200

# Characters that only appear in specific categories of string from SkiFree, so we can tell what string type we have

time_string_indicator = ":" # Colons only show up in time strings
speed_string_indicator = "m/s" # "m/s" only shows up in the strings strings
distance_string_indicator = "m" # "m" alone shows up in distance strings, but we check speed first

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
    if text in novelvars.starter_text:
        return novelvars.starter_text.get(text)
    elif time_string_indicator in text:
        return get_time_text(text)
    elif speed_string_indicator in text:
        return get_speed_text(text)
    elif distance_string_indicator in text:
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
    update_speed_state(speed)
    if check_crash():
        speed_text = ((random.choice(novelvars.crash_preambles)) + get_tailored_text("crash")["text"])
        speed_text += roll_for_extra_text("crash2")
        return speed_text
    if speed > max_ground_speed:
        speed_text = get_tailored_text("airborne")["text"]
        speed_text += roll_for_extra_text("airborne2")
        return speed_text
    else:
        return ("I'm going %s." %(text))

def update_speed_state(speed):
    novelvars.last_speeds.popleft()
    novelvars.last_speeds.append(speed)

# A quick and dirty method of crash detection, using text only. It errs on the side of false negatives.
# Basically: Did our speed go from normal to 0 suddenly, and did we stop moving?
def check_crash():
    return abs(novelvars.last_speeds[0] - novelvars.last_speeds[2]) > 7 and novelvars.last_distance_delta == 0

def get_distance_text(text):
    distance = get_skifree_number(text)
    distance_delta = novelvars.last_distance - distance
    update_distance_state(distance, distance_delta)
    distance_text = ("I've gone %s now." %(text))
    if distance > max_safe_distance:
        distance_text += " I've gone too far..."
    elif distance > post_route_distance:
        distance_postscript = get_tailored_text("postroute")["text"]
        distance_text += (" " + distance_postscript + roll_for_extra_text("postroute", distance_postscript))
    elif distance_delta < 0 and novelvars.on_route:
        distance_text += (" " + get_tailored_text("backward")["text"])
    return distance_text

def update_distance_state(distance, delta):
    novelvars.last_distance = distance
    novelvars.last_distance_delta = delta
    if distance > post_route_distance:
        novelvars.on_route = False
        novelvars.post_ski = True
    if abs(delta) > new_route_delta:
        novelvars.on_route = True

def get_style_text(text):
    style = get_skifree_number(text)
    style_text = "I ask myself how I'm skiing. "
    if novelvars.post_ski:
        style_text += get_tailored_text("afterscore")["text"]
    elif style < 0:
        style_text += get_tailored_text("bad")["text"]
    elif style > 0:
        style_text += get_tailored_text("good")["text"]
    else:
        style_text += get_tailored_text("noscore")["text"]
    return style_text

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