from typing import Tuple, List

import callofduty
import discord

import call_of_duty_handler
import player_stats


class Player:

    def __init__(self, discord_guild: discord.Guild, discord_id: int, game_id: str, platform: callofduty.Platform):
        self._discord_guild = discord_guild
        self._discord_id = discord_id
        self._game_id = game_id
        self._cod_player = None
        self._platform = platform
        self._player_stats: List[player_stats.PlayerStats] = list()

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

    def add_stats(self, stats: player_stats.PlayerStats) -> None:
        if len(self._player_stats) >= 10:
            self._player_stats.pop(0)

        self._player_stats.append(stats)
