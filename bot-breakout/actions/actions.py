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
from utils.formatting import utter
from utils.game_parameters import GameParams
from utils import information_interface as ii


class StartGame(Action):
    # def __init__(self):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker: Tracker, domain):
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        

        if "blocked" not in data.keys():
            data["blocked"] = {
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
                "action_character_last_seen": "",
            }
        
        if "hint_given" not in data.keys():
            data["hint_given"] = False

        if "first_message_sent" not in data.keys():
            utter(dispatcher,
                "Oh hi, Sorry I’m just shocked. I..I..I know this woman - it’s Maria, a journalist...😨 <br>I just called the police, because that's what a good citizen does, right? But now we should find some hints to not become a suspect ourselves! The police is here in 10 minutes.⏰ When they arrive, we should provide valuable hints about a <b>potential suspect</b> who had both <b>motive and access</b> to the crime scene and the <b>murder weapon</b>. <br>I'm not sure where to start. Can you help me clear my mind?🥺 Maybe we could investigate the room, or I can tell you about my co-workers."
            )

            timestamp = datetime.now()
            timer = timestamp + timedelta(seconds=GameParams.game_time_seconds)
            updated_timestamp = timer.timestamp()

            if "timer" not in data.keys():
                data['timer'] = updated_timestamp
            if "timercount" not in data.keys():
                data['timercount'] = 1
        else:
            utter(dispatcher,
                "This whole situation is really <em>aweful</em> for a date, but I think we are doing good!🥹 Let’s solve this mystery!☺️ We could talk about my coworkers or investigate the room.🔍"
            )

        data["first_message_sent"] = True

        return check_timer(dispatcher, data)


class ActionReactToReminder(Action):
    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        utter(dispatcher,"The police is coming now! ⏰ Before we go outside tell me who do you suspect as the murderer?👀")

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
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []
        elif data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return []

        sentences = [
            "You can’t leave before the police arrive in a few minutes!😱 We need to find hints together, so they don’t think we two did it. Should we investigate or talk?👀",
            "This is not possible! The murderer could still be walking around.😰 When the police arrive in a few minutes, we need to tell them as much about this Mystery as possible. I think we should investigate the scene more."
        ]

        utter(dispatcher,text= random.choice(sentences))

        return check_timer(dispatcher, data)


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
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []
        elif data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return []

        sentences = [
            "As you already know, I work here at the amusement park.🎡 I'm part of the marketing team and we're currently working on a new marketing campaign, since we recently built a new large rollercoaster in our park and we hope to attract more people to come here.",
            "I'm part of the marketing team at the amusement park. Lately we are working on a campaign for the park, my boss Patrick thinks this is the best way to attract more visitors. If you ask me it would be better to renovate the attractions we have and keep them up to date. But Patrick thinks different...🙄"
        ]

        utter(dispatcher,text=random.choice(sentences))

        return check_timer(dispatcher, data)

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
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []
        elif data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return []

        sentences = [
            "I don't know who the murderer could be.🤷 Let's collect some more hints together, to find out who did it.😊 My co-workers could have something to do with this...",
            "I have no clue at the moment. Let's collect some more hints together, to find out who killed Maria. Could there be a murder weapon in the cabin?🧐"
        ]

        utter(dispatcher,text= random.choice(sentences))

        return check_timer(dispatcher, data)

class CharacterLastSeen(Action):
    def name(self) -> Text:
        return "action_character_last_seen"
    
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
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []
        elif data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return []
        
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        if len(characters) == 1 or characters[0] in ii.get_story_characters():
            utter(dispatcher, text=ii.get_story_information(f"last_seen/{characters[0]}", "", data))
        else:
            utter(dispatcher, text=f"If you want to know something about a character, please specify who you mean.😇")
            

        return check_timer(dispatcher, data)