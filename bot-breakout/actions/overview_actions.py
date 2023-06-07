from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import information_interface as ii

INFORMATION = [
    {
        "text": "Maria is the victim. She was a journalist and worked on a big story about this amusment park.",
        "required_story_states": ["character_information/Maria/base_1"],
    },
    {
        "text": "Kira is my co-worker and I know her pretty well.",
        "required_story_states": ["character_information/Kira/base_1"],
    },
    {
        "text": "She is the Ex-Girlfriend of Maria. She didn't handle the break-up well, as Maria was already together with Victor after a few days.",
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
        "text": "I don't know how he could have accessed the building.",
        "required_story_states": ["character_information/Victor/base_1", "access/Victor"],
    },
    {
        "text": "Anna is a journalist and a colleague of Maria.",
        "required_story_states": ["character_information/Anna/base_1"],
    },
    {
        "text": "She and Maria were rivals. Anna is very driven and wanted to be the first to publish the story about the amusement park.",
        "required_story_states": ["character_information/Anna/base_1", "motive/Anna"],
    },
    {
        "text": "She definitely doesn't have access to the roller coaster.",
        "required_story_states": ["character_information/Anna/base_1", "access/Anna"],
    },
    {
        "text": "Patrick is my snobbish boss who owns the family amusement park business and loves luxury vehicles and opulence.",
        "required_story_states": ["character_information/Patrick/base_1"],
    },
    {
        "text": "As the owner of the amusement park, he has access to the roller coaster.",
        "required_story_states": ["character_information/Patrick/base_1", "access/Patrick"],
    },
    {
        "text": "Maria just found out that Patrick's been caught up in some sketchy corruption stuff. If this gets out, he's toast, but I don't know all the details.",
        "required_story_states": ["character_information/Patrick/base_1", "motive/Patrick"],
    },
    {
        "text": "Somebody used a knife to kill Maria. Written on the knife were the initials 'A' and 'P'.",
        "required_story_states": ["scene_investigation/knife"],
    },
    {
        "text": "This can only be Anna Pollock or Patrick Anyang.",
        "required_story_states": ["scene_investigation/knife", "character_information/Anna/full_name", "character_information/Patrick/full_name"],
    },
    {
        "text": "There is a note on the body saying “You are next”. We have to hurry!",
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

        if "story_state" not in data or data["story_state"] is {}:
            data["story_state"] = {}
            return [SlotSet("data", data)]

        dispatcher.utter_message(text="Here is everything we talked about so far: \n\n")

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
                dispatcher.utter_message(text=info["text"])
                

        return [SlotSet("data", data)]
