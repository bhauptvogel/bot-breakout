from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random

from actions.actions import INITIAL_DATA_OBJECT


class CharacterMotive(Action):
    def name(self) -> Text:
        return "action_tell_motive"



    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')

        # check if the person asked for is suspect or victim
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        if len(characters) > 0:
            # if unknown name in characters
            if type(characters) == str:
                dispatcher.utter_message(text=("I'm sorry, I don't know this person..."))
                data["last_spoken_about_character"] = []
                return [SlotSet("data", data)]
        print("Characters after: ", characters)

        # check if group is set and define suspects and victims
        suspects = victim = []
        if len(entities) > 0 and "group" in entities[0].keys():
            suspects = [e['value'] for e in entities if e['group'] == 'suspect' and e['entity'] == 'person']
            victim = [e['value'] for e in entities if e['group'] == 'victim' and e['entity'] == 'person']

            # if unknown name in characters
            if type(suspects) == str:
                dispatcher.utter_message(text=("I'm sorry, I don't know a person called " + suspects + "."))
                data["last_spoken_about_character"] = []
                return [SlotSet("data", data)]
            if type(victim) == str:
                dispatcher.utter_message(text=("I'm sorry, I don't know a person called " + victim + "."))
                data["last_spoken_about_character"] = []
                return [SlotSet("data", data)]
        # else:
        #     # If user enters a name that is not in our story
        #     dispatcher.utter_message(text=("I'm sorry, I don't know this person..."))
        #     data["last_spoken_about_character"] = []
        #     return [SlotSet("data", data)]

        story_characters = {"Kira" : {1 : "Maria is the Ex of Kira. The break up wasn't so nice and a few days after, Maria was already together with Victor. Kira didn't handle the break up very good.",
                                      2: "Second answer if asked again (maybe look for a second smaller motive later)"},
                            "Patrick": {1 : "I'm not sure if I should tell you about this, but whatever... the situation can't really get any worse. Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published.",
                                        2: "Second answer if asked again",
                                        3: "Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published."},
                            "Victor": {1 : "As far as I know, he wouldn't have a reason to kill Maria. They just started dating and it was going really well.",
                                       2: "Second answer if asked again"},
                            "Anna": {1 : "Anna and Maria were rivals. If it's about a good story Anna would have done anything.",
                                     2: "Second answer if asked again"}}


        # If user asks for a motive of Maria (the vicitm)
        if "Maria" in victim and suspects == []:
            dispatcher.utter_message(
                        text=("I'm pretty sure Maria didn't unalive herself. This looks definitly like a murder.")
                    )
            data["last_spoken_about_character"] = []
            return [SlotSet("data", data)]

        print("Suspect: ", suspects)
        print("Victim: ", victim)

        # print motive of character that is asked for, if specific name was entered
        if len(suspects) > 0:
            for story_character, motive in story_characters.items():
                if len(suspects) > 1:
                    if story_character in suspects:
                        if "times_asked_about_" + story_character not in data:
                            data["times_asked_about_" + story_character] = 1
                            data["revealed_information"][story_character]["motive"] = True
                            dispatcher.utter_message(text=(story_character + "'s motive is: " + motive[1]))
                        else:
                            data["times_asked_about_" + story_character] += 1
                            if data["times_asked_about_" + story_character] == 2:
                                dispatcher.utter_message(text=(story_character + "'s motive to kill Maria is: " + motive[2]))
                            else:
                                dispatcher.utter_message(text=("You already asked me about " + story_character + "'s motive but no worries, i'll tell you again. " + motive[3]))
                else:
                    if story_character in suspects:
                        if "times_asked_about_" + story_character not in data:
                            data["times_asked_about_" + story_character] = 1
                            dispatcher.utter_message(text=(motive[1]))
                        else:
                            data["times_asked_about_" + story_character] += 1
                            if data["times_asked_about_" + story_character] == 2:
                                dispatcher.utter_message(text=(motive[2])) # To decide: here also motive[2] could be used
                            else:
                                dispatcher.utter_message(text=("You already asked me about " + story_character + "'s motive but no worries, i'll tell you again. " + motive[3]))
        #If they ask about "her", "him", "it" it uses the "last_spoken"
        elif len(suspects) == 0:
            #append the response of API in the form of title and payload
            buttons = []
            # buttons.append({"title": "" , "payload": ""})
            if "last_spoken_about_character" in data.keys() and data["last_spoken_about_character"] == "":
                dispatcher.utter_message(text="I'm not sure who you mean")
            elif "last_spoken_about_character" in data.keys() and len(data["last_spoken_about_character"]) == 2:
                buttons.append({"title": "" , "payload": data["last_spoken_about_character"][0],
                                "title": "" , "payload": data["last_spoken_about_character"][1]})
                dispatcher.utter_message(text="Which person do you want to know more about its motive:",
                                         buttons=buttons)
                print("Buttons: ", buttons)

            # if characters == []:
            #     if "last_spoken_about_character" in data.keys():
            #         for last_spoken in data["last_spoken_about_character"]:
            #             if "times_asked_about_" + last_spoken not in data:
            #                 data["times_asked_about_" + last_spoken] = 1
            #                 dispatcher.utter_message(text=(story_characters[last_spoken][1]))
            #             else:
            #                 data["times_asked_about_" + last_spoken] += 1
            #                 if data["times_asked_about_" + last_spoken] == 2:
            #                     if 2 not in story_characters[last_spoken]:
            #                         dispatcher.utter_message(text=("You already asked me about " + last_spoken + " but sure, her you go: " + story_characters[last_spoken][1]))
            #                     else:
            #                         dispatcher.utter_message(text=(story_characters[last_spoken][2]))
            #                 else:
            #                     dispatcher.utter_message(text=("You already asked me about " + last_spoken + " but sure, her you go: " + story_characters[last_spoken][1]))

        # set last persons that user asked about
        data["last_spoken_about_character"] = characters
        print("Data: ", data)

        return [SlotSet("data", data)]
