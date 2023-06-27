from rasa_sdk.executor import CollectingDispatcher
from utils.game_parameters import GameParams

formattings = {
    "Maria": "<b style='color: FireBrick;'>Maria</b>",
    "Sterling": "<b><em style='color: FireBrick;'>Sterling</em></b>",
    "Kira": "<b style='color: Navy;'>Kira</b>",
    "Russell": "<b><em style='color: Navy;'>Russell</em></b>",
    "Victor": "<b style='color: RosyBrown;'>Victor</b>",
    "Lopez": "<b><em style='color: RosyBrown;'>Lopez</em></b>",
    "Anna": "<b style='color: DarkOrange;'>Anna</b>",
    "Pollock": "<b><em style='color: DarkOrange;'>Pollock</em></b>",
    "Patrick": "<b style='color: Olive;'>Patrick</b>",
    "Anyang": "<b><em style='color: Olive;'>Anyang</em></b>",
    "Mika": "<b style='color: DarkSlateGray;'>Mika</b>",
}

font_family = "font-family: baskerville;"

# ONLY use this function to send messages to the user
def utter(dispatcher: CollectingDispatcher, text: str) -> None:
    if GameParams.formatting:
        for key, value in formattings.items():
            text = text.replace(key, value)
        
        text = f"<p style='{font_family}'>{text}</p>"

    dispatcher.utter_message(text=text)