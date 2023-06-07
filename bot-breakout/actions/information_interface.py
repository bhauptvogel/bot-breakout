
import yaml
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_information():
    """
    Loads the information from the information.yml file
    """
    with open('information.yml', encoding="utf8") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)
    return info

def set_game_state(class_, item, data_slot):

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

def get_class_split(class_, info):
    """
    if class_ has '/' -> path to a class
    else -> class_ is a class
    split and go through the path
    """
    if '/' in class_:
        class_split = class_.split('/')
        for i in range(len(class_split)):
            if class_split[i] in info:
                info = info[class_split[i]]
            else:
                return None
    elif class_ in info:
        info = info[class_]
    else:
        return None
    
    return info

def get_base_item(keys, times_asked_about):
    """
    base is the amount of times the user has asked about the class (+1)
    or the highest base that exists (if the user has asked multiple times)
    """

    if 'base_1' not in keys:
        return None
    if 'base_' + str(times_asked_about+1) in keys:
        item = 'base_' + str(times_asked_about+1)
    else:
        highest_base = 0
        for base in keys:
            if base.startswith('base_'):
                if int(base[5:]) > highest_base:
                    highest_base = int(base[5:])
        item = 'base_' + str(highest_base)

    return item

def get_story_information(class_, item, data_slot):
    """
    :param class_: class to get information about (e.g. 'scene_investigation')
    :param item: item of the class (e.g. 'base_1', none means base)
    :param times_asked_about: how many times the user has asked about the class (without item)
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
            
    
    times_asked_about = 0
    if "times_asked_about_" + class_ in data_slot:
        times_asked_about = data_slot["times_asked_about_" + class_]

    # keys in class
    class_keys = []
    for dict in class_data:
        class_keys.append(list(dict.keys())[0])
    
    if item == '' or item is None:
        item = get_base_item(class_keys, times_asked_about)
    
    if item not in class_keys:
        logging.warning(f'item {item} not in keys... ' + ' '.join(class_keys))
        return None
    
    # add 1 to times_asked_about_class_ in data_slot
    if item.startswith('base_'):
        if "times_asked_about_" + class_ in data_slot:
            data_slot["times_asked_about_" + class_] += 1
        else:
            data_slot["times_asked_about_" + class_] = 1

    set_game_state(class_, item, data_slot)
    
    return class_data[class_keys.index(item)][item]






