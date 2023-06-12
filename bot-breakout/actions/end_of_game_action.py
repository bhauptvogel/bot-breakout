from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random
from . import information_interface as ii


PERCENTAGE_THRESHOLD = 0.45

REQUIRED_GAME_STATES = [
    "character_information/Maria",
    "character_information/Anna",
    "character_information/Patrick",
    "character_information/Kira",
    "scene_investigation/base_1",
    "scene_investigation/cabin",
    "scene_investigation/body",
    "scene_investigation/knife",
    "motive/Maria",
    "motive/Anna",
    "motive/Patrick",
    "motive/Kira",
    "access/Maria",
    "access/Anna",
    "access/Patrick",
    "access/Kira",
]

class UserGuessesMurderer(Action):
    def name(self) -> Text:
        return "action_user_guess"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot("data") is None or tracker.get_slot("data") == "Null":
            data = {}
        else:
            data = tracker.get_slot("data")

        entities = tracker.latest_message["entities"]
        person = [e["value"] for e in entities if e["entity"] == "person"]
        
        # ! hack for the case that the "Maria" entity is in persons (f.e. "Did Kira kill Maria?")
        if len(person) == 2 and "Maria" in person:
                # person is the other person
                person = [p for p in person if p != "Maria"]

        if len(person) > 1:
            dispatcher.utter_message(text="So who do you think it is? I'm confused.")
            return [SlotSet("data", data)]

        if "times_wanted_to_guess_murderer" not in data:
            data["times_wanted_to_guess_murderer"] = 0

        if "story_state" not in data:
            data["story_state"] = {}

        false_count = 0
        for state in REQUIRED_GAME_STATES:
            keys = state.split("/")
            temp_data = data["story_state"]

            for key in keys:
                if key in temp_data:
                    temp_data = temp_data[key]
                else:
                    false_count += 1
                    break

        true_count = len(REQUIRED_GAME_STATES) - false_count
        true_percentage = true_count / (true_count + false_count)

        # TODO (#23): Rewrite end
        if true_percentage > PERCENTAGE_THRESHOLD:
            if data["times_wanted_to_guess_murderer"] == 0:
                dispatcher.utter_message(
                    text="Are you sure? Maybe, but I'm not sure about that. Let's check the clues we have! Type watch overview. Then tell me who you think is the murderer."
                )
                data["times_wanted_to_guess_murderer"] += 1
            elif "user_wants_to_commit" not in data:
                dispatcher.utter_message(
                    text="Alright, thanks for clearing my mind. I'm not a hundred percent sure but I trust you. Let's go now and look for the police to tell them... We have to be right here! \n\n [Police Officer] Hey, I'm police officer Kramer. I heard about the dead body you found. Is there anything you want to tell me? Who do you suspect?"
                )
                data["user_wants_to_commit"] = True
            elif data["user_wants_to_commit"] == True:
                data["user_wants_to_commit"] = False
                if person[0] == "Patrick":
                    dispatcher.utter_message(
                        "Haha seams like you already did my Job! We will check all the details and talk to you after we are done. Please leave some of your informations to my colleage. Possible, that we will be in touch sone. But for now you can leave.\n"
                    )
                    dispatcher.utter_message(
                        "After a hot investigation the police found multiple hints to claim Patrick for corruption. Your perfect Hint was very helpful and leaded to Patrick being in jail very quick. Police work is your ambition. Great job. Your Date is impressed too and ask for another Date. Maybe you will solve a theft this time!"
                    )
                    dispatcher.utter_message("You won the game! Congratulations!")
                    # end game

                else:
                    dispatcher.utter_message(
                        f"So you already did my job. We talked with {person[0]} before we arrived. They have an alibi... maybe I should talk to you two bit more. Maybe on the Police Station. Hendrick! Handcuff these two, they are suspiscious.\n"
                    )
                    dispatcher.utter_message(
                        f"After a hot investigation, the Police that {person[0]} is innocent. Your were hold at the police station for a couple of hours and are now drained. But you had a lot of time to get to know your Date in jail. Police work seams not to be your secret talent. \n"
                    )
                    dispatcher.utter_message(
                        "You lost the game! Better luck next time!"
                    )
            else:
                dispatcher.utter_message(
                    text="Game is over. You can't do anything anymore."
                )
        else:
            dispatcher.utter_message(
                text="We can’t leave before the police arrives in a few minutes! You need to know more about this story to be sure. Let's find more hints together, so they don’t think we two did it. We need to check for a motive, if the suspect had access and the murder weapon!"
            )

        return [SlotSet("data", data)]
