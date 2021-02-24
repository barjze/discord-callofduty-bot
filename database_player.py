from typing import Tuple, List
from avoid_loop_import import players, platform_matcher, Minutes_to_pull_data_again, get_role_by_name, raise_error, get_channel_by_name, LAST_MATCH_CHANNEL,platform_reverse_matcher
from callofduty import Title, Mode
from player_stats import PlayerStats, make_player_stats_from_JSON_DATA, make_player_stats_from_info_database
from normal_game import NormalGame
import callofduty
import discord
import call_of_duty_handler
from discord.ext import commands
import datetime
from game import game_mod_normal

class DATABase_Player:

    def __init__(self, discord_guild: discord.Guild, discord_id: int, game_id: str, platform: callofduty.Platform, player_stats_list: List[dict], name_in_game: str, discord_member = None):
        self._discord_guild = discord_guild
        self._discord_id = discord_id
        self._game_id = game_id
        self._name_in_game = name_in_game
        self._cod_player = None
        self._discord_member = discord_member
        self._platform = platform
        self._player_stats: List[PlayerStats] = [
            make_player_stats_from_info_database(json_data)
            for json_data
            in player_stats_list
        ]

    @property
    def discord_guild(self) -> discord.Guild:
        return self._discord_guild

    @property
    def discord_id(self) -> int:
        return self._discord_id

    @property
    def platform(self) -> callofduty.Platform:
        return self._platform


    async def discord_name(self) -> str:
        discord_member = await self.discord_member()
        return discord_member.display_name

    @property
    def game_id(self) -> str:
        return self._game_id

    @property
    def name_in_game(self) -> str:
        return self._name_in_game

    @property
    async def cod_player(self) -> callofduty.Player:
        if self._cod_player is None:
            await self._set_cod_player()
        return self._cod_player

    async def _set_cod_player(self) -> None:
        if self._cod_player is None:
            self._cod_player = await call_of_duty_handler.CodClient().SearchPlayers(self.platform, self.game_id)
            self._cod_player = self._cod_player[0]

    async def discord_member(self):
        if self._discord_member is None:
            await self._set_discord_member()

        return self._discord_member

    async def _set_discord_member(self):
        self._discord_member = self._discord_guild.get_member(self.discord_id)
        return self._discord_member

    async def give_KD_roles(self):
        discord_member = await self.discord_member()
        roles = discord_member.roles
        for r in roles:
            if r.name[0:3] == 'Ove' or r.name[0:3] == 'Win' or r.name[0:3] == 'Wee':
                await discord_member.remove_roles(r)

        i = 0
        while (i < 10000):
            if i <= self.last_stats().wins < i + 50:
                wins_title_role = int(i)
                break
            i = i + 50
        if (wins_title_role < 50):
            role_name = 'Wins| < 50'
        else:
            role_name = 'Wins| ' + str(wins_title_role) + '+'
        role = get_role_by_name(ctx=None, guild=self.discord_guild, name_of_role=role_name)
        if role is None:
            New_role_as_create = await self.guild.create_role(name=role_name)
            await discord_member.add_roles(New_role_as_create)
        else:
            await discord_member.add_roles(role)

        i = 0
        while (i < 100):
            if i <= self.last_stats().kd < i + 0.5:
                kd_title_role = i
                break
            i = i + 0.5
        if (kd_title_role < 1):
            role_name = 'Overall KD| < 1'
        else:
            role_name = 'Overall KD| ' + str(kd_title_role) + '-' + str(float(kd_title_role) + 0.5)

        role = get_role_by_name(ctx=None, guild=self.discord_guild, name_of_role=role_name)
        if role is None:
            New_role_as_create = await discord_member.guild.create_role(name=role_name)
            await discord_member.add_roles(New_role_as_create)
        else:
            await discord_member.add_roles(role)

        i = 0
        while (i < 100):
            if i <= self.last_stats().weekly_kd < i + 0.5:
                kd_weekly_title_role = i
                break
            i = i + 0.5
        if (kd_title_role < 1):
            role_name = 'Weekly KD| < 1'
        else:
            role_name = 'Weekly KD| ' + str(kd_weekly_title_role) + '-' + str(float(kd_weekly_title_role) + 0.5)

        role = get_role_by_name(ctx=None, guild=self.discord_guild, name_of_role=role_name)
        if role is None:
            New_role_as_create = await self.guild.create_role(name=role_name)
            await discord_member.add_roles(New_role_as_create)
        else:
            await discord_member.add_roles(role)

    @property
    def stats(self) -> Tuple[PlayerStats]:
        return self._player_stats


    def last_stats(self):
        return self.stats[-1]

    def change_name_in_game(self, name_in_game):
        self._name_in_game = name_in_game
        self._change_name_in_game_in_database()

    def change_game_id_and_platform(self, game_id: str, platform: callofduty.Platform):
        self._platform = platform
        self._game_id = game_id
        self._change_game_id_in_database()
        self._change_Platform_in_database()

    async def last_matches(self, Number_of_maches):
        print(Number_of_maches)
        print(type(Number_of_maches))
        results = await call_of_duty_handler.CodClient().GetPlayerMatches(self.platform, self.game_id, Title.ModernWarfare, Mode.Warzone, limit=Number_of_maches + 1)
        for i in range(len(results) - 1):
            game = await make_games_from_JSON_DATA(results[i], self)
            if isinstance(game, NormalGame):
                await game.normal_game_message_form(str(i+1))
            elif isinstance(game, str):
                await raise_error(
                    await self.discord_member(),
                    'your game number: '+ str(i) + 'wasnt normal so i skip it',
                    get_channel_by_name(LAST_MATCH_CHANNEL)
                )

    def check_if_to_pull_again_stats(self):
        time_now = datetime.datetime.now()
        if time_now.day == self.last_stats().timestamp.day:
            if (time_now.hour - self.last_stats().timestamp.hour) > 1:
                return True
            elif (time_now.minute - self.last_stats().timestamp.minute) > Minutes_to_pull_data_again:
                return True
            else:
                return False
        else:
            True

    async def pull_new_stats(self):
        temp = await self.cod_player
        new_stats = await temp.profile(Title.ModernWarfare, Mode.Warzone)
        return make_player_stats_from_JSON_DATA(new_stats)

    def add_stats(self, stats: PlayerStats) -> None:
        if isinstance(self.last_stats().timestamp,list):
            if len(self.stats) >= 10:
                stats.set_deltas_kds(*self._calculate_deltas_kd(stats))
                self._player_stats.pop(0)
            self._player_stats.append(stats)
            self._change_player_stats_in_database()
            return
        if self.last_stats().timestamp.day == stats.timestamp.day:
            stats.set_deltas_kds(*self._calculate_deltas_kd(stats))
            self.stats[-1] = stats
            self._change_player_stats_in_database()
            return
        if len(self.stats) >= 10:
            stats.set_deltas_kds(*self._calculate_deltas_kd(stats))
            self._player_stats.pop(0)
        self._player_stats.append(stats)
        self._change_player_stats_in_database()

    def _calculate_deltas_kd(self, stats: PlayerStats):
        if len(self.stats) > 1:
            delta_kd = stats.kd - self.stats[-2].kd
            delta_weekly_kd = stats.weekly_kd - self.stats[-2].weekly_kd
            delta_last_kd = stats.kd - self.stats[-1].kd
            delta_last_weekly_kd = stats.weekly_kd - self.stats[-1].weekly_kd
            delta_kd = round(delta_kd, 2)
            delta_weekly_kd = round(delta_weekly_kd, 2)
            delta_last_kd = round(delta_last_kd, 2)
            delta_last_weekly_kd = round(delta_last_weekly_kd, 2)
        else:
            delta_kd = 0
            delta_weekly_kd = 0
            delta_last_kd = 0
            delta_last_weekly_kd = 0
        return delta_kd, delta_weekly_kd, delta_last_kd, delta_last_weekly_kd


    def _change_game_id_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"Game-id": self.game_id}}
        players.update_one(myquery, newvalues)

    def _change_Platform_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"Platform": platform_reverse_matcher[self.platform]}}
        players.update_one(myquery, newvalues)

    def _change_player_stats_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {
            "$set": {
                "info": [
                    stat.export_for_db()
                    for stat
                    in self._player_stats
                ]
            }
        }
        players.update_one(myquery, newvalues)

    def _change_name_in_game_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"name-in-game": self._name_in_game}}
        players.update_one(myquery, newvalues)

