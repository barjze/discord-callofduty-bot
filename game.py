import datetime
import abc
from normal_game import NormalGame
from database_player import DATABase_Player

game_mod_normal = ['br_brquads', 'br_brtrios', 'br_brduos', 'br_brsolos']

class Game(abc.ABC):

    def __init__(self, game_id: int, start_time: datetime.datetime, end_time: datetime.datetime):

        self._game_id = game_id
        self._start_time = start_time
        self._end_time = end_time

    @property
    def game_id(self) -> int:
        return self._game_id

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self._end_time


def make_games_from_JSON_DATA(game, player_member: DATABase_Player):
    game_info = {}
    players = {}
    game_data = await game.details()
    game_id = game_data["allPlayers"][0]["matchID"]
    time_game_is_start = game_data["allPlayers"][0]["utcStartSeconds"]
    time_game_is_end = game_data["allPlayers"][0]["utcEndSeconds"]
    game_mode = game_data["allPlayers"][0]["mode"]
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
    if str(game_mode) in game_mod_normal:
        return NormalGame(game_info)