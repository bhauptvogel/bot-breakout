from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from utils import information_interface as ii
from utils.timer_check import check_timer, end_of_game
from utils.last_talked_about import reset_last_talked_about_character
from utils.string_similarity import get_most_similar_person
from utils.blocked_message import get_blocked_message
from utils.end_of_game import guess_murderer
from utils.formatting import utter

PERCENTAGE_THRESHOLD = 0.40

REQUIRED_GAME_STATES = [
    "character_information/Maria",
    "character_information/Anna",
    "character_information/Patrick",
    "character_information/Kira",
    "scene_investigation/base_1",
    "scene_investigation/cabin",
    "scene_investigation/body",
    "scene_investigation/knife",
    "scene_investigation/weapon",
    "motive/Maria",
    "motive/Anna",
    "motive/Patrick",
    "motive/Kira",
    "access/Maria",
    "access/Anna",
    "access/Patrick",
    "access/Kira",
]

# TODO: Rename file to "user_guess.py"

class UserGuessesMurderer(Action):
    def name(self) -> Text:
        return "action_user_guess"
    
    def get_percentage_of_required_game_states(self, data):
        if "story_state" not in data:
            data["story_state"] = {}

        false_count = 0
        for state in REQUIRED_GAME_STATES:
            keys = state.split("/")
            temp_data = data["story_state"]

            for key in keys:
                if key in temp_data:
                    temp_data = temp_data[key]
                else:
                    false_count += 1
                    break

        true_count = len(REQUIRED_GAME_STATES) - false_count
        return true_count / (true_count + false_count)


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot("data") is None or tracker.get_slot("data") == "Null":
            data = {}
        else:
            data = tracker.get_slot("data")
        
        if "blocked" not in data.keys():
            utter(dispatcher, text=get_blocked_message(data,"no_greet_yet"))
            return []
        elif data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return [SlotSet("data", data)]

        entities = tracker.latest_message["entities"]
        person = [e["value"] for e in entities if e["entity"] == "person"]

        # ! hack for the case that the "Maria" entity is in persons (f.e. "Did Kira kill Maria?")
        if len(person) == 2 and "Maria" in person:
                # person is the other person
                person = [e["value"] for e in entities if (e["entity"] == "person" and e["role"] == "suspect")]

        if len(person) != 1:
            utter(dispatcher,text="So who do you think it is? I'm confused.😵")
            return [SlotSet("data", data)]
        elif person[0] not in ii.get_story_characters():
            utter(dispatcher,text=f"I don't know who {person[0]} is.😵 {get_most_similar_person(person[0])}")
            return [SlotSet("data", data)]

        if self.get_percentage_of_required_game_states(data) > PERCENTAGE_THRESHOLD or end_of_game(data):
            utter(dispatcher,text=guess_murderer(data, person[0]))
            return [SlotSet("data", data)]
        else:
            utter(dispatcher,
                #text="We can’t leave before the police arrives in a few minutes! You need to know more about this story to be sure. Let's find more hints together, so they don’t think we two did it. We need to check for a motive, if the suspect had access and the murder weapon!"
                f"So you guess that {person[0]} is the murderer...👀 We need to make sure we know as much about all of our suspects as possible, like if they had <b>access to the train</b> and their <b>motive</b>. Also taking a closer look at the <b> murder weapon </b> could give a clue! Lets go on with the investigation before we accuse someone."
            )
        
            reset_last_talked_about_character(data)

            return check_timer(dispatcher, data)
    