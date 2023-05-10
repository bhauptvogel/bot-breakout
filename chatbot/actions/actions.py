# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import googlesearch 


class ValidateSimpleAgeForm(FormValidationAction):
     def name(self) -> Text:
          return "validate_simple_age_form"

     def validate_age(
               self, 
               slot_value: Any, 
               dispacher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: DomainDict,
     ) -> Dict[Text, Any]: 
          """Validate `age` value."""

          if int(slot_value) != 25:
               #dispacher.utter_message(text=f"That's not right, try again")
               return {"age": None}
          dispacher.utter_message(text=f"Yes! I'm {slot_value} years old")
          return {"age": slot_value}


class ActionLocationSearch(Action):

    def name(self) -> Text:
        return "action_restaurant_search"

    def run(self, dispatcher: CollectingDispatcher,
          tracker: Tracker,
          domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

          location = next(tracker.get_latest_entity_values("location"), None)
          place = next(tracker.get_latest_entity_values("place"), None)

          dispatcher.utter_message(text=f"Perfect let's go to a {place} in {location}! I'll send you the details.")
#          query = str(place)+" in "+str(location)
#          search = googlesearch.search(query)
#          dispatcher.utter_message(f"Query: {query}")
            
#          return []
