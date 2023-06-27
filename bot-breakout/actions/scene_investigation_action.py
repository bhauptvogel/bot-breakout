
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from utils import information_interface as ii
from utils.timer_check import check_timer, set_timer
from utils.blocked_message import get_blocked_message
from utils.formatting import utter

class SceneInvestigation(Action):
    def name(self) -> Text:
        return "action_scene_investigation"

    def utter_hint_scene_investigation(self, dispatcher, data):
        """
        If the user has already looked around, but not yet at certain objects:
        Give a little hint what to do next.
        """
        NOT_IN_GAME_STATE = {
            "cabin": "I think we should take a look at the cabin.",
            "body": "Now I thinks it is time to take a look at the body.",
            "knife": "We have not yet looked at the knife though.",
        }
        for key in NOT_IN_GAME_STATE:
            if key not in data["story_state"]["scene_investigation"]:
                utter(dispatcher,text=NOT_IN_GAME_STATE[key])
                return
        if "character_investigation" not in data["story_state"]:
            utter(dispatcher,text="I think we should talk about my coworkers.")
            return

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        if "blocked" in data and data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            return [SlotSet("data", data)]


        if 'cabin_open' not in data.keys():
            cabin_open = False
        else:
            cabin_open = data['cabin_open']

        entities = tracker.latest_message['entities']
        objects = [e['value'] for e in entities if e['entity'] == 'object']

        if len(objects) == 0:
            utter(dispatcher,text=ii.get_story_information("scene_investigation", "", data))
            # if alrealy asked about scene_investigation: talk about stuff that is not yet explored
            if "base_2" in data["story_state"]["scene_investigation"]:
                self.utter_hint_scene_investigation(dispatcher, data)

        for obj in objects:
            objects_inside_cabin = ['body', 'weapon', 'knife', 'note', 'cabin']
            if obj in objects_inside_cabin and not cabin_open:
                obj = "no_access"

            if obj in ii.get_story_objects():
                utter(dispatcher,text=ii.get_story_information("scene_investigation", obj, data))
            else:
                # TODO: If User has not yet looked around: "I could look around and tell you what I see."
                utter(dispatcher,text=f"Sorry, I don't know what {obj} is.")

        if check_timer(data):
            utter(dispatcher,text=set_timer(data))

        return [SlotSet("data", data)]


# Start the cabin riddle
class CabinStart(Action):
    def name(self) -> Text:
        return "action_cabin_start"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')

        if 'cabin_open' not in data.keys():
            cabin_open = False
        else:
            cabin_open = data['cabin_open']

        data['cabin_riddle_started'] = True

        if "blocked" in data and data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            if check_timer(data):
                utter(dispatcher,text=set_timer(data))
            return [SlotSet("data", data)]

        block = {
            "action_character_investigation": "cabin_blocked",
            "action_user_guess": "cabin_blocked",
            "action_give_hint": "cabin_blocked",
            "action_tell_motive": "",
            "action_overview_of_the_state": "",
            "action_access_to_roller_coaster": "cabin_blocked",
            "action_scene_investigation": "cabin_blocked",
            "validate_simple_cabin_form": "",
            "action_cabin_end": "",
            "action_cabin_start": "",
            "action_set_reminder": "cabin_blocked",
            "action_react_to_reminder": "",
            "action_you_cannot_leave": "cabin_blocked",
            "action_ask_about_mika": "cabin_blocked",
            "action_who_is_the_murderer": "cabin_blocked",
            "action_cabin_validation": "",

        }

        if cabin_open:
            utter(dispatcher,text="It has two seats, just like ours. On the seat closer to us is Maria's corpse. She is covered in blood and a note is pinned to her chest. I don’t see why and how she died... The floor also looks messy. I see something in the puddles. It's a knife! It's strange to grab in blood, but I'll get it out. I could take a closer look at it.")
        else:
            data["blocked"] = block
            utter(dispatcher,text="We are now standing in front of the train cabin with the dead body. But Damn... the door is locked, and I can't get in. All cabins are locked with a 3-digit pin code. I set those after a rough workday... I don't know the solution but I work with a specific system. I subtract the fourth prime number from the cabin number, added 2 and divide it by 2. I think the cabin number of this cabin is 686. Can you help me find the right pin code to enter the cabin? Just tell me the 3-digit pin code I should try!")

        if check_timer(data):
            utter(dispatcher,text=set_timer(data))

        return [SlotSet("data", data)]

