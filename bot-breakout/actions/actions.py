from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled
from datetime import datetime, timedelta
import time
import random





class StartGame(Action):
    # def __init__(self):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker: Tracker, domain):
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
    
        timestamp = datetime.now()
        timer = timestamp + timedelta(seconds=20)
        #timer = timestamp + timedelta(seconds=420)
        updated_timestamp = timer.timestamp()

        if "timer" not in data.keys():
            data['timer'] = updated_timestamp
        if "timercount" not in data.keys():
            data['timercount'] = 1
        
        blocked = {
            "action_character_investigation": "",
            "action_user_guess": "",
            "action_give_hint": "",
            "action_tell_motive": "",
            "action_overview_of_the_state": "",
            "action_access_to_roller_coaster": "",
            "action_scene_investigation": "",
            "validate_simple_cabin_form": "",
            "action_cabin_end": "",
            "action_cabin_start": ""
        }

        if "blocked" not in data.keys():
            data["blocked"] = blocked

        dispatcher.utter_message(
            "Oh hi! Sorry, I’m just a bit stunned. I know this woman - it's Maria, a journalist... After seeing the dead body, I called the police. Because this is what a good citizen does, right? But now I’m not sure if it was the right decision... We are the only people here and its my work place. I might be a suspect! We have 10 min until the police is here. I should give them some valuable hints about the motive, the access to the crime scene and the murder weapon when they arrive here. But I don’t know where to start. Can you help me clear my mind? We could first investigate the body with the note, or I can tell you about my co-workers."
        )
        
        return [SlotSet("data", data)]
        
    
class ActionReactToReminder(Action):
    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("The police is coming now! What's our guess?")

        return []



