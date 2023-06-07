from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random
from . import information_interface as ii

class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def utter_relation(self, dispatcher, characters, data):
        if len(characters) != 2:
            dispatcher.utter_message(text="I don't know what you mean")
        else:
            dispatcher.utter_message(text=ii.get_story_information("story_character_relation", f"{characters[0]}_{characters[1]}", data, fallback="I don't quite understand. Do you want to know a relation between two persons? Please be more specific."))
            data["last_spoken_about_information"] = []
            data["last_spoken_about_character"] = []
    
    def utter_specific_information(self, dispatcher, characters, informations, data):
        # set character to last_spoken_about if empty (if user asks about "her", "him", "it")
        characters = characters if "last_spoken_about_character" not in data.keys() or len(characters) > 0 else data["last_spoken_about_character"]
        for info in informations:
            if info == "relation" or info =="connection":  
                self.utter_relation(dispatcher, characters, data)                 
            else: 
                if info == "last name" or info == "full name":
                    info = "full_name"

                if len(characters) == 0:
                    dispatcher.utter_message(text=ii.get_story_information(f"character_information/__General__", info, data, fallback="I don't understand that or don't have that information."))
                    data["last_spoken_about_information"] = informations
                    return
             
                for character in characters:
                    dispatcher.utter_message(text=ii.get_story_information(f"character_information/{character}", info, data, fallback=f"I don't have that information about {character}"))
                    data["last_spoken_about_information"] = informations
                    
                data["last_spoken_about_character"] = characters

    def utter_base_information(self, dispatcher, characters, data):
        for character in characters:
            dispatcher.utter_message(text=ii.get_story_information(f"character_information/{character}", "", data, fallback=f"I don't know who you're talking about"))
        data["last_spoken_about_character"] = characters
        data["last_spoken_about_information"] = []

        
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


        # set character and information to last_spoken_about if empty (if user asks about "her", "him", "it")
        if len(informations) == 0 and len(characters) == 0:
            if "last_spoken_about_information" in data.keys() and len(data["last_spoken_about_information"]) > 0:
                informations = data["last_spoken_about_information"]
            if "last_spoken_about_character" in data.keys() and len(data["last_spoken_about_character"]) > 0:
                characters = data["last_spoken_about_character"]
        
        if len(informations) > 0: 
            self.utter_specific_information(dispatcher, characters, informations, data)   
        elif len(entities) > 0 and "group" in entities[0].keys():
            # If all coworkers are asked 
            characters = ["__General__"]
            self.utter_base_information(dispatcher, characters, data)
        elif len(characters) > 0 and len(informations) == 0:
            self.utter_base_information(dispatcher, characters, data)

        

        return [SlotSet("data", data)]