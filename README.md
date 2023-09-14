# Escape Room Chatbot Challenge
## Project Description
In collaboration between Technical University Berlin and University of Magdeburg, we initiated a project to develop a chatbot that simulates an escape room game. This project aims to offer an interactive user experience, which encouraged us in learning the RASA Framework, interactive chat design, implementation, and user experience engineering.

## Game Concept
Inspired by the classic board game "Cluedo", our chatbot immerses players in a thrilling narrative where they need to solve a murder mystery in an amusement park, accompanied by their virtual date, Mika. Players are challenged to find out who the murderer is by considering clues about the weapon and the motive behind the crime before the police arrive in 10 minutes, promoting a sense of urgency.

Players have the freedom to choose their path, ask different questions, and explore various narrative arcs. The questions and responses are grouped into various categories like character information, motives, crime scene access, and relationships.

## Technical Framework
The project is built on the [RASA Framework](https://rasa.com/), a tool that facilitates the development of chatbots and conversational AI systems through machine learning and natural language processing. The central component is the [`domain.yml`](https://github.com/bhauptvogel/bot-breakout/blob/main/bot-breakout/domain.yml) file which contains basic information and defines the intents representing different user goals. The [`nlu.yml`](https://github.com/bhauptvogel/bot-breakout/blob/main/bot-breakout/data/nlu.yml) file helps in classifying user inputs and extracting essential information or entities. The chatbot maintains context through slots and ensures meaningful interactions using a combination of text responses and programmed logic in Python classes, defined in the [`rules.yml`](https://github.com/bhauptvogel/bot-breakout/blob/main/bot-breakout/data/rules.yml) file and action server.

## How to Play
The adventure begins with the first message introducing the story. Players interact with the chatbot to gather clues, explore surroundings, and solve the mystery before time runs out.

## Acknowledgements
Special thanks to the [Quality and Usability Lab](https://www.tu.berlin/qu), the Technical University Berlin and the University of Magdeburg for their guidance and support throughout the project.
