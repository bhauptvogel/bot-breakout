
def guess_murderer(data, person):
    if "user_wants_to_commit" not in data:
        data["user_wants_to_commit"] = True
        return f" So you think {person} is the murderer. <br>Interesting choice!💫 Thanks for clearing my mind. You can still ask me for an <b>overview</b> of what we talked about. Let's go now and look for the police to tell them our suspect...👀 <br><br> <p style='font-family: georgia;'><b>[Police Officer👮‍♂️]</b> Hey, I'm police officer Kramer. I heard about the dead body you found. Is there anything you want to tell me? Who do you suspect? 🧐 </p>"
    elif data["user_wants_to_commit"] == True:
        data["user_wants_to_commit"] = False
        if person == "Patrick":
            output = "<p style='font-family: georgia;'>[Police officer👮‍♂️] Haha seams like you already did my Job!🤩 We will check all the details and talk to you after we are done. Please leave some of your informations to my colleage. Possible, that we will be in touch sone. But for now you can go home.</p><br>"
            output += "After a hot investigation the police found multiple hints to claim Patrick for corruption. Your perfect Hint was very helpful and leaded to Patrick being in jail very quick.🔗 You should consider a career as an detective. Great job!🥳 Your Date is impressed too and asks for another Date. Maybe you will solve a theft next time!💞<br>"
            output += "<h1>You won the game!✅</h1> <br>Congratulations!🎉"
            data['blocked'] = {
                "action_character_investigation": "game_over_blocked",
                "action_user_guess": "game_over_blocked",
                "action_give_hint": "game_over_blocked",
                "action_tell_motive": "game_over_blocked",
                "action_overview_of_the_state": "game_over_blocked",
                "action_access_to_roller_coaster": "game_over_blocked",
                "action_scene_investigation": "game_over_blocked",
                "validate_simple_cabin_form": "game_over_blocked",
                "action_cabin_end": "game_over_blocked",
                "action_cabin_start": "game_over_blocked",
                "action_set_reminder": "game_over_blocked",
                "action_react_to_reminder": "game_over_blocked",
                "action_you_cannot_leave": "game_over_blocked",
                "action_ask_about_mika": "game_over_blocked",
                "action_who_is_the_murderer": "game_over_blocked",
                "action_cabin_validation": "game_over_blocked",
            }
            data["won"] = True
            return output
        else:
            output = f"<p style='font-family: georgia;'>[Police officer👮‍♂️] So you already did my job. We talked with {person} before we arrived. Maybe I should talk to you two bit more because {person} has an alibi...🫣 Maybe on the Police Station. Hendrick! Handcuff these two, they are suspiscious.🤨</p><br>"
            output = f"After a hot investigation, the Police concluded that {person} is innocent. Your were hold at the police station for a couple of hours and are now drained. But you had a lot of time to get to know your Date in ✨jail✨. Detective work seams not to be your secret talent... <br>"
            output += "<h1>You lost the game!❌</h1> <br>Better luck next time!🍀"
            data['blocked'] = {
                "action_character_investigation": "game_over_blocked",
                "action_user_guess": "game_over_blocked",
                "action_give_hint": "game_over_blocked",
                "action_tell_motive": "game_over_blocked",
                "action_overview_of_the_state": "game_over_blocked",
                "action_access_to_roller_coaster": "game_over_blocked",
                "action_scene_investigation": "game_over_blocked",
                "validate_simple_cabin_form": "game_over_blocked",
                "action_cabin_end": "game_over_blocked",
                "action_cabin_start": "game_over_blocked",
                "action_set_reminder": "game_over_blocked",
                "action_react_to_reminder": "game_over_blocked",
                "action_you_cannot_leave": "game_over_blocked",
                "action_ask_about_mika": "game_over_blocked",
                "action_who_is_the_murderer": "game_over_blocked",
                "action_cabin_validation": "game_over_blocked",
            }
            data["won"] = False
            return output
    else:
        print("ERROR: this should not happen, look into end_of_game.py")
        return "Game is over. You can't do anything anymore. If you want to restart, leave the room and join back in."
        