from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ReminderScheduled

from datetime import datetime, timedelta
import random

from actions.actions import INITIAL_DATA_OBJECT


class CharacterInvestigation(Action):
    def name(self) -> Text:
        return "action_character_investigation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        characters = [e['value'] for e in entities if e['entity'] == 'person']
        informations = [e['value'] for e in entities if e['entity'] == 'information']
        cowoker_set = False

        if len(entities) > 0 and "group" in entities[0].keys():
            coworker = [e['value'] for e in entities if e['group'] == 'multiple' and e['entity'] == 'person']
            cowoker_set = True
     
        

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = INITIAL_DATA_OBJECT
        else:
            data = tracker.get_slot('data')


        story_characters = {"Maria": {1 : "Maria is the Ex-girlfriend of my co-worker Kira. Do you want to know more about Kira or should we investigate the cabin a bit more?"}, 
                            "Kira" : {1 : "Kira is my co-worker. We are pretty good... I helped her to get through the breakup with Maria. That really took her down she was super upset - specially because of Marias new boyfriend.", 2: "Information 2 about Kira"}, 
                            "Patrick": {1 : "Patrick is my boss. He in charge of the amusement park. Its actually a family business, he earned it from his dad. Patrick is kind of a snob... he loves to drive around in big cars and all this wealthy stuff.", 2: "Information 2 about Patrick"}, 
                            "Victor": {1 : "To be honest... I don’t know him. He is just Marias new boyfriend 🤷", 2: "Victor is Maria's new boyfriend. I don’t know him. Only the things Kira told me about him. She was pretty jealous, that Maria has someone new 👀"}, 
                            "Anna": {1 : "Anna is Marias colleague at the Fictional Times Paper. I met her at some of Kiras Partys. She is nice but very focused on her job, just as Maria is … sorry, was 😥", 2: "Information 2 about Anna"}}

        story_characters_information = {"breakup": {1: ["Kira", "Maria"], 2: "Kira and Maria were totally in love, but they had heated arguments about Maria working too much. She always wanted to catch the hottest stories and loved to do investigations on her own. She tried to outshine her Colleague Anna. Thats why their relationship broke apart…"},
                                        "secret": {1: ["Patrick"], 2: "Secret about Patrick"},
                                        }
        
        story_character_last_name = {"Maria": {1 : "S."}, 
                            "Kira" : {1 : "R."}, 
                            "Patrick": {1 : "Anyang"}, 
                            "Victor": {1 : "L."}, 
                            "Anna": {1 : "Pollock"}}
        
        
        
         #If they ask about "her", "him", "it" it uses the "last_spoken"
        if len(informations) == 0 and len(characters) == 0:
            print("In not characters not informations")
            if "last_spoken_about_character" in data.keys() and len(data["last_spoken_about_character"]) > 0:
                for last_spoken in data["last_spoken_about_character"]:
                    if "times_asked_about_" + last_spoken not in data:
                        data["times_asked_about_" + last_spoken] = 1
                        dispatcher.utter_message(text=(story_characters[last_spoken][1]))
                    else:
                        data["times_asked_about_" + last_spoken] += 1
                        if data["times_asked_about_" + last_spoken] == 2:
                            if 2 not in story_characters[last_spoken]:
                                dispatcher.utter_message(text=("You already asked me about " + last_spoken + " but sure, her you go: " + story_characters[last_spoken][1]))
                            else:
                                dispatcher.utter_message(text=(story_characters[last_spoken][2]))
                        else:
                            dispatcher.utter_message(text=("You already asked me about " + last_spoken + " but sure, her you go: " + story_characters[last_spoken][1]))
            elif "last_spoken_about_information" in data.keys() and len(data["last_spoken_about_information"]) > 0:
                for character_information in data["last_spoken_about_information"]:
                    if character_information in story_characters_information:
                        dispatcher.utter_message(text=(story_characters_information[character_information][2]))
                    else:
                        dispatcher.utter_message(text=("Sorry, I don't have any information about a "+ character_information + " from "+ "".join(data["last_spoken_about_character"])))

        
        #If information about something character-related is asked
        if len(informations) > 0: 
            print("In informations")
            for info in informations:
                if info == "last name":
                    if len(characters) > 0:
                        for character in characters:
                            dispatcher.utter_message(text=(str(character)+"'s last name is "+str(story_character_last_name[character][1])))
                    elif "last_spoken_about_character" in data.keys():
                        for character in data["last_spoken_about_character"]:
                            dispatcher.utter_message(text=(str(character)+"'s last name is "+str(story_character_last_name[character][1])))
                    else:
                        dispatcher.utter_message(text=("I don't know who you're talking about"))
                elif info == "full name":    
                    if len(characters) > 0:
                        for character in characters:
                            dispatcher.utter_message(text=(character+"'s full name is "+ str(character) + " "+str(story_character_last_name[character][1])))
                    elif "last_spoken_about_character" in data.keys():
                        for character in data["last_spoken_about_character"]:
                            dispatcher.utter_message(text=(character+"'s full name is "+ str(character) + " "+str(story_character_last_name[character][1])))
                    else:
                        dispatcher.utter_message(text=("I don't know who you're talking about"))     

                for character_information in story_characters_information:
                    if len(characters) < 1 and "last_spoken_about_character" not in data.keys():
                        dispatcher.utter_message(text="I don't know what you mean")
                        break
                    elif character_information in informations:
                        if len(characters) > 0: 
                            if set(characters).issubset(story_characters_information[character_information][1]):
                                dispatcher.utter_message(text=(story_characters_information[character_information][2]))
                                data["last_spoken_about_information"] = informations
                                data["last_spoken_about_character"] = []
                        else:
                            if set(data["last_spoken_about_character"]).issubset(story_characters_information[character_information][1]):
                                dispatcher.utter_message(text=(story_characters_information[character_information][2]))
                                data["last_spoken_about_information"] = informations
                                data["last_spoken_about_character"] = []
                                break
                        
                            else:
                                dispatcher.utter_message(text=("Sorry, I don't have any information about a "+ character_information + " from "+ "".join(data["last_spoken_about_character"])))

                


        #If basic information about character is asked
        if len(characters) > 0 and len(informations) == 0 and not cowoker_set:
            print("In characters > 0 informations < 0 coworker == 0")
            for story_character in story_characters:
                if story_character in characters:
                    if "times_asked_about_" + story_character not in data:
                        data["times_asked_about_" + story_character] = 1
                        dispatcher.utter_message(text=(story_characters[story_character][1]))
                    else:
                        data["times_asked_about_" + story_character] += 1
                        if data["times_asked_about_" + story_character] == 2:
                            if 2 not in story_characters[story_character]:
                                dispatcher.utter_message(text=("You already asked me about " + story_character + " but sure, her you go: " + story_characters[story_character][1]))
                            else:
                                dispatcher.utter_message(text=(story_characters[story_character][2]))
                        else:
                            dispatcher.utter_message(text=("You already asked me about " + story_character + " but sure, her you go: " + story_characters[story_character][1]))
            data["last_spoken_about_character"] = characters
            data["last_spoken_about_information"] = []
        
        if len(informations) == 0 and cowoker_set:
            print("In characters > 0 informations < 0 coworker == 0")
            dispatcher.utter_message(text=("My coworkers are Kira, who works as a cashier, and Patrick who is the director of the amusement park. Who do you want to know more about?"))

        
        if "last_spoken_about_information" in data.keys() and "last_spoken_about_character" in data.keys():                   
            dispatcher.utter_message(text=('TODO: Investigate characters: ' + str(characters) + ' / informations: ' + str(informations) + 'last spoken character: ' + str(data["last_spoken_about_character"]) + "last spoken information: " + str(data["last_spoken_about_information"])))
        else:
            dispatcher.utter_message(text=('TODO: Investigate characters: ' + str(characters) + ' / informations: ' + str(informations)))

        return [SlotSet("data", data)]