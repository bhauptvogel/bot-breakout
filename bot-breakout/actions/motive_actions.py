from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import information_interface as ii
from . import helper_functions as helper
class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        # check if the person asked for is suspect or victim
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        # if user is not specifiing a character
        if len(characters) == 0:
            dispatcher.utter_message(text="If you want to know the motive about a certain character, let me know who you want to know about.")
            return [SlotSet("data", data)]
        
        for character in characters:
            # if user asks about a character that is not in the story
            if character not in ii.get_story_characters():
                dispatcher.utter_message(text=f"I don't know who {character} is. {helper.get_most_similar_person(character)}")
            else:
                dispatcher.utter_message(text=ii.get_story_information(f"motive/{character}", "", data))
        
            
            

        return [SlotSet("data", data)]
