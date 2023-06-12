from . import information_interface as ii


def get_story_characters():
    keys = ii.load_information()["character_information"].keys()
    keys = list(keys)
    keys.remove("__General__")
    return keys

def get_story_characters_information():
    """
    Returns a dictionary with all characters as keys and a list of all their information as values.
    """
    output = {}
    story_character_information = ii.load_information()["character_information"]
    for character in story_character_information.keys():
        character_information_dict = story_character_information[character]
        if character not in output.keys():
            output[character] = []
        for info_list in character_information_dict:
            specific_information = info_list.keys()
            specific_information = list(specific_information)[0]
            if not specific_information.startswith("base_"):
                output[character].append(specific_information)
    return output

def get_story_objects():
    output = []
    story_objects_dict = ii.load_information()["scene_investigation"]
    for object in story_objects_dict:
        keys = object.keys()
        obj = list(keys)[0]
        if not obj.startswith("base_"):
            output.append(obj)

    return output


def get_most_similar_person(character):
        """
        Returns the most similar character from the story to the given character. 
        (if the user did not enter a character from the story)
        """
        def levenshtein_distance(string1, string2):
            if len(string1) > len(string2):
                string1, string2 = string2, string1
            distances = range(len(string1) + 1)
            for index2, char2 in enumerate(string2):
                new_distances = [index2 + 1]
                for index1, char1 in enumerate(string1):
                    if char1 == char2:
                        new_distances.append(distances[index1])
                    else:
                        new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
                distances = new_distances
            return distances[-1]
        
        most_similar_character = ""
        most_similar_character_similarity = 100
        for story_character in get_story_characters():
            similarity = levenshtein_distance(character, story_character)
            if similarity < most_similar_character_similarity:
                most_similar_character = story_character
                most_similar_character_similarity = similarity
        
        if most_similar_character_similarity >= 3:
            return f"Did you mean {most_similar_character}?"
        else:
            return ""