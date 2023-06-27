from utils import information_interface as ii

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

def get_most_similar_person(character):
    """
    Returns the most similar character from the story to the given character. 
    (if the user did not enter a character from the story)
    """
    
    
    most_similar_character = ""
    most_similar_character_similarity = 100
    for story_character in ii.get_story_characters():
        similarity = levenshtein_distance(character, story_character)
        if similarity < most_similar_character_similarity:
            most_similar_character = story_character
            most_similar_character_similarity = similarity
    
    if most_similar_character_similarity >= 3:
        return f"Maybe you meant {most_similar_character}. Please specify the name of the person."
    else:
        return ""
        