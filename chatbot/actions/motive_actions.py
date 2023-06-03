from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import helper

class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = helper.INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')

        # check if the person asked for is suspect or victim
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        # set character to last_spoken_about if empty (if user asks about "her", "him", "it")
        if len(characters) == 0:
            if "last_spoken_about_character" in data:
                characters = data["last_spoken_about_character"]
            else:
                dispatcher.utter_message(text=("Who do you mean?"))
                return [SlotSet("data", data)]
            
        # Todo: If user enters a name that is not in our story
        
        for character in characters:
            dispatcher.utter_message(text=helper.get_story_information(f"motive/{character}", "", data, f"{character}/motive"))
            
        data["last_spoken_about_character"] = characters


        return [SlotSet("data", data)]
