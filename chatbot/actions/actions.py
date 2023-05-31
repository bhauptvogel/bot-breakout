from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random


# the object that is used to store the data (inital content)
INITIAL_DATA_OBJECT = {
    "revealed_information": {
        "Kira": {
            "personal_information": False,
            "motive": False,
            "access": False,
            "full_name": False,
        },
        "Maria": {
            "personal_information": False,
            "full_name": False,
        },
        "Victor": {
            "personal_information": False,
            "motive": False,
            "access": False,
            "full_name": False,
        },
        "Anna": {
            "personal_information": False,
            "motive": False,
            "access": False,
            "full_name": False,
        },
        "Patrick": {
            "personal_information": False,
            "motive": False,
            "access": False,
            "full_name": False,
        },
        "Weapon_initials": False,
    },
}


class StartGame(Action):
    # def __init__(self):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker: Tracker, domain):
        dispatcher.utter_message(
            "The police is coming soon! I will remind you in 10 seconds. Just a test"
        )

        date = datetime.now() + timedelta(seconds=10)

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]


class ActionReactToReminder(Action):
    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("The police is coming now! What's our guess?")

        return []



