from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random

KIRA_SYNONYMS = ["Kira", "Kiras", "Kira's", "Kisa", "kira"]
PATRICK_SYNONYMS = ["Patrick", "Patricks", "Patrik", "Patriks", "Patrik's", "Patrick's", "Padrik", "patrick"]
VICTOR_SYNONYMS = ["Victor", "Victors", "Victor's", "Viktor", "Vicktor", "Viktors", "Vicktors", "victor"]
ANNA_SYNONYMS = ["Anna", "Ana", "Annna", "Annas", "Anna's", "anna"]
MARIA_SYNONYMS = ["Maria", "Marias", "Maria's", "Marie", "Marria", "maria"]


class StartGame(Action):
    # def __init__(self):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker: Tracker, domain):
        dispatcher.utter_message("The police is coming soon! I will remind you in 10 seconds. Just a test")

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


class GiveHint(Action):
    def name(self) -> Text:
        return "action_hint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='TODO: Give hint (answer to last question)')

        return []

class SituationOverview(Action):
    def name(self) -> Text:
        return "action_overview_of_the_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='TODO: Give situation overview')

        return []
