from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random


class AccessToRollerCoaster(Action):
    def name(self) -> Text:
        return "action_access_to_roller_coaster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        dispatcher.utter_message(text='TODO: Tell access to roller coaster of ' + ', '.join(characters) + '...')

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        story_characters = {"Kira" : {1 : "Maria is the Ex of Kira. The break up wasn't so nice and a few days after, Maria was already together with Victor. Kira didn't handle the break up very good.",
                                      2: "Second answer if asked again (maybe look for a second smaller motive later)"},
                            "Patrick": {1 : "I'm not sure if I should tell you about this, but whatever... the situation can't really get any worse. Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published.",
                                        2: "Second answer if asked again"},
                            "Victor": {1 : "As far as I know, he wouldn't have a reason to kill Maria. They just started dating and it was going really well.",
                                       2: "Second answer if asked again"},
                            "Anna": {1 : "Anna and Maria were rivals. If it's about a good story Anna would have done anything.",
                                     2: "Second answer if asked again"}}


        return [SlotSet("data", data)]
