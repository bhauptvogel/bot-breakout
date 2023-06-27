from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from utils import information_interface as ii
from utils.timer_check import check_timer, set_timer
from utils.string_similarity import get_most_similar_person
from utils.last_talked_about import get_last_talked_about_character, set_last_talked_about_character, reset_last_talked_about_character
from utils.blocked_message import get_blocked_message

class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"

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

        # check if the person asked for is suspect or victim
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
            utter(dispatcher,text="I don't know who you are talking about. Please specify one person you want to know about.")
            reset_last_talked_about_character(data)
            return [SlotSet("data", data)]

        # if user is not specifiing a character
        if len(characters) == 0 or characters[0] == "":
            # TODO: I can tell you the motive of... (all characters the user has not asked the motive about yet) #53
            utter(dispatcher,text="If you want to know the motive about a certain character, let me know who you want to know about.")
            reset_last_talked_about_character(data)
            return [SlotSet("data", data)]

        for character in characters:
            # if user asks about a character that is not in the story
            if character not in ii.get_story_characters():
                utter(dispatcher,text=f"I don't know who {character} is. {get_most_similar_person(character)}")
            else:
                utter(dispatcher,text=ii.get_story_information(f"motive/{character}", "", data))

        set_last_talked_about_character(characters[-1], data)

        if check_timer(data):
            utter(dispatcher,text=set_timer(data))

        return [SlotSet("data", data)]
