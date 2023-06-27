from dataclasses import dataclass

@dataclass
class GameArgs:
    formatting: bool = True         # True when deploying in frontend
    game_time_seconds: int = 60     # 420 in final game