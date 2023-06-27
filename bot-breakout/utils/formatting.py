from rasa_sdk.executor import CollectingDispatcher
from utils.game_parameters import GameArgs

formattings = {
    "Maria": "<b style='color: FireBrick;'>Maria</b>",
    "Kira": "<b style='color: Navy;'>Kira</b>",
    "Victor": "<b style='color: RosyBrown;'>Victor</b>",
    "Anna": "<b style='color: DarkOrange;'>Anna</b>",
    "Patrick": "<b style='color: Olive;'>Patrick</b>",
    "Mika": "<b style='color: DarkSlateGray;'>Mika</b>",
}

def utter(dispatcher: CollectingDispatcher, text: str):
    if GameArgs.formatting:
        for key, value in formattings.items():
            text = text.replace(key, value)
        
    dispatcher.utter_message(text=text)