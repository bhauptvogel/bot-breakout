from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import helper



INFORMATION = {
    "Maria": {
        "personal_information": "Maria is the victim. She was a journalist and worked on a big story about this amusment park. ",
    },
    "Kira": {
        "personal_information": "Kira is my co-worker and I know her pretty well. ",
        "motive": "She is the Ex-Girlfriend of Maria. She didn't handle the break-up well, as Maria was already together with Victor after a few days. ",
        "access": "She works here in the office and has access to the building 👀. ",
    },
    "Victor": {
        "personal_information": "I don't know Victor very well. He is the new boyfriend of Maria. ",
        "motive": "I don't see any reason why he would kill Maria. ",
        "access": "I don't know how he could have accessed the building. ",
    },
    "Anna": {
        "personal_information": "Anna is a journalist and a colleague of Maria. ",
        "motive": "She and Maria were rivals. Anna is very driven and wanted to be the first to publish the story about the amusement park. ",
        "access": "She definitely doesn't have access to the roller coaster. ",
    },
    "Patrick": {
        "personal_information": "Patrick is my snobbish boss who owns the family amusement park business and loves luxury vehicles and opulence. ",
        "motive": "Maria just found out that Patrick's been caught up in some sketchy corruption stuff. If this gets out, he's toast, but I don't know all the details. ",
        "access": "As the owner of the amusement park, he has access to the roller coaster. ",
    },
    "Weapon_initials": "Somebosy used a knife to kill Maria. Written on the knife were the initials 'A' and 'P'.",
    "Weapon_full_name": "This can only be Anna Pollock or Patrick Anyang.",
}


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

        revealed_information = data["revealed_information"]

        dispatcher.utter_message(text="Here is everything we talked about so far: \n\n")

        # Maria information
        if (revealed_information["Maria"]["personal_information"] == True):
            dispatcher.utter_message(text=INFORMATION["Maria"]["personal_information"] + " \n")

        # Kira information
        if (revealed_information["Kira"]["personal_information"] == True):
            dispatcher.utter_message(text=INFORMATION["Kira"]["personal_information"])
            if (revealed_information["Kira"]["motive"] == True):
                dispatcher.utter_message(text=INFORMATION["Kira"]["motive"])
            if (revealed_information["Kira"]["access"] == True):
                dispatcher.utter_message(text=INFORMATION["Kira"]["access"])
            dispatcher.utter_message(text=" \n")
        
        # Victor information
        if (revealed_information["Victor"]["personal_information"] == True):
            dispatcher.utter_message(text=INFORMATION["Victor"]["personal_information"])
            if (revealed_information["Victor"]["motive"] == True):
                dispatcher.utter_message(text=INFORMATION["Victor"]["motive"])
            if (revealed_information["Victor"]["access"] == True):
                dispatcher.utter_message(text=INFORMATION["Victor"]["access"])
            dispatcher.utter_message(text=" \n")

        # Anna information
        if (revealed_information["Anna"]["personal_information"] == True):
            dispatcher.utter_message(text=INFORMATION["Anna"]["personal_information"])
            if (revealed_information["Anna"]["motive"] == True):
                dispatcher.utter_message(text=INFORMATION["Anna"]["motive"])
            if (revealed_information["Anna"]["access"] == True):
                dispatcher.utter_message(text=INFORMATION["Anna"]["access"])
            dispatcher.utter_message(text=" \n")

        # Patrick information
        if (revealed_information["Patrick"]["personal_information"] == True):
            dispatcher.utter_message(text=INFORMATION["Patrick"]["personal_information"])
            if (revealed_information["Patrick"]["motive"] == True):
                dispatcher.utter_message(text=INFORMATION["Patrick"]["motive"])
            if (revealed_information["Patrick"]["access"] == True):
                dispatcher.utter_message(text=INFORMATION["Patrick"]["access"])
            dispatcher.utter_message(text=" \n")

        # Weapon information
        if (revealed_information["Weapon_initials"] == True):
            dispatcher.utter_message(text=INFORMATION["Weapon_initials"])
            if (revealed_information["Anna"]["motive"]["full_name"] == True) and (revealed_information["Patrick"]["motive"]["full_name"] == True):
                dispatcher.utter_message(text=INFORMATION["Weapon_full_name"])



        return [SlotSet("data", data)]
