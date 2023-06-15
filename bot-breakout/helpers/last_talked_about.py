from actions import information_interface as ii

def get_last_talked_about_character(data):
    return data["last_talked_about_character"]

def set_last_talked_about_character(character, data):
    if character in ii.get_story_characters():
        data["last_talked_about_character"] = character
    else:
        data["last_talked_about_character"] = ""

def reset_last_talked_about_character(data):
    data["last_talked_about_character"] = ""