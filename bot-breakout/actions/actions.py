from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled
from datetime import datetime, timedelta
import time
import random
from utils.timer_check import check_timer, set_timer
from utils.blocked_message import get_blocked_message


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
            "action_cabin_start": "",
            "action_set_reminder": "",
            "action_react_to_reminder": "",
            "action_you_cannot_leave": "",
            "action_ask_about_mika": "",
            "action_who_is_the_murderer": "",
            "action_cabin_validation": "",
        }

        if "blocked" not in data.keys():
            data["blocked"] = blocked

        if "first_message_sent" not in data.keys():
            dispatcher.utter_message(
                "I..I..I’m shocked. I know this woman - it’s Maria, a journalist... \nI just called the police, because that's what a good citizen does, right? But now I’m not sure if it was the right decision... We are the only people here and it’s my work place. I might be a suspect! The police said they will be here in 10 minutes. When they arrive, we should provide them with valuable hints about a potential suspect who had both motive and access to the crime scene and the murder weapon. \nI'm not sure where to start. Can you help me clear my mind? Maybe we could investigate the body with the note, or I can tell you about my co-workers."
            )

            timestamp = datetime.now()
            timer = timestamp + timedelta(seconds=20)
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


class UserWantsToLeave(Action):
    def name(self) -> Text: 
        return "action_you_cannot_leave"
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        if "blocked" in data and data["blocked"][self.name()] != "":
            dispatcher.utter_message(text=get_blocked_message(data,data["blocked"][self.name()]))
            return []

        sentences = [
            "You can’t leave before the police arrive in a few minutes! We need to find hints together, so they don’t think we two did it. Should we investigate or talk?",
            "This is not possible! The murderer could still be walking around, we should wait until the police arrive in a few minutes. I think we should investigate the situation more."
        ]

        dispatcher.utter_message(text= random.choice(sentences))

        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))

        return []


class AskAboutMika(Action):
    def name(self) -> Text: 
        return "action_ask_about_mika"
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        if "blocked" in data and data["blocked"][self.name()] != "":
            dispatcher.utter_message(text=get_blocked_message(data,data["blocked"][self.name()]))
            return []

        dispatcher.utter_message(text="As you already know, I work here at the amusement park. I'm part of the marketing team and we're currently working on a new marketing campaign, since we recently built a new large rollercoaster in our park and we hope to attract more people to come here.")

        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))

        return []


class WhoIsTheMurderer(Action):
    def name(self) -> Text: 
        return "action_who_is_the_murderer"
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        if "blocked" in data and data["blocked"][self.name()] != "":
            dispatcher.utter_message(text=get_blocked_message(data,data["blocked"][self.name()]))
            return []

        sentences = [
            "I don't know who the murderer could be. Let's collect some more hints together, to find out who did it.",
            "I have no clue at the moment. Let's collect some more hints together, to find out who killed Maria."
        ]

        dispatcher.utter_message(text= random.choice(sentences))

        if check_timer(data):
            dispatcher.utter_message(text=set_timer(data))

        return []