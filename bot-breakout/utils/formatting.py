from rasa_sdk.executor import CollectingDispatcher
from utils.game_parameters import GameParams

# NOT in frontend deployment
if GameParams.formatting == False:
    from bs4 import BeautifulSoup
    from html import unescape

formattings = {
    "Maria": "<b style='color: FireBrick;'>Maria</b>",
    "Sterling": "<b><em style='color: FireBrick;'>Sterling</em></b>",
    "Kira": "<b style='color: DarkMagenta;'>Kira</b>",
    "Russell": "<b><em style='color: DarkMagenta;'>Russell</em></b>",
    "Victor": "<b style='color: Navy;'>Victor</b>",
    "Lopez": "<b><em style='color: Navy;'>Lopez</em></b>",
    "Anna": "<b style='color: DarkOrange;'>Anna</b>",
    "Pollock": "<b><em style='color: DarkOrange;'>Pollock</em></b>",
    "Patrick": "<b style='color: Olive;'>Patrick</b>",
    "Anyang": "<b><em style='color: Olive;'>Anyang</em></b>",
    "Mika": "<b style='color: DarkSlateGray;'>Mika</b>",
}

font_family = "font-family: verdana;"

# ONLY use this function to send messages to the user
def utter(dispatcher: CollectingDispatcher, text: str) -> None:
    if GameParams.formatting == False:
        # remove html tags
        text = text.replace("<br>", "\n")
        soup = BeautifulSoup(text, "html.parser")
        text = unescape(soup.get_text())
    else:
        for key, value in formattings.items():
            text = text.replace(key, value)

        text = f"<p style='{font_family}'>{text}</p>"

    dispatcher.utter_message(text=text)