import event_mode
import player


class Event:

    def __init__(self, mode: event_mode.EventMode, creator: player.Player):
        self._mode = mode
        self._creator = creator

    @property
    def mode(self) -> event_mode.EventMode:
        return self._mode

    @property
    def creator(self) -> player.Player:
        return self._creator
