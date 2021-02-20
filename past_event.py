import datetime

import event
import event_mode
import database_player


class PastEvent(event.Event):

    def __init__(self, mode: event_mode.EventMode, creator: database_player.DATABase_Player, start_time: datetime.datetime, end_time: datetime.datetime):
        super().__init__(mode, creator)

        self._start_time = start_time
        self._end_time = end_time


    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self._end_time
