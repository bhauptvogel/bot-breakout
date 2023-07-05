from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from utils import information_interface as ii
from utils.last_talked_about import reset_last_talked_about_character
from utils.timer_check import check_timer, set_timer
from utils.blocked_message import get_blocked_message
from utils.formatting import utter

INFORMATION = [
    {
        "text": "Maria is the victim.⚰️ She was a journalist and worked on a big story about this amusment park.",
        "required_story_states": ["character_information/Maria/base_1"],
    },
    {
        "text": "Kira is my co-worker and I know her pretty well.😇",
        "required_story_states": ["character_information/Kira/base_1"],
    },
    {
        "text": "She is the Ex-Girlfriend of Maria.💔 She didn't handle the break-up well, as Maria was already together with Victor after a few days.🫣",
        "required_story_states": ["character_information/Kira/base_1", "motive/Kira"],
    },
    {
        "text": "She works here in the office and has access to the building 👀.",
        "required_story_states": ["character_information/Kira/base_1", "access/Kira"],
    },
    {
        "text": "I don't know Victor very well. He is the new boyfriend of Maria.",
        "required_story_states": ["character_information/Victor/base_1"],
    },
    {
        "text": "I don't see any reason why he would kill Maria.",
        "required_story_states": ["character_information/Victor/base_1", "motive/Victor"],
    },
    {
        "text": "I don't know how he could have accessed the building.🤷",
        "required_story_states": ["character_information/Victor/base_1", "access/Victor"],
    },
    {
        "text": "Anna is a journalist and a colleague of Maria.👩‍💻",
        "required_story_states": ["character_information/Anna/base_1"],
    },
    {
        "text": "She and Maria were rivals.🤼‍♀️ Anna is very driven and wanted to be the first to publish the story about the amusement park.",
        "required_story_states": ["character_information/Anna/base_1", "motive/Anna"],
    },
    {
        "text": "She definitely doesn't have access to the roller coaster.",
        "required_story_states": ["character_information/Anna/base_1", "access/Anna"],
    },
    {
        "text": "Patrick is my snobbish boss who owns the family amusement park business and loves luxury vehicles and opulence.🏆",
        "required_story_states": ["character_information/Patrick/base_1"],
    },
    {
        "text": "As the owner of the amusement park, he has access to the roller coaster.",
        "required_story_states": ["character_information/Patrick/base_1", "access/Patrick"],
    },
    {
        "text": "Maria just found out that Patrick's been caught up in some sketchy corruption stuff. If this gets out, he's toast, but I don't know all the details.👀",
        "required_story_states": ["character_information/Patrick/base_1", "motive/Patrick"],
    },
    {
        "text": "Somebody used a knife to kill Maria. Written on the knife were the initials 'A' and 'P'.👀",
        "required_story_states": ["scene_investigation/knife"],
    },
    {
        "text": "This can only be Anna Pollock or Patrick Anyang.😱",
        "required_story_states": ["scene_investigation/knife", "character_information/Anna/full_name", "character_information/Patrick/full_name"],
    },
    {
        "text": "There is a note on the body saying “<em style='font-family: Brush Script MT, cursive; color: red;'>You are next</em>”. We have to hurry!🥺",
        "required_story_states": ["scene_investigation/note"],
    }
]


class SituationOverview(Action):
    def name(self) -> Text:
        return "action_overview_of_the_state"

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

        if "story_state" not in data.keys() or data["story_state"] == {}:
            data["story_state"] = {}
            return [SlotSet("data", data)]

        utter_text = ""

        for info in INFORMATION:
            in_game_state = True
            for state in info["required_story_states"]:
                keys = state.split("/")
                temp_data = data["story_state"]

                for key in keys:
                    if key in temp_data:
                        temp_data = temp_data[key]
                    else:
                        in_game_state = False
                        break

            # if all states of info are in the game_state 
            if in_game_state:
                if not utter_text:
                    if "hint_given" in data.keys() and data["hint_given"]:
                        utter_text += "Here is everything we talked about so far✨: <br><br>"
                    else:
                        utter_text += "Remember that you can also ask for a hint <br> ✨Here is everything we talked about so far✨: <br><br>"
                utter_text += f"{info['text']}<br>"
            
        if not utter_text:
            utter(dispatcher,text="We have not talked about anything important yet.")
        else:
            utter(dispatcher,text=utter_text)


        reset_last_talked_about_character(data)
               

        return check_timer(dispatcher, data)