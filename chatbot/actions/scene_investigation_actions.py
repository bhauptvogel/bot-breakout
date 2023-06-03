
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import helper
        

class SceneInvestigation(Action):
    def name(self) -> Text:
        return "action_scene_investigation"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = helper.INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')
        
        entities = tracker.latest_message['entities']
        objects = [e['value'] for e in entities if e['entity'] == 'object']

        if len(objects) == 0:
            dispatcher.utter_message(text=helper.get_story_information("scene_investigation", "", data))

        for obj in objects:
            dispatcher.utter_message(text=helper.get_story_information("scene_investigation", obj, data, f"Objects/{obj}"))

        # Todo: If user enters an object that is not in our story
        
        return [SlotSet("data", data)]