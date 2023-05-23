# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random


class GiveHint(Action):
    def name(self) -> Text:
        return "action_hint"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        dispatcher.utter_message(text='TODO: Give hint (answer to last question)')
        
        return []
    
class SituationOverview(Action):
    def name(self) -> Text:
        return "action_overview_of_the_state"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        dispatcher.utter_message(text='TODO: Give situation overview')
        
        return []
    
class SceneInvestigation(Action):
    def name(self) -> Text:
        return "action_scene_investigation"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entities = tracker.latest_message['entities']
        objects = [e['value'] for e in entities if e['entity'] == 'object']

        dispatcher.utter_message(text=('TODO: Investigate ' + ', '.join(objects) + '...'))
        
        return []
    
class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        informations = [e['value'] for e in entities if e['entity'] == 'information']
        dispatcher.utter_message(text=('TODO: Investigate characters: ' + ', '.join(characters) + ' / informations: ' + ', '.join(informations) + '...'))
        
        return []


class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entites = tracker.latest_message['entities']
        suspects = [e['value'] for e in entites if e['group'] == 'suspect' and e['entity'] == 'person']
        victim = [e['value'] for e in entites if e['group'] == 'victim' and e['entity'] == 'person']
        dispatcher.utter_message(text='TODO: Tell motive of ' + ', '.join(suspects) + ' for killing ' + ', '.join(victim) + '...')
        
        return []

class AccessToRollerCoaster(Action):
    def name(self) -> Text:
        return "action_access_to_roller_coaster"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        dispatcher.utter_message(text='TODO: Tell access to roller coaster of ' + ', '.join(characters) + '...')
        
        return []