global used_text
used_text = None

global words
words = 0

global skinovel
skinovel = open("skinovel.txt", "w+")

starter_text = {
    "Time:": "I told myself I wasn't going to ski long.",
    "Dist:": "Or ski far.",
    "Speed:": "Or ski too fast.",
    "Style:": "I don't know how to ski."
}

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
    return ("I'm going %s." %(text))

def get_distance_text(text):
    distance = get_skifree_number(text)
    if distance > 2000:
        return "I've gone too far..."
    return ("I've gone %s meters." %(text))

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
    if text != "0" and text != "00": # strip leading zeroes if any
        return int(text.lstrip("0"))
    else:
        return int(text)