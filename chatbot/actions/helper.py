
import yaml
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def set_revealed_information(data_slot, revealed_information):
    """
    Sets the revealed_information in data_slot to True
    """
    keys = revealed_information.split('/')
    d = data_slot["revealed_information"]

    for key in keys[:-1]:
        if key in d:
            d = d[key]
        else:
            return

    if keys[-1] in d:
        d[keys[-1]] = True

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

def get_base_specification(keys, times_asked_about):
    """
    base is the amount of times the user has asked about the class (+1)
    or the highest base that exists (if the user has asked multiple times)
    """

    if 'base_1' not in keys:
        return None
    if 'base_' + str(times_asked_about+1) in keys:
        specification = 'base_' + str(times_asked_about+1)
    else:
        highest_base = 0
        for base in keys:
            if base.startswith('base_'):
                if int(base[5:]) > highest_base:
                    highest_base = int(base[5:])
        specification = 'base_' + str(highest_base)

    return specification

def get_story_information(class_, specification, data_slot=None, revealed_information=None):
    """
    :param class_: class to get information about (e.g. 'scene_investigation')
    :param specification: specification of the class (e.g. 'base_1', none means base)
    :param times_asked_about: how many times the user has asked about the class (without specification)
    :return: utter message that the chatbot should say
    """
    
    logging.info("get_story_information: " + class_ + " " + specification)

    with open('information.yml', encoding="utf8") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)

    info = get_class_split(class_, info)

    if info is None:
        return None
    
    times_asked_about = 0
    if data_slot is not None and "times_asked_about_" + class_ in data_slot:
        times_asked_about = data_slot["times_asked_about_" + class_]

    # list of keys in class
    keys = []
    for dict in info:
        keys.append(list(dict.keys())[0])
    
    if specification == '' or specification is None:
        specification = get_base_specification(keys, times_asked_about)
    
    if specification not in keys:
        print('specification not in keys...')
        return None
    
    # add 1 to times_asked_about_class_ in data_slot
    if data_slot is not None:
        if "times_asked_about_" + class_ in data_slot:
            data_slot["times_asked_about_" + class_] += 1
        else:
            data_slot["times_asked_about_" + class_] = 1

        if revealed_information:
            set_revealed_information(data_slot, revealed_information)
    

    return info[keys.index(specification)][specification]