async def make_games_from_JSON_DATA(game, player_member: DATABase_Player):
    game_info = {}
    players = {}
    game_data = await game.details()
    game_id = game_data["allPlayers"][0]["matchID"]
    time_game_is_start = game_data["allPlayers"][0]["utcStartSeconds"]
    time_game_is_end = game_data["allPlayers"][0]["utcEndSeconds"]
    game_mode = game_data["allPlayers"][0]["mode"]
    if str(game_mode) in game_mod_normal:
        for j in game_data["allPlayers"]:
            if player_member.name_in_game.lower() == j["player"]["username"].lower():
                team_name = j["player"]["team"]
                rank = j["playerStats"]["teamPlacement"]
                break
        for a in game_data["allPlayers"]:
            if team_name == a["player"]["team"]:
                kills = a["playerStats"]["kills"]
                players[a["player"]["username"]] = {'kills': kills}
        game_info['players'] = players
        killsteam = 0
        for s in game_info['players']:
            killsteam = killsteam + game_info['players'][s]["kills"]
        game_info['game_id'] = game_id
        game_info['game_mode'] = game_mode
        game_info['time_start'] = time_game_is_start
        game_info['time_end'] = time_game_is_end
        game_info['Team'] = {'killsTeam': killsteam, 'rankTeam': rank}
        game_info['belong'] = player_member
        return NormalGame(game_info)
    elif str(game_mode) == "br_dmz_plnbld":
        ame_id = game_data["allPlayers"][0]["matchID"]
        time_game_is_start = game_data["allPlayers"][0]["utcStartSeconds"]
        time_game_is_end = game_data["allPlayers"][0]["utcEndSeconds"]
        game_mode = game_data["allPlayers"][0]["mode"]
        return game_mode
    else:
        f = open("myfile.txt", "w")
        f.write(str(game_data) + "\n")
