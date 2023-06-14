
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import information_interface as ii
from helpers.timer_check import check_timer, set_timer
        

class SceneInvestigation(Action):
    def name(self) -> Text:
        return "action_scene_investigation"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        entities = tracker.latest_message['entities']
        objects = [e['value'] for e in entities if e['entity'] == 'object']

        if len(objects) == 0:
            dispatcher.utter_message(text=ii.get_story_information("scene_investigation", "", data, fallback="Sorry, I don't undestand what you mean. Do you want me to investigate the scene?"))

        for obj in objects:
            objects_inside_cabin = ['body', 'weapon', 'knife', 'note', 'cabin']
            if obj in objects_inside_cabin and not ("cabin_open" in data.keys() and data["cabin_open"] == True):
                obj = "no_access"
            dispatcher.utter_message(text=ii.get_story_information("scene_investigation", obj, data, fallback=f"Sorry, I'm not sure what you mean with {obj}."))


        # TODO: If user enters an object that is not in our story
    
        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))
        
        return [SlotSet("data", data)]


# Validation Form for the cabin pin
class ValidateSimpleCabinForm(FormValidationAction):
        def name(self) -> Text:
            return "validate_simple_cabin_form"

        def validate_cabin_password(
                self,
                slot_value: Any,
                dispacher: CollectingDispatcher,
                tracker: Tracker,
                domain: DomainDict,
        ) -> Dict[Text, Any]:
            if tracker.get_slot('cabin_guess') is None:
                value = 1
            else:
                value = tracker.get_slot('cabin_guess')
            
            print(value)
            
            if tracker.get_slot('cabin_number_guess') is None:
                boolean = False
            else:
                boolean = tracker.get_slot('cabin_number_guess')
        
            if slot_value == "492":
                dispacher.utter_message(text="Yes "+slot_value+" worked. We can enter the cabin.")
                return {"cabin_password": slot_value}
            if slot_value == "989" and not boolean:
                dispacher.utter_message(text="Yes that looks better. This is the right cabin number, sorry for the confusion. Please do the equation with that number but first let me try it with "+slot_value+" ...")
                boolean = True
                value += 1
                return {"cabin_password": None, "cabin_guess": value, "cabin_number_guess": boolean}
 
            if value < 3:
                value += 1
            elif value == 3: 
                dispacher.utter_message(text="Maybe look at the 686 ANOTHER WAY... but let me try first with "+slot_value+" ...")
                value += 1
            elif value == 4:
                value += 1
            elif value == 5:
                if not boolean:
                    dispacher.utter_message(text="Oh I see now... the cabin number is 989 - but first let me try it with "+slot_value+" ...")
                value += 1
            else:
                dispacher.utter_message(text="The pin should be (989 - 7 + 2) / 2. I'll try it first with "+slot_value+" ...")
                value += 1
            
            return {"cabin_password": None, "cabin_guess": value, "cabin_number_guess": boolean}

# End if the pin was right 
class CabinEnd(FormValidationAction):
    def name(self) -> Text:
        return "action_cabin_end"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        ii.set_game_state("scene_investigation", "cabin", data)

        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))

        return [SlotSet("data", data), SlotSet("cabin_open", True)]

