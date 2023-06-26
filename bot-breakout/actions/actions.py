from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled
from datetime import datetime, timedelta
import time
import random
from helpers.timer_check import check_timer, set_timer


class StartGame(Action):
    # def __init__(self):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker: Tracker, domain):
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

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

        if "first_message_sent" not in data.keys():
            dispatcher.utter_message(
                "I..I..I’m shocked. I know this woman - it’s Maria, a journalist... \nI just called the police, because that's what a good citizen does, right? But now I’m not sure if it was the right decision... We are the only people here and it’s my work place. I might be a suspect! The police said they will be here in 10 minutes. When they arrive, we should provide them with valuable hints about a potential suspect who had both motive and access to the crime scene and the murder weapon. \nI'm not sure where to start. Can you help me clear my mind? Maybe we could investigate the body with the note, or I can tell you about my co-workers."
            )

            timestamp = datetime.now()
            timer = timestamp + timedelta(seconds=60)
            #timer = timestamp + timedelta(seconds=420)
            updated_timestamp = timer.timestamp()

            if "timer" not in data.keys():
                data['timer'] = updated_timestamp
            if "timercount" not in data.keys():
                data['timercount'] = 1
        else:
            dispatcher.utter_message(
                "This whole situation is really aweful for a date, but I think we are doing good! Let’s solve this mystery and find out who the murderer is! We could talk about my coworkers or investigate the room."
            )

        data["first_message_sent"] = True

        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))

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
