from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled
from utils.timer_check import check_timer, set_timer
from utils.blocked_message import get_blocked_message

from datetime import datetime, timedelta
import random
from utils import information_interface as ii
from utils.string_similarity import get_most_similar_person
from utils.last_talked_about import get_last_talked_about_character, set_last_talked_about_character, reset_last_talked_about_character
from utils.formatting import utter

class AccessToRollerCoaster(Action):
    def name(self) -> Text:
        return "action_access_to_roller_coaster"
    
    def hint_access(self, data):
        if "story_state" not in data or "access" not in data["story_state"]:
            return ""
        
        discussed_characters = data["story_state"]["access"]
        discussed_characters = list(discussed_characters.keys())

        characters_to_talk_about = []
        for character in ii.get_story_characters():
            if character not in discussed_characters:
                characters_to_talk_about.append(character)

        if len(characters_to_talk_about) == 0:
            return ""
        elif len(characters_to_talk_about) == 1:
            return "I could tell you if " + characters_to_talk_about[0] + " had access to the roller coaster."
        elif len(characters_to_talk_about) == 2:
            return "You have not asked if " + characters_to_talk_about[0] + " or " + characters_to_talk_about[1] + " had access to this roller coaster."
        else:
            return "It might be helpful for you to know if "+ ", ".join(characters_to_talk_about[:-1]) + " or " + characters_to_talk_about[-1] + " had access to the roller coaster."

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        if "blocked" in data and data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return [SlotSet("data", data)]

        entities = tracker.latest_message['entities']
        characters = []
        subjetive_pronouns = [] # if the user says he/she/her/him
        for e in entities:
            if e['entity'] == 'person':
                if 'group' in e and e['group'] == 'reference':
                    subjetive_pronouns.append(e['value'])
                else:
                    characters.append(e['value'])

        if len(subjetive_pronouns) == 1:
            # TODO: Check gender of last talked about character
            characters.append(get_last_talked_about_character(data))
        elif len(subjetive_pronouns) > 1:
            utter(dispatcher,text=f"I don't know who you are talking about.😵 Please specify one person you want to know about. {self.hint_access(data)}")
            reset_last_talked_about_character(data)
            return [SlotSet("data", data)]


        # if user is not specifiing a character
        if len(characters) == 0 or characters[0] == "":
            utter(dispatcher,text=f"If you want to know who had access to the roller coaster, tell me who do you want to know about.🥺 {self.hint_access(data)}")
            reset_last_talked_about_character(data)
            return [SlotSet("data", data)]
        
        for character in characters:
            # if user asks about a character that is not in the story
            if character not in ii.get_story_characters():
                utter(dispatcher,text=f"I don't know who {character} is.😵 {get_most_similar_person(character)}")
            else:
                utter(dispatcher,text=ii.get_story_information(f"access/{character}", "", data))
        
        set_last_talked_about_character(characters[-1], data)

        if check_timer(data):
            utter(dispatcher,text=set_timer(data))  

        return [SlotSet("data", data)]
