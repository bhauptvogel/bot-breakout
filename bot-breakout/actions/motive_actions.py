from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import information_interface as ii
from helpers.timer_check import check_timer, set_timer

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

        # set character to last_spoken_about if empty (if user asks about "her", "him", "it")
        if len(characters) == 0:
            if "last_spoken_about_character" in data:
                characters = data["last_spoken_about_character"]
            else:
                dispatcher.utter_message(text=("Who do you mean?"))
                return [SlotSet("data", data)]
            
        # Todo: If user enters a name that is not in our story
        
        for character in characters:
            dispatcher.utter_message(text=ii.get_story_information(f"motive/{character}", "", data, fallback="Sorry, I don't know who you're talking about. If you want to know motives for killing Maria, ask for a specific person."))
            
        data["last_spoken_about_character"] = characters

        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))

        return [SlotSet("data", data)]
