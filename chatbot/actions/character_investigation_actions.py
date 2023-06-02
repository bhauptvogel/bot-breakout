from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random
from . import helper

from actions.actions import INITIAL_DATA_OBJECT


class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def utter_relation(self, dispatcher, characters, data):
        if len(characters) != 2:
            dispatcher.utter_message(text="I don't know what you mean")
        else:
            dispatcher.utter_message(text=helper.get_story_information("story_character_relation", f"{characters[0]}_{characters[1]}", data))
            
    
    def utter_specific_information(self, dispatcher, characters, informations, data):
        characters = characters if "last_spoken_about_character" not in data.keys() or len(characters) > 0 else data["last_spoken_about_character"]
        for info in informations:
            if info == "relation" or info =="connection":  
                self.utter_relation(dispatcher, characters, data)                 
            else: 
                info = "full_name" if info == "last name" or info == "full name" else info
             
                for character in characters:
                    dispatcher.utter_message(text=helper.get_story_information(f"character_information/{character}", info, data, f"{character}/{info}"))
                    data["last_spoken_about_information"] = informations
                    
                data["last_spoken_about_character"] = [] if len(characters) == 0 else characters

    def utter_base_information(self, dispatcher, characters, data):
        for character in characters:
            dispatcher.utter_message(text=helper.get_story_information(f"character_information/{character}", "", data, f"{character}/personal_information"))
        data["last_spoken_about_character"] = characters
        data["last_spoken_about_information"] = []

        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        informations = [e['value'] for e in entities if e['entity'] == 'information']

     
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')


        # If they ask about "her", "him", "it" -> information and character is last spoken about
        if len(informations) == 0 and len(characters) == 0:
            if "last_spoken_about_information" in data.keys() and len(data["last_spoken_about_information"]) > 0:
                informations = data["last_spoken_about_information"]
            if "last_spoken_about_character" in data.keys() and len(data["last_spoken_about_character"]) > 0:
                characters = data["last_spoken_about_character"]
            # TODO: Sorry I already told you everything about X...
        
        # If information about something character-related is asked
        if len(informations) > 0: 
            self.utter_specific_information(dispatcher, characters, informations, data)   
        # If all coworkers are asked     
        elif len(entities) > 0 and "group" in entities[0].keys():
            self.utter_base_information(dispatcher, characters, data)
        # If basic information about character is asked
        elif len(characters) > 0 and len(informations) == 0:
            self.utter_base_information(dispatcher, characters, data)

        

        return [SlotSet("data", data)]