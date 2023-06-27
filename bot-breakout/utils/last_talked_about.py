from utils import information_interface as ii

def get_last_talked_about_character(data):
    # TODO: Check gender of last talked about character (if the last talked about character matches with the pronoun the user is using)
    if "last_talked_about_character" not in data:
        data["last_talked_about_character"] = ""
    return data["last_talked_about_character"]

def set_last_talked_about_character(character, data):
    if character in ii.get_story_characters():
        data["last_talked_about_character"] = character
    else:
        data["last_talked_about_character"] = ""

def reset_last_talked_about_character(data):
    data["last_talked_about_character"] = ""