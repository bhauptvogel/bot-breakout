from datetime import datetime
from datetime import datetime, timedelta
from rasa_sdk.events import SlotSet
from utils.game_parameters import GameParams
from rasa_sdk.executor import CollectingDispatcher
from utils.formatting import utter

def set_timer(dispatcher: CollectingDispatcher, data: dict):
    if "timercount" not in data.keys():
        return [SlotSet("data", data)]
    if data['timercount'] == 1:
        data['timercount'] = 2
        timestamp = datetime.now()
        timer = timestamp + timedelta(seconds=(GameParams.game_time_seconds/3))
        updated_timestamp = timer.timestamp()
        data['timer'] = updated_timestamp
        if "hint_given" in data.keys() and not data["hint_given"]:
            utter(dispatcher=dispatcher, text="Remember that you can also ask for a hint ✨")
        return [SlotSet("data", data)]
    elif data["timercount"] == 2:
        data['timercount'] = 3
        timestamp = datetime.now()
        timer = timestamp + timedelta(seconds=(GameParams.game_time_seconds/3))
        updated_timestamp = timer.timestamp()
        data['timer'] = updated_timestamp
        utter(dispatcher=dispatcher, text= "We have 3 more minutes until the police arrives. We need to hurry!⏰ Maybe ask for a hint, I can check if there is something important that we have not talked about.")
        return [SlotSet("data", data)]
    else:
        data['blocked'] = {
            "action_character_investigation": "end_of_game_blocked",
            "action_user_guess": "",
            "action_give_hint": "end_of_game_blocked",
            "action_tell_motive": "end_of_game_blocked",
            "action_overview_of_the_state": "",
            "action_access_to_roller_coaster": "end_of_game_blocked",
            "action_scene_investigation": "end_of_game_blocked",
            "validate_simple_cabin_form": "end_of_game_blocked",
            "action_cabin_end": "end_of_game_blocked",
            "action_cabin_start": "end_of_game_blocked",
            "action_set_reminder": "end_of_game_blocked",
            "action_react_to_reminder": "end_of_game_blocked",
            "action_you_cannot_leave": "end_of_game_blocked",
            "action_ask_about_mika": "end_of_game_blocked",
            "action_who_is_the_murderer": "end_of_game_blocked",
            "action_cabin_validation": "end_of_game_blocked",
        }
        
        utter(dispatcher=dispatcher, text="The Time is over. ⏰ The police waits outside, we need to go and tell them our suspect. By the way, who do suspect?👀 Please tell me a name.")
        return [SlotSet("data", data)]

def check_timer(data: dict):
    if "timer" not in data or "won" in data:
        return
    elif data['timer'] >= datetime.now().timestamp():
        return False
    else:
        return True

def check_timer(dispatcher: CollectingDispatcher, data: dict):
    if "timer" not in data or "won" in data:
        return [SlotSet("data", data)]
    elif data['timer'] >= datetime.now().timestamp():
        return [SlotSet("data", data)]
    else:
        return set_timer(dispatcher, data)