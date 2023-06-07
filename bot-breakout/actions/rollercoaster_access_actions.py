from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random
from . import helper

class AccessToRollerCoaster(Action):
    def name(self) -> Text:
        return "action_access_to_roller_coaster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        if len(characters) == 0:
            if "last_spoken_about_character" in data:
                characters = data["last_spoken_about_character"]
            else:
                dispatcher.utter_message(text=("I don't know who you're talking about"))
                return [SlotSet("data", data)]
            
        # Todo: If user enters an name that is not in our story
    
        for character in characters:
            dispatcher.utter_message(text=helper.get_story_information(f"access/{character}", "", data))
        
        data["last_spoken_about_character"] = characters


        return [SlotSet("data", data)]
