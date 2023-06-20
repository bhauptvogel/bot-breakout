
def guess_murderer(data, person):
    if "user_wants_to_commit" not in data:
        data["user_wants_to_commit"] = True
        return "Alright, thanks for clearing my mind. I'm not a hundred percent sure but I trust you. Before you tell the police, remember you can always ask me after an overview of the what we talked about. Let's go now and look for the police to tell them... \n\n [Police Officer] Hey, I'm police officer Kramer. I heard about the dead body you found. Is there anything you want to tell me? Who do you suspect?"
    elif data["user_wants_to_commit"] == True:
        data["user_wants_to_commit"] = False
        if person == "Patrick":
            output = "Haha seams like you already did my Job! We will check all the details and talk to you after we are done. Please leave some of your informations to my colleage. Possible, that we will be in touch sone. But for now you can leave.\n"
            output += "After a hot investigation the police found multiple hints to claim Patrick for corruption. Your perfect Hint was very helpful and leaded to Patrick being in jail very quick. Police work is your ambition. Great job. Your Date is impressed too and ask for another Date. Maybe you will solve a theft this time!"
            output += "You won the game! Congratulations!"
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
                "action_cabin_start": "game_over_blocked"
            }
            data["won"] = True
            return output
        else:
            output = f"So you already did my job. We talked with {person} before we arrived. They have an alibi... maybe I should talk to you two bit more. Maybe on the Police Station. Hendrick! Handcuff these two, they are suspiscious.\n"
            output = f"After a hot investigation, the Police that {person} is innocent. Your were hold at the police station for a couple of hours and are now drained. But you had a lot of time to get to know your Date in jail. Police work seams not to be your secret talent. \n"
            output += "You lost the game! Better luck next time!"
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
                "action_cabin_start": "game_over_blocked"
            }
            data["won"] = True
            return output
    else:
        print("ERROR: this should not happen, look into end_of_game.py")
        return "Game is over. You can't do anything anymore."
        