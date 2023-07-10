from utils import end_of_game

def get_blocked_message(data, blocked_key): 
    if blocked_key == "cabin_blocked":
        return "We have to open the cabin first! Its not that, hard try again.🎲 Maybe I remember something and give you a hint while guessing the pin code.😉"
    elif blocked_key == "end_of_game_blocked":
        return "We dont have time anymore!⏰ The police waits outside, please tell me who you suspect? <br>Type in a name."
    elif blocked_key == "game_over_blocked":
        # TODO: Add emojis
        if data["won"] == True:
            return "The game is over! <b>You won.</b>✅ <br>Congratulations!🎉 If you leave the game and join back in you progress will be lost and you can start again😊"
        elif data["won"] == False:
            return "The game is over! <b>You have lost.</b>❌ <br>You can leave the room and join back in to give it another shot! Maybe next time you find the murderer😊"
    elif blocked_key == "no_greet_yet":
        return "<span style='font-family: georgia;'>Hoppla, there went something wrong. Please ask how mika is doing to start.</span>"
        