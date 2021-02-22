from avoid_loop_import import get_channel_by_name, LAST_MATCH_CHANNEL, Bot_Embed_Massage_THUMBNAIL_URL
import discord

class NormalGame():
    def __init__(self, game_info):
        self._game_id = game_info['game_id']
        self._game_mode = game_info['game_mode']
        self._start_time = game_info['time_start']
        self._end_time = game_info['time_end']
        self._players = game_info['players']
        self._game_info = game_info
        self._belong = game_info['belong']
        self._team_belong = game_info['Team']

    @property
    def game_id(self) -> str:
        return self._game_id

    @property
    def game_mode(self) -> str:
        return self._game_mode

    @property
    def start_time(self) -> str:
        return self._start_time

    @property
    def end_time(self) -> str:
        return self._end_time

    @property
    def players(self) -> str:
        return self._players

    @property
    def game_info(self) -> str:
        return self._game_info

    @property
    def belong(self) -> str:
        return self._belong

    @property
    def team_belong(self) -> str:
        return self._team_belong

    async def normal_game_message_form(self, number_game: str = "1"):
        discord_member = await self._belong.discord_member()
        Channel = get_channel_by_name(LAST_MATCH_CHANNEL)
        normal_game_message_form = discord.Embed(title="in " + discord_member.display_name + "game number: " + number_game, description="", color=0x00ff00)
        for i in self.players:
            normal_game_message_form.add_field(name="player: " + str(i) + " did: ", value=str(self.players[i]['kills']) + " kills", inline=False)
        normal_game_message_form.add_field(name="your team finish at: ", value=str(self.team_belong['rankTeam']) + ' place', inline=False)
        normal_game_message_form.add_field(name="your team had total of: ", value=str(self.team_belong['killsTeam']) + " kills", inline=False)
        normal_game_message_form.set_thumbnail(url=Bot_Embed_Massage_THUMBNAIL_URL)
        await Channel.send(embed=normal_game_message_form)