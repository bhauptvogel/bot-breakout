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

        story_characters = {"Kira" : {1: "Somehow yes, she is part of the staff. Every staff member has excess to the rides."},
                            "Patrick": {1: "He could have had access, since he’s the director of the amusement park, but I’m not sure if he knows how to stop the rollercoaster."},
                            "Victor": {1: "He shouldn’t have access since he doesn’t work here, but who knows if he found another way in."},
                            "Anna": {1: "She doesn’t have access and even if she had, she would not know how to control the machines."}
                            }

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')

        return [SlotSet("data", data)]
