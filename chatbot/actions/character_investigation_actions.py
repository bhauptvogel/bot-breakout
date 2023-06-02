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
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        informations = [e['value'] for e in entities if e['entity'] == 'information']
        cowoker_set = False

        if len(entities) > 0 and "group" in entities[0].keys():
            # coworker = [e['value'] for e in entities if e['group'] == 'multiple' and e['entity'] == 'person']
            cowoker_set = True
     
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')


        # If they ask about "her", "him", "it" it uses the "last_spoken"
        if len(informations) == 0 and len(characters) == 0:
            print("In not characters not informations")
            last_spoken_information = None
            if "last_spoken_about_information" in data.keys() and len(data["last_spoken_about_information"]) > 0:
                last_spoken_information = data["last_spoken_about_information"]

            if "last_spoken_about_character" in data.keys() and len(data["last_spoken_about_character"]) > 0:
                for last_spoken in data["last_spoken_about_character"]:
                    dispatcher.utter_message(text=helper.get_story_information(f"character_information/{last_spoken}", last_spoken_information, data))
            else:
                dispatcher.utter_message(text=helper.get_story_information(f"character_information/__General__", last_spoken_information, data))

            # TODO: Sorry I already told you everything about X...
        
        # If information about something character-related is asked
        if len(informations) > 0: 
            print("In informations")
            possible_specifications = helper.get_specifications_of_all_subclasses("character_information")
            if "last_spoken_about_character" in data.keys():
                characters = characters if len(characters) > 0 else data["last_spoken_about_character"]
            for info in informations:
                info = "full_name" if info == "last name" or info == "full name" else info

                if info == "relation" or info =="connection":                    
                    if len(characters) != 2:
                        dispatcher.utter_message(text="I don't know what you mean")
                        return [SlotSet("data", data)]
                    
                    dispatcher.utter_message(text=helper.get_story_information("character_information/story_character_relation", f"{characters[0]}_{characters[1]}", data))

                elif info in possible_specifications:
                        
                    if len(characters) > 0:
                        for character in characters:
                            dispatcher.utter_message(text=helper.get_story_information(f"character_information/{character}", info, data))
                            data["last_spoken_about_information"] = informations
                            print(character, info)
                            if info in data["revealed_information"][character].keys():
                                data["revealed_information"][character][info] = True
                        data["last_spoken_about_character"] = characters
                    else:
                        dispatcher.utter_message(text=helper.get_story_information(f"character_information/__General__", info, data))
                        data["last_spoken_about_information"] = informations
                        data["last_spoken_about_character"] = []
                    

                
        #If basic information about character is asked
        if len(characters) > 0 and len(informations) == 0 and not cowoker_set:
            print("In characters > 0 informations < 0 coworker == 0")
            for character in characters:
                dispatcher.utter_message(text=helper.get_story_information(f"character_information/{character}", "", data))
            data["last_spoken_about_character"] = characters
            data["last_spoken_about_information"] = []
        
        if len(informations) == 0 and cowoker_set:
            print("In informations == 0 coworker_set")
            dispatcher.utter_message(text=helper.get_story_information(f"character_information/__General__", "", data))

        

        return [SlotSet("data", data)]