from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from helpers.timer_check import check_timer, set_timer
from helpers.last_talked_about import reset_last_talked_about_character
from helpers.blocked_message import get_blocked_message

HINTS = [
    # not talked about coworkers
    {
        "text": "Maybe we can talk about my coworkers. I have a hunch they play an important role in all of this.",
        "disallowed_story_states": ["character_information"],
    },
    # scene not investigated
    {
        "text": "Let me look at the surroundings, should I? Investigating the scene might help us.",
        "disallowed_story_states": ["scene_investigation"],
    },
    # not talked about Maria (victim)
    {
        "text": "I think we should talk about Maria. She was the victim after all.",
        "disallowed_story_states": ["character_information/Maria"],
    },
    # not talked about Anna
    {
        "text": "Maybe you should know more about Anna. There is something important you need to know!",
        "disallowed_story_states": ["character_information/Anna"],
    },
    # cabin not investigated
    {
        "text": "It might be time now to take a look at the cabin.",
        "disallowed_story_states": ["scene_investigation/cabin"],
    },
    # not talked about Patrick
    {
        "text": "I think it's time to talk about Patrick. There is stuff you don't know about him yet!",
        "disallowed_story_states": ["character_information/Patrick"],
    },
    # not talked about Kira
    {
        "text": "We cannot get around talking about Kira. Although I don't want her to be a part of this.",
        "disallowed_story_states": ["character_information/Kira"],
    },
    # body not investigated
    {
        "text": "This is so tough but we need to take a look at the body. I know it's hard but it might help us.",
        "disallowed_story_states": ["scene_investigation/body"],
    },
    # note not investigated
    {
        "text": "I think we should take a look and read the note. It might help us.",
        "disallowed_story_states": ["scene_investigation/note"],
    },
    # weapon not investigated
    {
        "text": "I could take a closer look at the weapon.",
        "disallowed_story_states": ["scene_investigation/weapon"],
    },
    # knife not investigated
    {
        "text": "Let's look at the knife, should we?",
        "disallowed_story_states": ["scene_investigation/knife"],
    },
    # not asked about full names of characters (because of intitials)
    {
        "text": "I'm not sure you have the full names of the characters. I think you need them if you want to know who could be 'A.P.'",
        "disallowed_story_states": [
            "character_information/Maria/full_name",
            "character_information/Anna/full_name",
            "character_information/Patrick/full_name",
            "character_information/Kira/full_name",
            "character_information/Victor/full_name",
        ],
    },
    # not asked about possible motives of characters
    {
        "text": "Maybe we can think about possible motives of the characters.",
        "disallowed_story_states": [
            "motive/Maria",
            "motive/Anna",
            "motive/Patrick",
            "motive/Kira",
            "motive/Victor",
        ],
    },
    # not asked about possible access to rollercoaster
    {
        "text": "I think it might help us to clear our minds about who even had access to this rollercoaster and part of the amusement park.",
        "disallowed_story_states": [
            "access/Maria",
            "access/Anna",
            "access/Patrick",
            "access/Kira",
            "access/Victor",
        ],
    },
    # not asked about patricks secret
    {
        "text": "I'm not sure I told you everything about Patrick. There is more. He has a secret...",
        "disallowed_story_states": ["character_information/Patrick/secret"],
    },
]


class Hint(Action):
    def name(self) -> Text:
        return "action_give_hint"

    def get_next_hint(self, data):
        if "story_state" not in data:
            data["story_state"] = {}

        for hint in HINTS:
            in_game_state = []
            for state in hint["disallowed_story_states"]:
                in_game_state.append(True)
                keys = state.split("/")
                temp_data = data["story_state"]

                for key in keys:
                    if key in temp_data:
                        temp_data = temp_data[key]
                    else:
                        in_game_state[-1] = False
                        break

            # if all states of hint are not in game state, return hint
            if not any(in_game_state):
                return hint["text"]

        return "I don't have any hints for you right now."

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

        if ("cabin_riddle_started" in data.keys() and data["cabin_riddle_started"] == True):
            output = {
                1: "Ok, let's focus on the riddle. Just try typing in a number and we will work this out together.",
                2: "Ok, let's focus on the riddle. Maybe there is another way to look at the cabin number.",
                3: "Maybe look at the 686 ANOTHER WAY...",
                4: "Let's focus on the riddle. Just try typing in a number and we will work this out together.",
                5: "Oh I see now... the cabin number is 989",
                6: "It should be (989 - 7 + 2) / 2.",
            }
            if data["cabin_guess"] > 6:
                dispatcher.utter_message(text=output[6])
                return [SlotSet("data", data)]
            elif data["cabin_guess"] in output.keys():
                dispatcher.utter_message(text=output[data["cabin_guess"]])
                data["cabin_guess"] += 1
                return [SlotSet("data", data)]

        if "blocked" in data and data["blocked"][self.name()] != "":
            dispatcher.utter_message(text=get_blocked_message(data,data["blocked"][self.name()]))
            return [SlotSet("data", data)]

        dispatcher.utter_message(text=self.get_next_hint(data))

        reset_last_talked_about_character(data)

        if check_timer(data):
                dispatcher.utter_message(text=set_timer(data))

        return [SlotSet("data", data)]
