
import yaml
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def load_information():
    """
    Loads the information from the information.yml file
    """
    with open('story_information.yml', encoding="utf8") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)
    return info

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

def get_class_split(class_: str, info_dict: dict):
    """
    if class_ has '/' -> path to a class
    else -> class_ is a class
    split and go through the path
    """
    if '/' in class_:
        class_split = class_.split('/')
        for i in range(len(class_split)):
            if class_split[i] in info_dict:
                info_dict = info_dict[class_split[i]]
            else:
                return None
    elif class_ in info_dict:
        info_dict = info_dict[class_]
    else:
        return None
    
    return info_dict

def get_base_item(keys: list, class_: str,  data_slot: dict):
    """
    Get the base item of a class from the game state
    """
    if "story_state" not in data_slot:
        data_slot["story_state"] = {}
        return "base_1"
    game_state_class_split = get_class_split(class_, data_slot["story_state"])
    if game_state_class_split is None:
        return "base_1"

    game_state_class_split = game_state_class_split.keys()
    game_state_class_split = list(game_state_class_split)

    for key in keys:
        if key.startswith('base_'):
            if key not in game_state_class_split:
                print("return key: " + str(key))
                return key


def get_story_information(class_, item, data_slot):
    """
    :param class_: class to get information about (e.g. 'scene_investigation')
    :param item: item of the class (e.g. 'base_1', none means base)
    :param data_slot: data_slot of the each user
    :return: utter message that the chatbot should say
    """
    
    logging.info("get_story_information: " + class_ + ", item: " + item)

    information_yml = load_information()
    class_data = get_class_split(class_, information_yml)


    if class_data is None:
        logging.error(f"get_story_information: class_data is None! class:{class_}, item:{item}")
        return None
    if data_slot is None:
        logging.error("get_story_information: data_slot is None")
        return None

    # keys in class
    class_keys = []
    for dict in class_data:
        class_keys.append(list(dict.keys())[0])
    
    if item == '' or item is None:
        item = get_base_item(class_keys, class_, data_slot)
    
    if item not in class_keys:
        logging.warning(f'item {item} not in keys... ' + ' '.join(class_keys))
        return None

    set_game_state(class_, item, data_slot)
    
    return class_data[class_keys.index(item)][item]


def get_story_characters():
    keys = load_information()["character_information"].keys()
    keys = list(keys)
    keys.remove("__General__")
    return keys

def get_story_characters_information():
    """
    Returns a dictionary with all characters as keys and a list of all their information as values.
    """
    output = {}
    story_character_information = load_information()["character_information"]
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
    story_objects_dict = load_information()["scene_investigation"]
    for object in story_objects_dict:
        keys = object.keys()
        obj = list(keys)[0]
        if not obj.startswith("base_"):
            output.append(obj)

    return output