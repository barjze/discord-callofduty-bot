import dataclasses
import datetime
import discord
from main import get_channel_by_name
from main import find_player_by_Game_id

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

    def _set_deltas_kds(self, delta_kd, delta_weekly_kd, delta_last_kd, delta_last_weekly_kd):
        self.delta_kd = delta_kd
        self.delta_last_kd = delta_last_kd
        self.delta_weekly_kd = delta_weekly_kd
        self.delta_last_weekly_kd = delta_last_weekly_kd

    def stats_massage_form(self, member: discord.Member, lfg_stats: str, massage_to_delete=None):
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


def make_player_stats_from_JSON_DATA(profile: dict):
    #Game_id = str(profile["username"])
    kd = profile["lifetime"]["mode"]["br"]["properties"]["kdRatio"]
    wins = int(profile["lifetime"]["mode"]["br"]["properties"]["wins"])
    kills = int(profile["lifetime"]["mode"]["br"]["properties"]["kills"])
    games_played = int(profile["lifetime"]["mode"]["br"]["properties"]["gamesPlayed"])
    kills_weekly_br_solo = int(profile["weekly"]["mode"]["br_brsolo"]["properties"]["kills"])
    kills_weekly_br_duo = int(profile["weekly"]["mode"]["br_brduos"]["properties"]["kills"])
    kills_weekly_br_trio = profile["weekly"]["mode"]["br_brtrios"]["properties"]["kills"]
    kills_weekly_br_quad = profile["weekly"]["mode"]["br_brquads"]["properties"]["kills"]
    deaths_weekly_br_solo = profile["weekly"]["mode"]["br_brsolo"]["properties"]["deaths"]
    deaths_weekly_br_duo = profile["weekly"]["mode"]["br_brduos"]["properties"]["deaths"]
    deaths_weekly_br_trio = profile["weekly"]["mode"]["br_brtrios"]["properties"]["deaths"]
    deaths_weekly_br_quad = profile["weekly"]["mode"]["br_brquads"]["properties"]["deaths"]
    try:
        mona = kills_weekly_br_solo + kills_weekly_br_duo + kills_weekly_br_trio + kills_weekly_br_quad
        mhane = deaths_weekly_br_solo + deaths_weekly_br_duo + deaths_weekly_br_trio + deaths_weekly_br_quad
        kdweekly = mona/mhane
    except:
        if mona > 0 and mhane == 0:
            kdweekly = mona
        elif mhane == 0:
            kdweekly = 0


    kd = round(kd, 2)
    kdweekly = round(kdweekly, 2)
    winprecent = (wins*100)/games_played
    winprecent = round(winprecent, 2)

    return PlayerStats(
        timestamp = datetime.datetime.now(),
        kd = kd,
        wins = wins,
        kills = kills,
        games_played = games_played,
        weekly_kd = kdweekly,
        win_percentage = winprecent,
    )

def calculate_deltas_kd():
    find_player_by_Game_id()