from dataclasses import dataclass

@dataclass
class GameParams:
    formatting: bool = True        # True when deploying in frontend
    game_time_seconds: int = 420     # 420 in final game