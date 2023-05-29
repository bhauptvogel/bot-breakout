
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import random


investigation = {
    'base' : [
              'Ok, so we are standing in the zombie themed area of the ghost ride. In some way it’s a quite romantic area... we earlier shared a seat at the bench with two zombies holding hand. In the background there is a scary tree, with no leaf. We can look at the train cabin, under the bench and behind the tree. Where should we start?',
              'I found a knife at the cabin floor and a pen behind the tree , lets have a closer look… the pen seems to be used by a professional.',
              'This is all we can find here. We can now talk about my co-workers. I get the feeling that they have something to do with it... Do you want to talk about my coworkers?'],
    'knife': 'The Knife... Oh there are initials in it. It says “A.P”  in the knife. Hm, who might it be?',
    'maria': 'Ok, this feels a bit scary to look at a dead body, but it’s the best thing we can do. Let’s move a few steps closer... Hmm, I think I know the dead woman in the cabin.',
    'cabin': 'It has two seats, as ours did. On the seat closer to us and closer to the themed area is the female corpse. She is covered in blood and a note is pinned to her chest. I don’t see why and how she died... The floor also looks messy. Should I investigate it more or should I tell you about the note...',
    'floor cabin': 'The cabin floor is covert in puddles of blood. In between this mess there is a shape... Its strange to grab in blood but I get it out of it.',
    'bench': 'The cabin floor is covert in puddles of blood. In between this mess there is a shape... Its strange to grab in blood but I get it out of it.',
    'tree': 'The tree is a bit scary. It’s a dead tree with no leafs. Behind the tree there is just some light equipment to give the scene a spoky feeling. But... I think there is something, between the synthetic turf.',
    'note': 'There is a Note on the body. It says “Your are next”. I believe it means that I am the target the murderer intends to go after next.',  
}
              

class SceneInvestigation(Action):
    def name(self) -> Text:
        return "action_scene_investigation"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        if tracker.get_slot('data') is None or tracker.get_slot('data') == 'Null':
            data = {}
        else:
            data = tracker.get_slot('data')
        
        entities = tracker.latest_message['entities']
        objects = [e['value'] for e in entities if e['entity'] == 'object']

        if len(objects) == 0:
            if 'times_asked_about_scene_invesigation' not in data:
                data['times_asked_about_scene_invesigation'] = 0
            elif data['times_asked_about_scene_invesigation'] + 1 < len(investigation['base']):
                data['times_asked_about_scene_invesigation'] += 1
            dispatcher.utter_message(text=investigation['base'][data['times_asked_about_scene_invesigation']])

        for obj in objects:
            if obj in investigation:
                dispatcher.utter_message(text=investigation[obj])
            else:
                dispatcher.utter_message(text="What do you mean with " + obj + "?")

        return [SlotSet("data", data)]