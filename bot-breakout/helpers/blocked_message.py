from helpers import end_of_game

def get_blocked_message(data, blocked_key): 
    if blocked_key == "cabin_locked":
        return "We have to open the cabin first! Until then I can't help you with anything else."
    elif blocked_key == "end_of_game_blocked":
        return "We have to tell the police who the murderer is! I can't help you with anything else."
    elif blocked_key == "game_over_blocked":
        # TODO: Add emojis
        if data["won"] == True:
            return "The game is over! You won. You can't do anything anymore." 
        elif data["won"] == False:
            return "The game is over! You have lost. You can't do anything anymore."
        