from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

#from datetime import datetime, timedelta
import random





class StartGame(Action):
    # def __init__(self):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker: Tracker, domain):
        dispatcher.utter_message(
            "Oh, I’m just a bit stunned. I know this woman - it's Maria, a journalist... After seeing the dead body, I called the police. Because this is what a good citizen does, doesn’t they? But now I’m not sure if it was the right decision... We are the only people here and its my work place. I might be a suspect! We have 10 min until the police is here. I should give them some valuable hints about this case when they arrive here. But I don’t know where to start. Can you help me clear my mind? We could first investigate the body with the note, or I can tell you about my co-workers."
        )

        #date = datetime.now() + timedelta(seconds=10)

        #reminder = ReminderScheduled(
        #    "EXTERNAL_reminder",
        #    trigger_date_time=date,
        #    name="my_reminder",
        #    kill_on_user_message=False,
        #)

        #return [reminder]
        return []

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



