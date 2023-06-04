from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import helper

class Hint(Action):
    def name(self) -> Text:
        return "action_give_hint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = helper.INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')

        dispatcher.utter_message("Todo: HINT")

        


        return [SlotSet("data", data)]
