from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled
from utils.timer_check import check_timer, set_timer
from utils.blocked_message import get_blocked_message

import random
from utils import information_interface as ii
from utils.string_similarity import get_most_similar_person, levenshtein_distance
from utils.last_talked_about import get_last_talked_about_character, set_last_talked_about_character, reset_last_talked_about_character
from utils.end_of_game import guess_murderer
from utils.formatting import utter

class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def utter_base_information(self, dispatcher, characters, data):
        for character in characters:
            if character is not "__General__" and character not in ii.get_story_characters():
                    utter(dispatcher, text=f"I don't know who {character} is. {get_most_similar_person(character)}")
                    reset_last_talked_about_character(data)
                    return
            utter(dispatcher, text=ii.get_story_information(f"character_information/{character}", "", data))
            set_last_talked_about_character(character, data)

    def utter_specific_information(self, dispatcher, character, info, data):
        if info not in ii.get_story_characters_information()[character]:
            if character == "__General__":
                utter(dispatcher, text=f"I don't know anything about the {info}!")
            else:
                utter(dispatcher, text=f"I don't know anything about the {info} of {character}!")
        else:
            utter(dispatcher, text=ii.get_story_information(f"character_information/{character}", info, data))

    def utter_relation(self, dispatcher, characters, data):
        if len(characters) != 2:
            utter(dispatcher, text="I don't know what you mean.🫠 Please specify two characters names if you want to know about their relation.")
        else:
            utter(dispatcher, text=ii.get_story_information("story_character_relation", f"{characters[0]}_{characters[1]}", data))

    def process_informations(self, dispatcher, characters, informations, data):
        for info in informations:
            if info == "relation" or info =="connection":
                self.utter_relation(dispatcher, characters, data)
            else:
                if info == "last name" or info == "full name":
                    info = "full_name"

                if len(characters) == 0:
                    self.utter_specific_information(dispatcher, "__General__", info, data)

                for character in characters:
                    if character not in ii.get_story_characters():
                        utter(dispatcher, text=f"I don't know who {character} is.🫠 {get_most_similar_person(character)}")
                        return
                    self.utter_specific_information(dispatcher, character, info, data)

    def hint_character_to_talk_about(self, data):
        if "story_state" not in data or "character_information" not in data["story_state"]:
            return "I can tell you about Victor, Anna, Patrick, Maria and Kira."
        
        discussed_characters = data["story_state"]["character_information"]
        discussed_characters = list(discussed_characters.keys())

        characters_to_talk_about = []
        for character in ii.get_story_characters():
            if character not in discussed_characters:
                characters_to_talk_about.append(character)

        if len(characters_to_talk_about) == 0:
            return ""
        elif len(characters_to_talk_about) == 1:
            return f"Let's maybe talk about {characters_to_talk_about[0]}."
        elif len(characters_to_talk_about) == 2:
            return f"We still have not talked about {characters_to_talk_about[0]} and {characters_to_talk_about[1]}."
        else:
            return f"We can talk about {', '.join(characters_to_talk_about[:-1])} or {characters_to_talk_about[-1]}."

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []

        entities = tracker.latest_message['entities']
        informations = [e['value'] for e in entities if e['entity'] == 'information']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        if "blocked" in data.keys() and data["blocked"][self.name()] != "":
            if data["blocked"][self.name()] == "end_of_game_blocked":
                names_in_message = tracker.latest_message['text'].split(" ")
                if len(names_in_message) > 2:
                    utter(dispatcher, text=get_blocked_message(data,data["blocked"][self.name()]))
                for name in names_in_message:
                    for story_character in ii.get_story_characters():
                        if name == story_character or levenshtein_distance(name, story_character) <= 2:
                            utter(dispatcher, text=guess_murderer(data, story_character))
                            return [SlotSet("data", data)]
            utter(dispatcher, text=get_blocked_message(data,data["blocked"][self.name()]))
            return [SlotSet("data", data)]

        if len(characters) == 0:
            last_talked_about = get_last_talked_about_character(data)
            if last_talked_about != "":
                characters.append(last_talked_about)
            elif len(informations) == 0:
                utter(dispatcher, text=f"If you want to know something about a character, please specify who you mean.😇 <br>{self.hint_character_to_talk_about(data)}")
                reset_last_talked_about_character(data)
                return [SlotSet("data", data)]


        if len(entities) > 0 and "group" in entities[0].keys() and entities[0]["group"] == "multiple":
            # if all coworkers are asked
            characters = ["__General__"]

        # if user wants to know something specific (about a character)
        if len(informations) == 0:
            self.utter_base_information(dispatcher, characters, data)
        else:
            self.process_informations(dispatcher, characters, informations, data)
            reset_last_talked_about_character(data)

        if check_timer(data):
            utter(dispatcher, text=set_timer(data))

        return [SlotSet("data", data)]
