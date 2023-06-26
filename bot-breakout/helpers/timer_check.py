from datetime import datetime
from datetime import datetime, timedelta
from rasa_sdk.events import SlotSet

def check_timer(data):
    if "timer" not in data.keys():
        return 
    if data['timer'] >= datetime.now().timestamp():
        return False
    else:
        return True

def set_timer(data):
    if "timercount" not in data.keys():
        return
    if data['timercount'] > 1:
        blocked = {
            "action_character_investigation": "end_of_game_blocked",
            "action_user_guess": "",
            "action_give_hint": "end_of_game_blocked",
            "action_tell_motive": "end_of_game_blocked",
            "action_overview_of_the_state": "",
            "action_access_to_roller_coaster": "end_of_game_blocked",
            "action_scene_investigation": "end_of_game_blocked",
            "validate_simple_cabin_form": "end_of_game_blocked",
            "action_cabin_end": "end_of_game_blocked",
            "action_cabin_start": "end_of_game_blocked"
        }
        
        data['blocked'] = blocked
        SlotSet('data',data)
        return "The police is here, we need to tell them who the murderer is!"
    else:
        data['timercount'] = 2
        timestamp = datetime.now()
        timer = timestamp + timedelta(seconds=20)
        #timer = timestamp + timedelta(seconds=180)
        updated_timestamp = timer.timestamp()
        data['timer'] = updated_timestamp
        return "We have 3 more minutes until the police arrives. We need to hurry!"