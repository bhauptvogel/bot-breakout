# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random


class ValidateSimpleAgeForm(FormValidationAction):
     def name(self) -> Text:
          return "validate_simple_age_form"

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

class SceneInvestigation(Action):
    def name(self) -> Text:
        return "action_scene_investigation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        objects = [e['value'] for e in entities if e['entity'] == 'object']

        dispatcher.utter_message(text=('TODO: Investigate ' + ', '.join(objects) + '...'))

        return []

class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        story_characters = {"Maria": {1: "Maria is the Ex-girlfriend of my co-worker Kira. Do you want to know more about Kira or should we investigate the cabin a bit more?", 2: "Information 2 about Maria"},
                            "Kira" : {1 : "Information 1 about Kira", 2: "Information 2 about Kira"},
                            "Patrick": {1 : "Information 1 about Kira", 2: "Information 2 about Kira"},
                            "Victor": {1 : "Information 1 about Victor", 2: "Information 2 about Victor"},
                            "Anna": {1 : "Information 1 about Anna", 2: "Information 2 about Anna"}}

        for story_character in story_characters:
            if story_character in characters:
                if "times_asked_about_" + story_character not in data:
                    data["times_asked_about_" + story_character] = 1
                    dispatcher.utter_message(text=(story_characters[story_character][1]))
                else:
                    data["times_asked_about_" + story_character] += 1
                    if data["times_asked_about_" + story_character] == 2:
                        dispatcher.utter_message(text=(story_characters[story_character][2]))
                    else:
                        dispatcher.utter_message(text=("You already asked me about " + story_character + " but sure, her you go: " + story_characters[story_character][2]))


        informations = [e['value'] for e in entities if e['entity'] == 'information']
        dispatcher.utter_message(text=('TODO: Investigate characters: ' + ', '.join(characters) + ' / informations: ' + ', '.join(informations) + '...'))

        return [SlotSet("data", data)]


class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # check if the person asked for is suspect or victim
        entities = tracker.latest_message['entities']
        suspects = victim = None
        if 'suspect' in entities['group']:
            suspects = [e['value'] for e in entites if e['group'] == 'suspect' and e['entity'] == 'person']
        elif 'victim' in entities['group']:
            victim = [e['value'] for e in entites if e['group'] == 'victim' and e['entity'] == 'person']
        characters = [e['value'] for e in entities if e['entity'] == 'person']

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        story_characters = {"Kira" : {1 : "Maria is the Ex of Kira. The break up wasn't so nice and a few days after Maria was already together with Victor. Kira didn't handle the break up so good.",
                                      2: "Second answer if asked again (maybe look for a second smaller motive later)"},
                            "Patrick": {1 : "I'm not sure if I should tell you about this, but whatever... the situation can't really get any worse. Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published.",
                                        2: "Second answer if asked again"},
                            "Victor": {1 : "As far as I know, he wouldn't have a reason to kill Maria. They just started dating and it was going really well.",
                                       2: "Second answer if asked again"},
                            "Anna": {1 : "Anna and Maria were rivals. If it's about a good story Anna would have done anything.",
                                     2: "Second answer if asked again"}}

        # If user asks for a motive of Maria (the vicitm)
        if "Maria" in characters and len(characters) == 1 and suspect == None:
            dispatcher.utter_message(
                        text=("Since we're sure that Maria didn't unalive herself, she doesn't have a motive.")
                    )

        # print motive of character that is asked fors
        for story_character, motive in story_characters.items():
            if story_character in suspects:
                if "times_asked_about_" + story_character not in data:
                    data["times_asked_about_" + story_character] = 1
                    dispatcher.utter_message(text=(motive[1]))
                else:
                    data["times_asked_about_" + story_character] += 1
                    if data["times_asked_about_" + story_character] == 2:
                        dispatcher.utter_message(text=(motive[2]))
                    else:
                        dispatcher.utter_message(text=("You already asked me about the motive of " + story_character + " but sure, here you go: " + motive[1])) # To decide: here also motive[2] could be used

        #dispatcher.utter_message(text='TODO: Tell motive of ' + ', '.join(suspects) + ' for killing ' + ', '.join(victim) + '...')
        # last person talked about data["last_person_talked_information"]

        return [SlotSet("data", data)]


class AccessToRollerCoaster(Action):
    def name(self) -> Text:
        return "action_access_to_roller_coaster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        dispatcher.utter_message(text='TODO: Tell access to roller coaster of ' + ', '.join(characters) + '...')

        return []
