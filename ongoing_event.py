import datetime

import event
import event_mode
import player


class OngoingEvent(event.Event):

    def __init__(self, mode: event_mode.EventMode, creator: player.Player, start_time: datetime.datetime):
        super().__init__(mode, creator)

        self._start_time = start_time

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time
