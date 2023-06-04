from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random

HINTS = [
    # not talked about coworkers
    {
        "text": "Maybe we can talk about my coworkers. I have a hunch they play an important role in all of this.",
        "not_in_game_state": ["character_information"],
    },
    # scene not investigated
    {
        "text": "Let me look at the surroundings, should I? Investigating the scene might help us.",
        "not_in_game_state": ["scene_investigation"],
    },
    # not talked about Maria (victim)
    {
        "text": "I think we should talk about Maria. She was the victim after all.",
        "not_in_game_state": ["character_information/Maria"],
    },
    # not talked about Anna
    {
        "text": "Maybe you should know more about Anna. There is something important you need to know!",
        "not_in_game_state": ["character_information/Anna"],
    },
    # cabin not investigated
    {
        "text": "It might be time now to take a look at the cabin.",
        "not_in_game_state": ["scene_investigation/cabin"],
    },
    # not talked about Patrick
    {
        "text": "I think it's time to talk about Patrick. There is stuff you don't know about him yet!",
        "not_in_game_state": ["character_information/Patrick"],
    },
    # not talked about Kira
    {
        "text": "We cannot get around talking about Kira. Although I don't want her to be a part of this.",
        "not_in_game_state": ["character_information/Kira"],
    },
    # body not investigated
    {
        "text": "This is so tough but we need to take a look at the body. I know it's hard but it might help us.",
        "not_in_game_state": ["scene_investigation/body"],
    },
    # note not investigated
    {
        "text": "I think we should take a look and read the note. It might help us.",
        "not_in_game_state": ["scene_investigation/note"],
    },
    # weapon not investigated
    {
        "text": "I could take a closer look at the weapon.",
        "not_in_game_state": ["scene_investigation/weapon"],
    },
    # knife not investigated
    {
        "text": "Let's look at the knife, should we?",
        "not_in_game_state": ["scene_investigation/knife"],
    },
    # not asked about possible motives of characters
    {
        "text": "Maybe we can think about possible motives of the characters.",
        "not_in_game_state": [
            "character_information/Maria/motive",
            "character_information/Anna/motive",
            "character_information/Patrick/motive",
            "character_information/Kira/motive",
            "character_information/Victor/motive",
        ],
    },
    # not asked about possible access to rollercoaster
    {
        "text": "I think it might help us to clear our minds about who even had access to this rollercoaster and part of the amusement park.",
        "not_in_game_state": [
            "character_information/Maria/access",
            "character_information/Anna/access",
            "character_information/Patrick/access",
            "character_information/Kira/access",
            "character_information/Victor/access",
        ],
    },
    # not asked about patricks secret
    {
        "text": "I'm not sure I told you everything about Patrick. There is more. He has a secret...",
        "not_in_game_state": ["character_information/Patrick/secret"],
    },
    # not asked about full names of characters (because of intitials)
    {
        "text": "I'm not sure you have the full names of the characters. I think you need them if you want to know who could be 'A.P.'",
        "not_in_game_state": [
            "character_information/Maria/full_name",
            "character_information/Anna/full_name",
            "character_information/Patrick/full_name",
            "character_information/Kira/full_name",
            "character_information/Victor/full_name",
        ],
    },
]


class Hint(Action):
    def name(self) -> Text:
        return "action_give_hint"

    def get_next_hint(self, data):
        

        for hint in HINTS:
            not_in_game_state = hint["not_in_game_state"]
            in_game_state = []
            for state in not_in_game_state:
                in_game_state.append(True)
                keys = state.split("/")
                temp_data = data["story_state"]
                print(keys)

                for key in keys:
                    print(key)
                    if key in temp_data:
                        temp_data = temp_data[key]
                    else:
                        in_game_state[-1] = False
                        break

            # if only false in in_game_state, return hint
            if not any(in_game_state):
                return hint["text"]


        return

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

        dispatcher.utter_message(text=self.get_next_hint(data))

        return [SlotSet("data", data)]

