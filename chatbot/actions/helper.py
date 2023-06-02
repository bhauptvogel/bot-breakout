
import yaml



def get_specifications_of_all_subclasses(class_):

    with open('information.yml', encoding="utf8") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)

    possible_specifications = []

    for i in info[class_]:
        possible_specifications.append(get_specifications_of_class(f"{class_}/{i}"))


    possible_specifications = [item for sublist in possible_specifications for item in sublist]
    possible_specifications = [x for x in possible_specifications if not x.startswith("base_")]
    possible_specifications = list(set(possible_specifications))
    return possible_specifications


def get_specifications_of_class(class_):


    with open('information.yml', encoding="utf8") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)

    # if class_ has '/' -> path to a class
    # split and go through the path
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

    # list of keys in class
    keys = []
    for dict in info:
        keys.append(list(dict.keys())[0])

    return keys

def get_story_information(class_, specification, data_slot=None):
    """
    :param class_: class to get information about (e.g. 'scene_investigation')
    :param specification: specification of the class (e.g. 'base_1', none means base)
    :param times_asked_about: how many times the user has asked about the class (without specification)
    :return: utter message that the chatbot should say
    """
            

    with open('information.yml', encoding="utf8") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)

    # if class_ has '/' -> path to a class
    # split and go through the path
    if '/' in class_:
        class_split = class_.split('/')
        print("class_split")
        for i in range(len(class_split)):
            if class_split[i] in info:
                info = info[class_split[i]]
            else:
                return None
    elif class_ in info:
        info = info[class_]
    else:
        return None
    
    times_asked_about = 0
    if data_slot is not None and "times_asked_about_" + class_ in data_slot:
        times_asked_about = data_slot["times_asked_about_" + class_]

    # list of keys in class
    keys = []
    for dict in info:
        keys.append(list(dict.keys())[0])
    
    # if specification is not given -> get the base
    # base is the amount of times the user has asked about the class
    # or the highest base that exists (if the user has asked multiple times)
    if specification == '' or specification is None:
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

        print(specification)
    
    if specification not in keys:
        print('specification not in keys...')
        return None
    
    # add 1 to times_asked_about_class_ in data_slot
    if data_slot is not None:
        if "times_asked_about_" + class_ in data_slot:
            data_slot["times_asked_about_" + class_] += 1
        else:
            data_slot["times_asked_about_" + class_] = 1
    

    return info[keys.index(specification)][specification]


print(get_story_information('story_character_relation', 'Patrick_Anna'))


