from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random


class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # check if the person asked for is suspect or victim
        entities = tracker.latest_message['entities']
        suspect = [e['value'] for e in entities if e['group'] == 'suspect' and e['entity'] == 'person']
        victim = [e['value'] for e in entities if e['group'] == 'victim' and e['entity'] == 'person']

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

        # If user asks for a motive of Maria (the vicitm)
        if "Maria" in victim and suspect == []:
            dispatcher.utter_message(
                        text=("I'm pretty sure Maria didn't unalive herself. This looks definitly like a murder.")
                    )

        # print motive of character that is asked fors
        for story_character, motive in story_characters.items():
            if len(suspect) > 1:
                if story_character in suspect:
                    if "times_asked_about_" + story_character not in data:
                        data["times_asked_about_" + story_character] = 1
                        dispatcher.utter_message(text=(story_character + "'s motive to kill Maria is: " + motive[1]))
                    else:
                        data["times_asked_about_" + story_character] += 1
                        if data["times_asked_about_" + story_character] == 2:
                            dispatcher.utter_message(text=(story_character + "'s motive to kill Maria is: " + motive[2]))
                        else:
                            dispatcher.utter_message(text=("You already asked me about " + story_character + "'s motive but no worries, i'll tell you again. " + motive[1]))
            else:
                if story_character in suspect:
                    if "times_asked_about_" + story_character not in data:
                        data["times_asked_about_" + story_character] = 1
                        dispatcher.utter_message(text=(motive[1]))
                    else:
                        data["times_asked_about_" + story_character] += 1
                        if data["times_asked_about_" + story_character] == 2:
                            dispatcher.utter_message(text=(motive[2]))
                        else:
                            dispatcher.utter_message(text=("You already asked me about " + story_character + "'s motive but no worries, i'll tell you again. " + motive[1])) # To decide: here also motive[2] could be used

        # TODO: set last person talked about
        if len(suspect) == 1:
            data["last_person_talked_information"] = suspect
        else:
            if  len(suspect) > 1:
                print("Suspects: ", suspect)
                data["last_person_talked_information"] = suspect

        return [SlotSet("data", data)]
