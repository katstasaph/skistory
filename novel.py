import json
import random
import novelvars

second_text_chance = 75 # padding
third_text_chance = 66 # more padding
fourth_text_chance = 50 # love to pad
yeti_text_roll_bound = 200 # To dampen the spread of yeti text
max_ground_speed = 21  # Any speed > 21 means we've jumped
max_safe_distance = 2000  # After this distance the yeti appears
post_route_distance = 1020  # The post-route stretch is 1000 on
new_route_delta = 400  # When you choose a route (slalom etc), distance jumps from ~30 to ~500-1200
missed_turn_threshold = 499 # Missing a turn in slalom/tree slalom deducts 5 seconds.

# Characters that only appear in specific categories of string from SkiFree, so we can tell what string type we have

time_string_indicator = ":"  # Colons only show up in time strings
speed_string_indicator = "m/s"  # "m/s" only shows up in the strings strings
distance_string_indicator = "m"  # "m" alone shows up in distance strings, but we check speed first


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
        exhaust_onetime_text(flavor_text)
    write_text(chosen_text)

def exhaust_onetime_text(flavor_text):
    for i in range(len(novelvars.flavor_strings)):
        if novelvars.flavor_strings[i]["text"] == flavor_text["text"]:
            novelvars.flavor_strings[i]["usable"] = False
            break

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
        time = extract_time(text)
        time_delta = abs(novelvars.last_time - time)
        if novelvars.post_ski:
            time_text = ("I lost track of time somewhere around %s. " % (text))
            time_text += get_tailored_text("aftertime")["text"]
        else:
            time_text = ("I must have been out here something like %s. " % (text))
            time_text += get_tailored_text("time")["text"]
        update_time_state(time, time_delta)
        if time_delta > missed_turn_threshold and novelvars.on_route:
            time_text += get_tailored_text("missedturn")["text"]
        return time_text

def extract_time(text):
    return int(text.replace(":", "").replace(".", ""))

def update_time_state(time, delta):
    novelvars.last_time = time
    novelvars.last_time_delta = delta
    if time > 0:
        novelvars.on_route = True
    if delta == 0:
        novelvars.on_route = False
        novelvars.post_ski = True

def get_speed_text(text):
    speed = get_skifree_number(text)
    update_speed_state(speed)
    if check_crash():
        speed_text = ((random.choice(novelvars.crash_preambles)) + get_tailored_text("crash")["text"])
        speed_text += roll_for_extra_text("crash2", speed_text)
        return speed_text
    elif speed == 0:
        speed_text = get_tailored_text("stopped")["text"]
        speed_text += roll_for_extra_text("stopped2", speed_text)
        return speed_text
    elif speed > max_ground_speed:
        speed_text = get_tailored_text("airborne")["text"]
        speed_text += roll_for_extra_text("airborne2", speed_text)
        return speed_text
    else:
        return ("I'm going %s meters per hour." % (str(speed)))


def update_speed_state(speed):
    novelvars.last_speeds.popleft()
    novelvars.last_speeds.append(speed)

# A quick and dirty method of crash detection, using text only. It errs on the side of false negatives.
# Basically: Did our speed go from normal to 0 suddenly, and did we stop moving?
def check_crash():
    return (abs(novelvars.last_speeds[0] - novelvars.last_speeds[2]) > 7 and novelvars.last_distance_delta == 0)


def get_distance_text(text):
    distance = get_skifree_number(text)
    distance_delta = novelvars.last_distance - distance
    update_distance_state(distance, distance_delta)
    distance_text = ("I've gone %s meters now." % (str(distance)))
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
        style_text += roll_for_extra_text("bad2", style_text)
    elif style > 0:
        style_text += get_tailored_text("good")["text"]
        style_text += roll_for_extra_text("good2", style_text)
    else:
        style_text += get_tailored_text("noscore")["text"]
    style_text += "\n"
    return style_text


def get_skifree_number(text):
    text = text.strip().strip("m/s").strip("m")
    if text != "0" and text != "00":  # check for possible strings of just 0
        return int(text.lstrip("0"))
    else:
        return int(text)


def get_tailored_text(tag):
    while True:
        filtered_text = [text for text in novelvars.flavor_strings if tag in text["tags"]]
        tailored_text = random.choice(filtered_text)
        if not tailored_text["usable"]:
            continue
        if "onetime" in tailored_text["tags"]:
            exhaust_onetime_text(tailored_text)
        break
    return tailored_text


def roll_for_extra_text(specific_tag, repeatable_text=None):
    extra_text_roll = random.randint(0, 100)
    if second_text_chance > extra_text_roll:
        extra_text = get_tailored_text(specific_tag)["text"]
        if repeatable_text and repeatable_text == extra_text:
            return ""
        else: # needs 100000% more refactoring.
            repeatable_text = extra_text
            extra_text_roll = random.randint(0, 100)
            if third_text_chance > extra_text_roll:
                third_text = get_tailored_text(specific_tag)["text"]
                if repeatable_text != third_text:
                    extra_text += (" " + third_text)
            repeatable_text = extra_text
            extra_text_roll = random.randint(0, 100)
            if fourth_text_chance > extra_text_roll:
                fourth_text = get_tailored_text(specific_tag)["text"]
                if repeatable_text != fourth_text:
                    extra_text += (" " + fourth_text)
            return (" " + extra_text)
    else:
        return ""


def print_yeti_text():
    yeti_text = get_tailored_text("yeti")
    yeti_roll = random.randint(0, yeti_text_roll_bound)
    if yeti_text["probability"] > yeti_roll:
        write_text("\n" + yeti_text["text"] + "\n")
        yeti_text["probability"] -= 1
    else:
        yeti_text["probability"] += 1
