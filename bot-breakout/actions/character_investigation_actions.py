from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random
from . import information_interface as ii
from . import helper_functions as helper

class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def utter_relation(self, dispatcher, characters, data):
        if len(characters) != 2:
            dispatcher.utter_message(text="I don't know what you mean. Please specify two characters if you want to know about their relation.")
        else:
            dispatcher.utter_message(text=ii.get_story_information("story_character_relation", f"{characters[0]}_{characters[1]}", data))
    
    def utter_specific_information(self, dispatcher, characters, informations, data):
        for info in informations:
            if info == "relation" or info =="connection":  
                self.utter_relation(dispatcher, characters, data)                 
            else: 
                if info == "last name" or info == "full name":
                    info = "full_name"

                if len(characters) == 0:
                    if info not in helper.get_story_characters_information()["__General__"]:
                        dispatcher.utter_message(text=f"I don't know anything about the {info}!")
                    else:
                        characters = ["__General__"]
             
                for character in characters:
                    if info not in helper.get_story_characters_information()[character]:
                        dispatcher.utter_message(text=f"I don't know anything about the {info} of {character}!")
                    else:
                        dispatcher.utter_message(text=ii.get_story_information(f"character_information/{character}", info, data))

    def utter_base_information(self, dispatcher, characters, data):
        for character in characters:
            dispatcher.utter_message(text=ii.get_story_information(f"character_information/{character}", "", data))
    
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        informations = [e['value'] for e in entities if e['entity'] == 'information']


        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')


        if len(entities) > 0 and "group" in entities[0].keys():
            # if all coworkers are asked 
            characters = ["__General__"]
        else:
            # if user asks about a character that is not in the story
            for character in characters:
                if character not in helper.get_story_characters():
                    dispatcher.utter_message(text=f"I don't know who {character} is. {helper.get_most_similar_person(character)}")
                    return [SlotSet("data", data)]

        # if user wants to know something specific (about a character)
        if len(informations) > 0:
            self.utter_specific_information(dispatcher, characters, informations, data)   
            return [SlotSet("data", data)]
    
        # if user is not specifying a character
        if len(characters) == 0:
            dispatcher.utter_message(text="If you want to know something about a character, please specify who you mean.")
            return [SlotSet("data", data)]
        

        self.utter_base_information(dispatcher, characters, data)
        return [SlotSet("data", data)]