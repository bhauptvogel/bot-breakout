def get_locked_message(blocked_key): 
    if blocked_key == "cabin_locked":
        return "We have to open the cabin first! Until then I can't help you with anything else."
    elif blocked_key == "end_locked":
        return "We have to tell the police who the murderer is! I can't help you with anything else."