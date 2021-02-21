from typing import Tuple, List
from avoid_loop_import import players, platform_matcher, Minutes_to_pull_data_again, get_role_by_name, raise_error, get_channel_by_name, LAST_MATCH_CHANNEL
from callofduty import Title, Mode
from player_stats import PlayerStats, make_player_stats_from_JSON_DATA
from normal_game import NormalGame
import callofduty
import discord
import call_of_duty_handler
from discord.ext import commands
import datetime
from game import game_mod_normal

class DATABase_Player:

    def __init__(self, discord_guild: discord.Guild, discord_id: int, game_id: str, platform: callofduty.Platform, player_stats_list, name_in_game: str):
        self._discord_guild = discord_guild
        self._discord_id = discord_id
        self._game_id = game_id
        self._name_in_game = name_in_game
        self._cod_player = None
        self._discord_member = None
        self._platform = platform
        self._player_stats: List[player_stats.PlayerStats] = player_stats_list

    @property
    def discord_guild(self) -> discord.Guild:
        return self._discord_guild

    @property
    def discord_id(self) -> int:
        return self._discord_id

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

    @property
    async def cod_player(self) -> callofduty.Player:
        if self._cod_player is None:
            await self._set_cod_player()
        return self._cod_player

    async def _set_cod_player(self) -> None:
        if self._cod_player is None:
            self._cod_player = await call_of_duty_handler.CodClient().SearchPlayer(self.platform, self.game_id)

    @property
    async def discord_member(self):
        if self._discord_member is None:
            await self._set_discord_member()

        return self._discord_member

    async def _set_discord_member(self):
        guild = await discord.ext.commands.Bot.fetch_guild(self.discord_guild)
        self._discord_member = guild.get_member(self.discord_id)

    async def give_KD_roles(self):
        for r in self.discord_member.roles:
            if r.name[0:3] == 'Ove' or r.name[0:3] == 'Win' or r.name[0:3] == 'Wee':
                await self.discord_member.remove_roles(r)

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
        role = get_role_by_name(guild=self.discord_guild, name_of_role=role_name)
        if role is None:
            New_role_as_create = await self.guild.create_role(name=role_name)
            await self.discord_member.add_roles(New_role_as_create)
        else:
            await self.discord_member.add_roles(role)

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

        role = get_role_by_name(guild=self.discord_guild, name_of_role=role_name)
        if role is None:
            New_role_as_create = await self.discord_member.guild.create_role(name=role_name)
            await self.discord_member.add_roles(New_role_as_create)
        else:
            await self.discord_member.add_roles(role)

        i = 0
        while (i < 100):
            if i <= self.last_stats().kdweekly < i + 0.5:
                kd_weekly_title_role = i
                break
            i = i + 0.5
        if (kd_title_role < 1):
            role_name = 'Weekly KD| < 1'
        else:
            role_name = 'Weekly KD| ' + str(kd_weekly_title_role) + '-' + str(float(kd_weekly_title_role) + 0.5)

        role = get_role_by_name(guild=self.discord_guild, name_of_role=role_name)
        if role is None:
            New_role_as_create = await self.guild.create_role(name=role_name)
            await self.discord_member.add_roles(New_role_as_create)
        else:
            await self.discord_member.add_roles(role)

    @property
    def stats(self) -> Tuple[PlayerStats]:
        return tuple(self._player_stats)

    def last_stats(self):
        return self._player_stats[-1]

    def change_name_in_game(self, name_in_game):
        self._name_in_game = name_in_game
        self._change_name_in_game_in_database()

    def change_game_id_and_platform(self, game_id: str, platform: callofduty.Platform):
        self._platform = platform
        self._game_id = game_id
        self._change_game_id_in_database()
        self._change_Platform_in_database()

    async def last_matches(self, Number_of_maches):
        results = await call_of_duty_handler.CodClient().GetPlayerMatches(platform_matcher[self.platform], self.game_id,Title.ModernWarfare, Mode.Warzone, limit=Number_of_maches)
        for i in len(results) - 1:
            game = await make_games_from_JSON_DATA(results[i], self)
            if game is NormalGame:
                await game.normal_game_message_form(i)
            elif game is str:
                await raise_error(
                    self.discord_member,
                    'your game number: '+ str(i) + 'wasnt normal so i skip it',
                    get_channel_by_name(LAST_MATCH_CHANNEL)
                )

    def check_if_to_pull_again_stats(self):
        time_now = datetime.datetime.now()
        if time_now.day == self.last_stats.timestamp.day:
            if (time_now.hour - self.last_stats.timestamp.hour) > 1:
                return True
            elif (time_now.minute - self.last_stats.timestamp.minute) > Minutes_to_pull_data_again:
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
        if self.last_stats().timestamp.day == stats.timestamp.day:
            stats.set_deltas_kds(self._calculate_deltas_kd)
            self._player_stats[-1] = stats
            self._change_player_stats_in_database()
            return
        if len(self._player_stats) >= 10:
            stats.set_deltas_kds(self._calculate_deltas_kd)
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
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"Game-id": self.Game_id}}
        players.update_one(myquery, newvalues)

    def _change_Platform_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"Platform": self.Platform}}
        players.update_one(myquery, newvalues)

    def _change_player_stats_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"info": self._player_stats}}
        players.update_one(myquery, newvalues)

    def _change_name_in_game_in_database(self):
        myquery = {"discord-id": self.discord_id}
        newvalues = {"$set": {"info": self._name_in_game}}
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
        for s in game_info['players']:
            killsteam = killsteam + game_info[s]["kills"]
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