class CabinPinValidation(Action):
    def name(self) -> Text:
        return "action_cabin_validation"

    def cabin_end(self, data):

            data['cabin_open'] = True
            data['cabin_riddle_started'] = False

            block = {
                "action_character_investigation": "",
                "action_user_guess": "",
                "action_give_hint": "",
                "action_tell_motive": "",
                "action_overview_of_the_state": "",
                "action_access_to_roller_coaster": "",
                "action_scene_investigation": "",
                "validate_simple_cabin_form": "",
                "action_cabin_end": "",
                "action_cabin_start": "",
                "action_set_reminder": "",
                "action_react_to_reminder": "",
                "action_you_cannot_leave": "",
                "action_ask_about_mika": "",
                "action_who_is_the_murderer": "",
                "action_cabin_validation": "",
            }
            data["blocked"] = block

            ii.set_game_state("scene_investigation", "cabin", data)

            return [SlotSet("data", data)]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        if 'cabin_guess' not in data.keys():
            data['cabin_guess'] = 1

        if 'cabin_number_guess' not in data.keys():
            data['cabin_number_guess'] = False
        
        if "blocked" in data and data["blocked"][self.name()] != "":
            utter(dispatcher,text=get_blocked_message(data,data["blocked"][self.name()]))
            if check_timer(data):
                utter(dispatcher,text=set_timer(data))
            return [SlotSet("data", data)]


        cabin_password = tracker.latest_message['entities'][0]['value']

        if 'cabin_riddle_started' in data.keys() and data['cabin_riddle_started']:

            if cabin_password == "492":
                utter(dispatcher,text="Yes "+cabin_password+" worked. We can enter the cabin. It has two seats, as ours did. On the seat closer to us is Maria's body. She is covered in blood and a note is pinned to her chest. I don’t see why and how she died... The floor also looks messy. I see something in the puddles. It's a knife! It's strange to grab in blood, but I'll get it out. I could take a closer look at it.")
                self.cabin_end(data)
                if check_timer(data):
                    utter(dispatcher,text=set_timer(data))
                return [SlotSet('data', data)]
            if cabin_password == "989" and not data['cabin_number_guess']:
                utter(dispatcher,text="This is not the password. But 989 is the right cabin number, sorry for the confusion.")
                data['cabin_number_guess'] = True
                data['cabin_guess'] += 1
                if check_timer(data):
                    utter(dispatcher,text=set_timer(data))
                return [SlotSet('data', data)]

            if data['cabin_guess'] == 1:
                data['cabin_guess'] += 1
                utter(dispatcher,text="No, it is not "+cabin_password)
            elif data['cabin_guess'] == 2:
                data['cabin_guess'] += 1
                utter(dispatcher,text="It is also not "+cabin_password)
            elif data['cabin_guess'] == 3:
                utter(dispatcher,text="Nope, not right. Maybe look at the 686 ANOTHER WAY...")
                data['cabin_guess'] += 1
            elif data['cabin_guess'] == 4:
                utter(dispatcher,text="Nope unfortunately not "+cabin_password)
                data['cabin_guess'] += 1
            elif data['cabin_guess'] == 5:
                if not data['cabin_number_guess']:
                    utter(dispatcher,text="It is not "+cabin_password+". Oh I see now... the cabin number is 989")
                else:
                    utter(dispatcher,text= ""+cabin_password +" is not the pin. It should be (989 - 7 + 2) / 2.")
                data['cabin_guess'] += 1
            else:
                utter(dispatcher,text= ""+cabin_password +" is not the pin. It should be (989 - 7 + 2) / 2.")
                data['cabin_guess'] += 1

        else:
            utter(dispatcher,text="I don't know what you mean by "+cabin_password)

        if check_timer(data):
            utter(dispatcher,text=set_timer(data))

        return [SlotSet('data', data)]
