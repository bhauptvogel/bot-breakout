from dataclasses import dataclass

@dataclass
class GameParams:
    formatting: bool = False        # True when deploying in frontend
    game_time_seconds: int = 100     # 420 in final game