from typing import Tuple, List
from main import players
import callofduty
import discord

import call_of_duty_handler
import player_stats


class DATABase_Player:

    def __init__(self, discord_guild: discord.Guild, discord_id: int, game_id: str, platform: callofduty.Platform, player_stats_list, name_in_game: str):
        self._discord_guild = discord_guild
        self._discord_id = discord_id
        self._game_id = game_id
        self._name_in_game = name_in_game
        self._cod_player = None
        self._platform = platform
        self._player_stats: List[player_stats.PlayerStats] = player_stats_list

    @property
    def discord_guild(self) -> discord.Guild:
        return self._discord_guild

    @property
    def discord_id(self) -> int:
        return self._discord_id

    @property
    def discord_member(self) -> discord.Member:
        return self.discord_guild.get_member(self.discord_id)

    @property
    def platform(self) -> callofduty.Platform:
        return self._platform

    @property
    def discord_name(self) -> str:
        return self.discord_member.display_name

    @property
    def game_id(self) -> str:
        return self._game_id

    @property
    def name_in_game(self) -> str:
        return self._name_in_game

    def _set_cod_player(self) -> None:
        self._cod_player = await call_of_duty_handler.get_cod_client().GetPlayer(self.platform, self.game_id)

    @property
    def cod_player(self) -> callofduty.Player:
        if self._cod_player is None:
            self._set_cod_player()

        return self._cod_player

    @property
    def stats(self) -> Tuple[player_stats.PlayerStats]:
        return tuple(self._player_stats)

    def change_name_in_game(self, name_in_game):
        self._name_in_game = name_in_game
        self._change_name_in_game_in_database()


    def last_stats(self):
        return self._player_stats[-1]

    def change_game_id_and_platform(self, game_id: str, platform: callofduty.Platform):
        self._platform = platform
        self._game_id = game_id
        self._change_game_id_in_database()
        self._change_Platform_in_database()


    def add_stats(self, stats: player_stats.PlayerStats) -> None:
        if self.last_stats().timestamp.day == stats.timestamp.day:
            stats._set_deltas_kds(self._calculate_deltas_kd)
            self._player_stats[-1] = stats
            self._change_player_stats_in_database()
            return
        if len(self._player_stats) >= 10:
            stats._set_deltas_kds(self._calculate_deltas_kd)
            self._player_stats.pop(0)
        self._player_stats.append(stats)
        self._change_player_stats_in_database()

    def _calculate_deltas_kd(self, stats):
        if self.last_stats().timestamp.day == stats.timestamp.day:
            delta_kd = stats.kd - self._player_stats[-2].kd
            delta_weekly_kd = stats.weekly_kd - self._player_stats[-2].weekly_kd
        else:
            delta_kd = stats.kd - self._player_stats[-3].kd
            delta_weekly_kd = stats.weekly_kd - self._player_stats[-3].weekly_kd
        delta_last_kd = stats.kd - self._player_stats[-1].kd
        delta_last_weekly_kd = stats.weekly_kd - self._player_stats[-1].weekly_kd
        return delta_kd, delta_weekly_kd, delta_last_kd, delta_last_weekly_kd

    def _change_game_id_in_database(self):
        myquery = {"discordid": self.discord_id}
        newvalues = {"$set": {"Game-id": self.Game_id}}
        players.update_one(myquery, newvalues)

    def _change_Platform_in_database(self):
        myquery = {"discordid": self.discord_id}
        newvalues = {"$set": {"Platform": self.Platform}}
        players.update_one(myquery, newvalues)

    def _change_player_stats_in_database(self):
        myquery = {"discordid": self.discord_id}
        newvalues = {"$set": {"info": self._player_stats}}
        players.update_one(myquery, newvalues)

    def _change_name_in_game_in_database(self):
        myquery = {"discordid": self.discord_id}
        newvalues = {"$set": {"info": self._name_in_game}}
        players.update_one(myquery, newvalues)