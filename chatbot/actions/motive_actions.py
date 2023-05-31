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

        suspects = []
        victim = []
        story_characters = {"Kira" : {1: "Maria is the Ex of Kira. The break up wasn't so nice and a few days after, Maria was already together with Victor. Kira didn't handle the break up very good.",
                                      2: "Maria is the Ex of Kira. The break up wasn't so nice and a few days after, Maria was already together with Victor. Kira didn't handle the break up very good.",
                                      3: "Maria is the Ex of Kira. The break up wasn't so nice and a few days after, Maria was already together with Victor. Kira didn't handle the break up very good."},
                            "Patrick": {1: "I'm not sure if I should tell you about this, but whatever... the situation can't really get any worse. Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published.",
                                        2: "I'm not sure if I should tell you about this, but whatever... the situation can't really get any worse. Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published.",
                                        3: "Maria had recently discovered that Patrick was involved in some illegal activities reagrding corruption. I don't know the details but it would have been the end of Patricks career if this story got published."},
                            "Victor": {1: "As far as I know, he wouldn't have a reason to kill Maria. They just started dating and it was going really well.",
                                       2: "As far as I know, he wouldn't have a reason to kill Maria. They just started dating and it was going really well.",
                                       3: "I don't think he had a reason to kill Maria. They just started dating and it was going really well."},
                            "Anna": {1: "Anna and Maria were rivals. If it's about a good story Anna would have done anything.",
                                     2: "Anna and Maria were rivals. If it's about a good story Anna would have done anything.",
                                     3: "Anna and Maria were rivals. If it's about a good story Anna would have done anything."}
                            }

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')

        # check if the person asked for is suspect or victim
        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        print("Original entered names: ", characters)

        # set character to last_spoken_about if empty
        # If they ask about "her", "him", "it" it uses the "last_spoken"
        if len(characters) == 0 and "last_spoken_about_character" in data:
            if len(data["last_spoken_about_character"]) == 2:
                print("Add Button for user to choose which person hes/shes talking about")
                # buttons = []
                # if "last_spoken_about_character" in data.keys() and data["last_spoken_about_character"] == "":
                #     dispatcher.utter_message(text="I'm not sure who you mean")
                # elif "last_spoken_about_character" in data.keys() and len(data["last_spoken_about_character"]) == 2:
                #     buttons.append({"title": "" , "payload": data["last_spoken_about_character"][0],
                #                     "title": "" , "payload": data["last_spoken_about_character"][1]})
                #     dispatcher.utter_message(text="Which person do you want to know more about its motive:",
                #                             buttons=buttons)
                #     print("Buttons: ", buttons)
            characters = data["last_spoken_about_character"]
            for character in characters:
                if character in story_characters.keys():
                    suspects.append(character)
                elif character == "Maria":
                    victim.append("Maria")
            print("Her/him case: " + str(characters))

        elif len(characters) == 0 and "last_spoken_about_character" not in data:
            dispatcher.utter_message(text=("Who do you mean?"))
            return [SlotSet("data", data)]

        # If user enters an name that is not in our story
        if len(characters) == 1 and characters[0] not in story_characters.keys() and characters[0] != "Maria":
            dispatcher.utter_message(text=("I'm sorry, I don't know this person..."))
            data["last_spoken_about_character"] = characters
            return [SlotSet("data", data)]

        # check if group is set and define suspects and victims
        if len(entities) > 0 and "group" in entities[0].keys():
            suspects = [e['value'] for e in entities if e['group'] == 'suspect' and e['entity'] == 'person']
            victim = [e['value'] for e in entities if e['group'] == 'victim' and e['entity'] == 'person']

        # If user asks for a motive of Maria (the vicitm)
        if "Maria" in victim and suspects == []:
            dispatcher.utter_message(text=("I'm pretty sure Maria didn't unalive herself. This looks definitly like a murder."))
            data["last_spoken_about_character"] = ["Maria"]
            return [SlotSet("data", data)]
        print(data)
        # print motive of character that is asked for, if specific name was entered
        if len(suspects) > 0:
            for story_character, motive in story_characters.items():
                if len(suspects) > 1:
                    if story_character in suspects:
                        if "times_asked_about_" + story_character + "_motive" not in data:
                            data["times_asked_about_" + story_character + "_motive"] = 1
                            data["revealed_information"][story_character]["motive"] = True
                            dispatcher.utter_message(text=(story_character + "'s motive is: " + motive[1]))
                        else:
                            data["times_asked_about_" + story_character + "_motive"] += 1
                            if data["times_asked_about_" + story_character + "_motive"] == 2:
                                dispatcher.utter_message(text=(story_character + "'s motive to kill Maria could be: " + motive[2]))
                            else:
                                dispatcher.utter_message(text=("You already asked me about " + story_character + "'s motive but no worries, i'll tell you again. " + motive[3]))
                else:
                    if story_character in suspects:
                        if "times_asked_about_" + story_character + "_motive" not in data:
                            data["times_asked_about_" + story_character + "_motive"] = 1
                            dispatcher.utter_message(text=(motive[1]))
                        else:
                            data["times_asked_about_" + story_character + "_motive"] += 1
                            if data["times_asked_about_" + story_character + "_motive"] == 2:
                                dispatcher.utter_message(text=(motive[2])) # To decide: here also motive[2] could be used
                            else:
                                dispatcher.utter_message(text=("You already asked me about " + story_character + "'s motive but no worries, i'll tell you again. " + motive[3]))

        # set last persons that user asked about
        data["last_spoken_about_character"] = characters
        print("Data: ", data)

        return [SlotSet("data", data)]
