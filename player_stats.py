import dataclasses
import datetime
import enum
from typing import Type

import discord
from avoid_loop_import import get_channel_by_name

LFG_CHANNEL = "bot-lfg"
STATS_CHANNEL = "bot-stats"
STATS_THUMBNAIL_URL = 'https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg'


@dataclasses.dataclass
class PlayerStats:
    timestamp: datetime.datetime
    kd: float
    wins: int
    kills: int
    games_played: int
    weekly_kd: float
    win_percentage: float
    delta_kd: float = 0.0
    delta_last_kd: float = 0.0
    delta_weekly_kd: float = 0.0
    delta_last_weekly_kd: float = 0.0

    def export_for_db(self):
        return {
            "kd" : self.kd,
            "wins" : self.wins,
            "kills" : self.kills,
            "gamesPlayed" : self.games_played,
            "kdweekly" : self.weekly_kd,
            "winprecent" : self.win_percentage,
            "delta_kd" : 0.01,
            "delta_last_kd": self.delta_last_kd,
            "delta_weekly_kd" : self.delta_weekly_kd,
            "delta_last_weekly_kd" : self.delta_last_weekly_kd,
            "time" : self.timestamp


        }

    def set_deltas_kds(self, delta_kd, delta_weekly_kd, delta_last_kd, delta_last_weekly_kd):
        self.delta_kd = delta_kd
        self.delta_last_kd = delta_last_kd
        self.delta_weekly_kd = delta_weekly_kd
        self.delta_last_weekly_kd = delta_last_weekly_kd

    async def stats_massage_form(self, member: discord.Member, lfg_stats: str, massage_to_delete=None):
        if lfg_stats == 'lfg':
            Channel = get_channel_by_name(LFG_CHANNEL)
            title = "Looking For Group!"

        if lfg_stats == 'stats':
            Channel = get_channel_by_name(STATS_CHANNEL)
            title = "Stats"


        if massage_to_delete is not None:
            await discord.Message.delete(massage_to_delete)

        win_percentage = str(self.win_percentage)
        kd = str(self.kd)
        delta_kd = ' (' + str(self.delta_kd) + ')' + ' (' + str(self.delta_last_kd) + ')'
        kd_with_delta = kd + delta_kd
        weekly_kd = str(self.weekly_kd)
        deltas_weekly_kd = ' (' + str(self.delta_last_weekly_kd) + ') (' + str(self.delta_weekly_kd) + ')'
        weekly_kd_with_deltas = weekly_kd + deltas_weekly_kd

        botfrom = discord.Embed(title=member.display_name + title, description="", color=0x00ff00)
        botfrom.add_field(name="KD(today)(last-time): ", value=kd_with_delta, inline=False)
        botfrom.add_field(name="Weekly KD(today)(last-time): ", value=weekly_kd_with_deltas, inline=False)
        botfrom.add_field(name="Wins: ", value=self.wins, inline=False)
        botfrom.add_field(name="Games Played: ", value=self.games_played, inline=False)
        botfrom.add_field(name="Win Percentage: ", value=win_percentage + '%', inline=False)
        botfrom.add_field(name="Kills: ", value=self.kills, inline=False)
        botfrom.set_thumbnail(url=STATS_THUMBNAIL_URL)
        await Channel.send(embed=botfrom)


class ModeType(enum.Enum):
    BattleRoyal = 'br'
    BattleRoyalSolo = 'br_brsolo'
    BattleRoyalDuos = 'br_brduos'
    BattleRoyalTrios = 'br_brtrios'
    BattleRoyalQuads = 'br_brquads'


class Property(enum.Enum):
    KDRatio = 'kdRatio'
    Wins = 'wins'
    Kills = 'kills'
    Deaths = 'deaths'
    GamesPlayed = 'gamesPlayed'


def get_stat_for_profile(profile: dict, game_mode: ModeType, game_property: Property, *, is_weekly=False, t: Type = int):
    for_time = 'lifetime' if not is_weekly else 'weekly'
    try:
        return t(profile[for_time]['mode'][game_mode.value]['properties'][game_property.value])
    except KeyError:
        return 0.0


def make_player_stats_from_JSON_DATA(profile: dict) -> PlayerStats:

    kd = get_stat_for_profile(profile, ModeType.BattleRoyal, Property.KDRatio, is_weekly=False, t=float)
    wins = get_stat_for_profile(profile, ModeType.BattleRoyal, Property.Wins)
    kills = get_stat_for_profile(profile, ModeType.BattleRoyal, Property.Kills)
    games_played = get_stat_for_profile(profile, ModeType.BattleRoyal, Property.GamesPlayed)

    all_weekly_kills = sum(
        get_stat_for_profile(profile, mode, Property.Kills, is_weekly=True)
        for mode
        in ModeType
    )

    all_weekly_deaths = sum(
        get_stat_for_profile(profile, mode, Property.Deaths, is_weekly=True)
        for mode
        in ModeType
    )

    if all_weekly_deaths == 0:
        kdweekly = all_weekly_kills
    else:
        kdweekly = float(all_weekly_kills) / all_weekly_deaths

    kd = round(kd, 2)
    kdweekly = round(kdweekly, 2)
    if games_played == 0:
        winprecent = 0.0
    else:
        winprecent = (wins*100)/games_played
        winprecent = round(winprecent, 2)

    return PlayerStats(
        timestamp=datetime.datetime.now(),
        kd=kd,
        wins=wins,
        kills=kills,
        games_played=games_played,
        weekly_kd=kdweekly,
        win_percentage=winprecent,
    )


def make_player_stats_from_info_database(info: dict):
    try:
        delta_kd = info["delta_kd"]
        delta_last_kd = info["delta_last_kd"]
        delta_weekly_kd = info["delta_weekly_kd"]
        delta_last_weekly_kd = info["delta_last_weekly_kd"]
    except:
        delta_kd = info["deltakd"]
        delta_weekly_kd = info["deltakdweekly"]
        delta_last_weekly_kd = 0
        delta_last_kd = 0

    return PlayerStats(
    timestamp = info["time"],
    kd = info["kd"],
    wins = info["wins"],
    kills = info["kills"],
    games_played =info["gamesPlayed"],
    weekly_kd = info["kdweekly"],
    win_percentage = info["winprecent"],
    delta_kd = delta_kd,
    delta_last_kd = delta_last_kd,
    delta_weekly_kd = delta_weekly_kd,
    delta_last_weekly_kd = delta_last_weekly_kd,
    )