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
from utils.formatting import utter

class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"
    
    def hint_motive(self, data):
        if "story_state" not in data or "motive" not in data["story_state"]:
            return "We can talk about Kira, Patrick, Anna or the victim Maria."
        
        discussed_characters = data["story_state"]["motive"]
        discussed_characters = list(discussed_characters.keys())

        characters_to_talk_about = []
        for character in ii.get_story_characters():
            if character not in discussed_characters:
                characters_to_talk_about.append(character)

        if len(characters_to_talk_about) == 0:
            return ""
        elif len(characters_to_talk_about) == 1:
            return "We can maybe talk about why " + characters_to_talk_about[0] + " might have killed Maria."
        elif len(characters_to_talk_about) == 2:
            return "We have not yet discussed why " + characters_to_talk_about[0] + " or " + characters_to_talk_about[1] + " might have done it."
        else:
            return "You can ask me about possible motives of " + ", ".join(characters_to_talk_about[:-1]) + " or " + characters_to_talk_about[-1] + "."


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []
        elif data["blocked"][self.name()] != "":
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
            utter(dispatcher,text=f"I don't know who you are talking about.😵 Please specify one person you want to know about. {self.hint_motive(data)}")
            reset_last_talked_about_character(data)
            return [SlotSet("data", data)]

        # if user is not specifiing a character
        if len(characters) == 0 or characters[0] == "":
            utter(dispatcher,text=f"If you want to know the motive about a certain person, let me know who you want to know about.😊 {self.hint_motive(data)}")
            reset_last_talked_about_character(data)
            return [SlotSet("data", data)]

        for character in characters:
            # if user asks about a character that is not in the story
            if character not in ii.get_story_characters():
                utter(dispatcher,text=f"I don't know who {character} is.😵 {get_most_similar_person(character)}")
            else:
                utter(dispatcher,text=ii.get_story_information(f"motive/{character}", "", data))

        set_last_talked_about_character(characters[-1], data)

        return check_timer(dispatcher, data)
