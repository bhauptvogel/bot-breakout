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

class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def utter_base_information(self, dispatcher, characters, data):
        for character in characters:
            if character is not "__General__" and character not in ii.get_story_characters():
                    dispatcher.utter_message(text=f"I don't know who {character} is. {get_most_similar_person(character)}")
                    reset_last_talked_about_character(data)
                    return
            dispatcher.utter_message(text=ii.get_story_information(f"character_information/{character}", "", data))
            set_last_talked_about_character(character, data)

    def utter_specific_information(self, dispatcher, character, info, data):
        if info not in ii.get_story_characters_information()[character]:
            if character == "__General__":
                dispatcher.utter_message(text=f"I don't know anything about the {info}!")
            else:
                dispatcher.utter_message(text=f"I don't know anything about the {info} of {character}!")
        else:
            dispatcher.utter_message(text=ii.get_story_information(f"character_information/{character}", info, data))

    def utter_relation(self, dispatcher, characters, data):
        if len(characters) != 2:
            dispatcher.utter_message(text="I don't know what you mean. Please specify two characters if you want to know about their relation.")
        else:
            dispatcher.utter_message(text=ii.get_story_information("story_character_relation", f"{characters[0]}_{characters[1]}", data))

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
                        dispatcher.utter_message(text=f"I don't know who {character} is. {get_most_similar_person(character)}")
                        return
                    self.utter_specific_information(dispatcher, character, info, data)


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        entities = tracker.latest_message['entities']
        informations = [e['value'] for e in entities if e['entity'] == 'information']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        if "blocked" in data and data["blocked"][self.name()] != "":
            if data["blocked"][self.name()] == "end_of_game_blocked":
                names_in_message = tracker.latest_message['text'].split(" ")
                if len(names_in_message) > 2:
                    dispatcher.utter_message(text=get_blocked_message(data,data["blocked"][self.name()]))
                for name in names_in_message:
                    for story_character in ii.get_story_characters():
                        if name == story_character or levenshtein_distance(name, story_character) <= 2:
                            dispatcher.utter_message(text=guess_murderer(data, story_character))
                            return [SlotSet("data", data)]
            dispatcher.utter_message(text=get_blocked_message(data,data["blocked"][self.name()]))
            return [SlotSet("data", data)]

        if len(characters) == 0:
            last_talked_about = get_last_talked_about_character(data)
            if last_talked_about != "":
                characters.append(last_talked_about)
            elif len(informations) == 0:
                print(last_talked_about, )
                # TODO: I can tell you about... (all characters the user has not asked about yet) #53
                dispatcher.utter_message(text="If you want to know something about a character, please specify who you mean. I can tell you about Victor, Anna, Patrick and Kira.")
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
            dispatcher.utter_message(text=set_timer(data))

        return [SlotSet("data", data)]
