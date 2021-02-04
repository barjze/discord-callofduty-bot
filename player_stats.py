import dataclasses
import datetime


@dataclasses.dataclass
class PlayerStats:
    timestamp: datetime.datetime
    kd: float
    wins: int
    kills: int
    games_played: int
    weekly_kd: float
    win_percentage: float
    delta_kd: float
    delta_weekly_kd: float
    delta_last_kd: float
