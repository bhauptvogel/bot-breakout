from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random

from actions.actions import INITIAL_DATA_OBJECT

class AccessToRollerCoaster(Action):
    def name(self) -> Text:
        return "action_access_to_roller_coaster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')

        story_characters_access = {"Kira" : {1 : "Kira works at the rollercoaster and has backstage access so yes she had access"},
                            "Patrick": {1 : "Since he is the owner of the rollercoaster he definetly had access to it, so he could have done something..."},
                            "Victor": {1 : "Victor doesn't work at the rollercoaster, and since access to the backstage area requires specific keys, it's highly unlikely that he could have gotten back there."},
                            "Anna": {1 : "Anna doesn't work here so she doesn't have the keys she requires to access backstage. So it was not possible for her to get there"}}

        
        if len(characters) > 0:
            print("In characters > 0 informations < 0 coworker == 0")
            for story_character in story_characters_access:
                if story_character in characters:
                    data["last_spoken_about_character"].append(story_character)
                    if "times_asked_about_access" + story_character not in data:
                        data["times_asked_about_access" + story_character] = 1
                        dispatcher.utter_message(text=(story_characters_access[story_character][1]))
                    else:
                        data["times_asked_about_access" + story_character] += 1
                        dispatcher.utter_message(text=("Like I told you: " + story_characters_access[story_character][1]))
        elif "last_spoken_about_character" in data.keys() and data["last_spoken_about_character"] != []:
            for story_character in story_characters_access:
                if story_character in data["last_spoken_about_character"]:
                    if "times_asked_about_access" + story_character not in data:
                        data["times_asked_about_access" + story_character] = 1
                        dispatcher.utter_message(text=(story_characters_access[story_character][1]))
                    else:
                        data["times_asked_about_access" + story_character] += 1
                        dispatcher.utter_message(text=("Like I told you: " + story_characters_access[story_character][1]))
        else:
            dispatcher.utter_message(text=("I don't know who you're talking about"))


        return [SlotSet("data", data)]
