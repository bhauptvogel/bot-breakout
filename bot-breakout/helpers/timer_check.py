from datetime import datetime
from datetime import datetime, timedelta

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
        return "The police is here, we need to tell them who the murderer is!"
    else:
        data['timercount'] = 2
        timestamp = datetime.now()
        timer = timestamp + timedelta(seconds=180)
        updated_timestamp = timer.timestamp()
        data['timer'] = updated_timestamp
        return "We have 3 more minutes until the police arrives. We need to hurry!"

