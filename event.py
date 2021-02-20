import event_mode
import database_player


class Event:

    def __init__(self, mode: event_mode.EventMode, creator: database_player.DATABase_Player):
        self._mode = mode
        self._creator = creator

    @property
    def mode(self) -> event_mode.EventMode:
        return self._mode

    @property
    def creator(self) -> database_player.DATABase_Player:
        return self._creator
