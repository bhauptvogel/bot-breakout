
import yaml
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def load_story_yml():
    """
    Loads the information from the information.yml file
    """
    with open('story_information.yml', encoding="utf8") as f:
        story_yml = yaml.load(f, Loader=yaml.FullLoader)
    return story_yml

def set_game_state(class_: str, item: str, data_slot: dict):

    st = f"{class_}/{item}"
    keys = st.split('/')
    if "story_state" not in data_slot:
        data_slot["story_state"] = {}
    d = data_slot["story_state"]


    for index, key in enumerate(keys):
        if key in d:
            d = d[key]
        elif index == len(keys)-1:
            d[key] = True
        else:
            d[key] = {}
            d = d[key]

    logging.debug("Game state was set: " + str(data_slot["story_state"]))

def get_class_split(class_: str, story_dict: dict):
    """
    if class_ has '/' -> path to a class
    else -> class_ is a class
    split and go through the path
    """
    if '/' in class_:
        class_split = class_.split('/')
        for i in range(len(class_split)):
            if class_split[i] in story_dict:
                story_dict = story_dict[class_split[i]]
            else:
                return None
    elif class_ in story_dict:
        story_dict = story_dict[class_]
    else:
        return None
    
    return story_dict

def get_base_item(story_keys: list, class_: str,  data_slot: dict):
    """
    Get the base item of a class from the game state
    """
    if "story_state" not in data_slot:
        data_slot["story_state"] = {}
        return "base_1"
    
    game_state_class_split = get_class_split(class_, data_slot["story_state"])
    if game_state_class_split is None:
        return "base_1"

    game_state_class_keys = game_state_class_split.keys()
    game_state_class_keys = list(game_state_class_keys)

    for key in story_keys:
        if key.startswith('base_'):
            if key not in game_state_class_keys:
                return key
            
    # return highest base in game_state_class_keys
    highest_base = 0
    for key in game_state_class_keys:
        if key.startswith('base_'):
            highest_base = max(highest_base, int(key.split('_')[1]))
    return "base_" + str(highest_base)
    

def get_story_information(class_, item, data_slot):
    """
    :param class_: class to get information about (e.g. 'scene_investigation')
    :param item: item of the class (e.g. 'base_1', none means base)
    :param data_slot: data_slot of the each user
    :return: utter message that the chatbot should say
    """
    
    logging.info("get_story_information: " + class_ + ", item: " + item)

    story_dict = load_story_yml()
    class_story_data = get_class_split(class_, story_dict)


    if class_story_data is None:
        logging.error(f"get_story_information: class_data is None! class:{class_}, item:{item}")
        return None
    if data_slot is None:
        logging.error("get_story_information: data_slot is None")
        return None

    # keys in class
    keys_in_class_story = []
    for dict in class_story_data:
        keys_in_class_story.append(list(dict.keys())[0])
    
    if item == '' or item is None:
        item = get_base_item(keys_in_class_story, class_, data_slot)
    
    if item not in keys_in_class_story:
        logging.warning(f'item {item} not in keys... ' + ' '.join(keys_in_class_story))
        return None

    set_game_state(class_, item, data_slot)
    
    return class_story_data[keys_in_class_story.index(item)][item]


def get_story_characters():
    keys = load_story_yml()["character_information"].keys()
    keys = list(keys)
    keys.remove("__General__")
    return keys

def get_story_characters_information():
    """
    Returns a dictionary with all characters as keys and a list of all their information as values.
    """
    output = {}
    story_character_information = load_story_yml()["character_information"]
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
    story_objects_dict = load_story_yml()["scene_investigation"]
    for object in story_objects_dict:
        keys = object.keys()
        obj = list(keys)[0]
        if not obj.startswith("base_"):
            output.append(obj)

    return output