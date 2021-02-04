import datetime
import abc


class Game(abc.ABC):

    def __init__(self, game_id: int, start_time: datetime.datetime, end_time: datetime.datetime):

        self._game_id = game_id
        self._start_time = start_time
        self._end_time = end_time

    @property
    def game_id(self) -> int:
        return self._game_id

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self._end_time
