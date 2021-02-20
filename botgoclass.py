import os
from typing import Any, Union, List
import asyncio
import pymongo
import time
import callofduty
import callofduty.http
import callofduty.utils
import callofduty.auth
from callofduty import Mode, Platform, Title, Match
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime



load_dotenv("DISCORD_TOKEN.env")  # nessery
TOKEN = os.getenv('DISCORD_TOKEN')
listc2 = []
listc3 = []
listc4 = []
listp1 = []
teamchek = []
credlist = [
    'almog889@gmail.com:An130991',
    'sihmon.tally@gmail.com:Alon2253',
    'moranmoradi20@gmail.com:moran689',
    'bigfancod@gmail.com:callofduty2@',
    'ovo6owl@hotmail.com:Artemis1!2@',
    'linanachshon1@gmail.com:Ln261155',
    'kayosha2020@gmail.com:Kaya2020'
]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

myMongo = pymongo.MongoClient('mongodb://localhost:1111/')
discordlab = myMongo["discord-data"]
players = discordlab["players"]

################constnts####################
DG = client.get_guild(710393755299217492)               #discord
LFGChannel = client.get_channel(778996619520901150)       #Text_Channle
ErorrChannel = client.get_channel(786564015357689896)     #Text_Channle
lastmatchchannel = client.get_channel(787705808762568724) #Text_Channle
statsChannel = client.get_channel(778996335348023316)   #Text_Channle
signupChannel = client.get_channel(778996231971405845)  #Text_Channle
TornamentcommandChannel = client.get_channel(805780162004254730) #Text_Channle
JointoclanChannle = client.get_channel(780391706486243328) #Voice_Channle
platform_matcher = {
            'Activision': Platform.Activision,
            'Xbox': Platform.Xbox,
            'BattleNet': Platform.BattleNet,
            'PlayStation': Platform.PlayStation,
        }

game_mod_matcher = {'squad':br_brquads,
                    'trios':br_brtrios,
                    'duos':br_brduos,
                    'solo':br_brsolos,
                    'plander':br_dmz_plnbld}



def arbi():
    arbi.counter += 1
    if arbi.counter > 107:
        arbi.counter = 0
arbi.counter = 0

def open_MD_laybel_for_events():
    global clan
    global games
    global event
    clan = discordlab["clan"]
    games = discordlab["games"]
    event = discordlab["event"]
    return

def close_MD_laybel_for_events():
    global clan
    global games
    global event
    c1 = clan.drop_collection()
    c2 = games.drop_collection()
    c3 = event.drop_collection()
    return c1, c2, c3


class BMDevent:
    def __init__(self, eventModeArgument, BMDmember_open_the_event):
        self.id
        self.eventMode = eventModeArgument
        self.BMDmember_open_the_event = BMDmember_open_the_event
        self.TimeStart = 'not-yet'
        self.timeEnd = 'not-yet'

    def change_TimeStart(self):

    def change_TimeEnd(self):

    def close_event(self):


class Bteam_in_game:
    def __init__(self, MDgame, BMDmember_game_look):
        self.player_belong = BMDmember_game_look
        self.team_name = find_name_team(self, MDgame)
        self.players_names_list , self.players_kills_list , self.placement_team = find_names_and_kills_players_team(self,MDgame)
        self.kills_team = sum(self.players_kills_list)


    def find_name_team(self, MDgame):
        for i in MDgame["allPlayers"]:
            if self.player_belong.name_in_game == i["player"]["username"]:
                self.name_team_belong = i["player"]["team"]
                return self.name_team_belong

    def find_names_and_kills_players_team(self, MDgame):
        players_name_list = []
        players_kills_list = []
        for a in MDgame["allPlayers"]:
            if self.name_team_belong == a["player"]["team"]:
                rank = a["playerStats"]["teamPlacement"]
                players_name_list.append(a["player"]["username"])
                players_kills_list.append(a["playerStats"]["kills"])
        return players_name_list, players_kills_list, rank


class BMDgame:
    """class for game in the data base"""
    def __init__(self, MDgame, BMDmember_game_look):
        game_mod_convertor = {'br_brquads': normal,
                            'br_brtrios': normal,
                            'br_brduos': normal,
                            'br_brsolos': normal,
                            'br_dmz_plnbld': plander}
        self.id = MDgame["allPlayers"][0]["matchID"]
        self.mode = MDgame["allPlayers"][0]["mode"]
        BMDgame_game = BMDgame_mode_game_mod_convertor[self.mode](MDgame,BMDmember_game_look)






class BMDgame_mode_normal(BMDgame):
    def __init__(self, MDgame, BMDmember_game_look):
        self.mode = MDgame["allPlayers"][0]["mode"]
        self.timeStart = MDgame["allPlayers"][0]["utcStartSeconds"]
        self.timeEnd = MDgame["allPlayers"][0]["utcEndSeconds"]
        self.player_belong = BMDmember_game_look
        self.team_belong = Bteam_in_game(MDgame, BMDmember_game_look)


class BMDgame_mode_plander(BMDgame):
    def __init__(self, MDgame, BMDmember_game_look):
        self.mode = MDgame["allPlayers"][0]["mode"]
        self.timeStart = MDgame["allPlayers"][0]["utcStartSeconds"]
        self.timeEnd = MDgame["allPlayers"][0]["utcEndSeconds"]
        self.player_belong = BMDmember_game_look
        self.team_belong = Bteam_in_game(MDgame, BMDmember_game_look)

class BMDgame_mode_privte_match(BMDgame):
    def __init__(self, MDgame, BMDmember_game_look):
        self.mode = MDgame["allPlayers"][0]["mode"]
        self.timeStart = MDgame["allPlayers"][0]["utcStartSeconds"]
        self.timeEnd = MDgame["allPlayers"][0]["utcEndSeconds"]
        self.player_belong = BMDmember_game_look
        self.team_belong = Bteam_in_game(MDgame, BMDmember_game_look)

class BMDplayer_info:
    """class for player_info list of dic with info of a player in the database"""
    def __init__(self, **kwargs):
        self.time = BMDtime(time)
        self.kd = kd
        self.wins = wins
        self.kills= kills
        self.gamesPlayed = gamesPlayed
        self.kdweekly = kdweekly
        self.winprecent = winprecent
        self.deltakd = deltakd
        self.deltakdweekly = deltakdweekly
        self.deltakdcompertoday = deltakdcompertoday

class BMDtime:
    """class for time in the data base"""
    def __init__(self, *args):
        self.year = args[0]
        self.month = args[1]
        self.day = args[2]
        self.hour = args[3]
        self.minetus = args[4]

class BMDclan:
    def __init__(self, MDclan):
        self.clan_name = MDclan['clan-name']
        self.Players_in = MDclan['player-in']
        self.Players_stand_by = MDclan['player-stand-by']
        self.clan_Leader = find_by_discord_id(MDclan['player-in'][0]["discordid"])
        self.Games =
        try:
            self.channel_clan_id = MDclan['channel_clan_id']
        except:
            self.channel_clan_id = "no channel exist yet"

    def change_players_in(self):
        newvalues = {"$set": {'playerin': self.Players_in}}
        myquery = {"clan-name": self.clan_name}
        clan.update_one(myquery, newvalues)
        return find_clan_by_name(self.clan_name)

    def change_players_stand_by(self):
        newvalues = {"$set": {'player-stand-by': self.Players_stand_by}}
        myquery = {"clan-name": self.clan_name}
        clan.update_one(myquery, newvalues)
        return find_clan_by_name(self.clan_name)

    def change_channel_clan_id(self):
        newvalues = {"$set": {'channel_clan_id': self.channel_clan_id}}
        myquery = {"clan-name": self.clan_name}
        clan.update_one(myquery, newvalues)
        return find_clan_by_name(self.clan_name)

    def clan_to_clan_MD(self):
        x = {"clan-name": clan_name}
        clanM = clan.find_one(x)
        if clanM == None:
            return None
        return clanM

class BMDplayer:
    """class for player in the database"""
    def __init__(self, MDdiscordmember):
        self.discord_id = MDdiscordmember['discordid']
        self.discord_name = MDdiscordmember['discord-name']
        self.Game_id = MDdiscordmember['Game-id']
        self.Platform = MDdiscordmember['Platform']
        self.info = make_list_of_BMDinfo(MDdiscordmember['info'])
        self.last_info = BMDplayer_info(MDdiscordmember['info'][-1])
        try:
            self.name_in_game = MDdiscordmember['name-in-game']
        except:
            self.name_in_game = None

    def change_info(self):
        myquery = {"Game-id": self.Game_id}
        newvalues = {"$set": {"info": self.info}}
        players.update_one(myquery, newvalues)
        return find_by_Game_id(self.Game_id)

    def change_Game_id(self, Game_id):
        self.Game_id = Game_id
        myquery = {"discordid": self.discord_id}
        newvalues = {"$set": {"Game-id": self.Game_id}}
        players.update_one(myquery, newvalues)
        return find_by_Game_id(self.Game_id)

    def change_Platform(self):
        myquery = {"Game-id": self.Game_id}
        newvalues = {"$set": {"Platform": self.Platform}}
        players.update_one(myquery, newvalues)
        return find_by_Game_id(self.Game_id)

    def change_name_in_game(self,name_in_game):
        self.name_in_game = name_in_game
        myquery = {"Game-id": self.Game_id}
        newvalues = {"$set": {"name-in-game": self.name_in_game}}
        players.update_one(myquery, newvalues)
        return find_by_Game_id(self.Game_id)

    def player_to_clan_MD(self):
        person1 = {"discordid": self.discord_id}
        person1 = players.find_one(person1, {"info": 0})
        return person1

    def check_if_player_already_invaited_to_clan(self):
        for x in clan.find():
            for y in x['player-stand-by']["discord-id"]:
                if player.discord_id == y:
                    return BMDclan(x), True
        return None, False

    def check_if_player_already_play_in_clan(self):
        for x in clan.find():
            for y in x['player-in']["discord-id"]:
                if player.discord_id == y:
                    return BMDclan(x), True
        return None, False

    def get_his_discord_member(self):
        member = DG.get_member(self.discord_id)
        return member

def find_by_Game_id(Gameid):
    x = {"Game-id": Gameid}
    person = players.find_one(x)
    if person == None:
        return None
    person = BMDplayer(person)
    return person

def find_by_discord_id(discord_id):
    x = {"discordid": discord_id}
    person = players.find_one(x)
    if person == None:
        return None
    person = BMDplayer(person)
    return person

def find_clan_by_name(clan_name):
    x = {"clan-name": clan_name}
    clanM = clan.find_one(x)
    if clanM == None:
        return None
    clanM = BMDclan(clanM)
    return clanM

def make_list_of_BMDinfo(info):
    BMDinfo_list = []
    for i in info:
        BMDinfo_list.append(BMDplayer_info(info[i]))
    return BMDinfo_list

class DorHTTP(callofduty.http.HTTP):
    def __init__(self, auth):
        super().__init__(auth)

    async def GetFullMatch(
            self, title: str, platform: str, mode: str, matchId: int,
    ) -> Union[dict, list, str]:
        return await self.Send(
            callofduty.http.Request(
                "GET",
                f"api/papi-client/crm/cod/v2/title/{title}/platform/{platform}/fullMatch/{mode}/{matchId}/en",
            )
        )

class DorMatch(callofduty.match.Match):

    def __init__(self, client: 'DorClient', **kwargs):
        super().__init__(client, kwargs)

    async def details(self) -> dict:
        return await self._client.GetFullMatch(self.title, self.platform, self.id)

class DorClient(callofduty.Client):
    def __init__(self, http):
        super().__init__(http)

    async def GetFullMatch(
            self, title: Title, platform: Platform, matchId: int
    ) -> dict:
        callofduty.utils.VerifyTitle(title)
        callofduty.utils.VerifyPlatform(platform)

        return (
            await self.http.GetFullMatch(
                title.value, platform.value, Mode.Warzone.value, matchId
            )
        )["data"]

    async def GetPlayerMatches(
            self, platform: Platform, username: str, title: Title, mode: Mode, **kwargs
    ) -> List[Match]:
        matches = await super().GetPlayerMatches(platform, username, title, mode, **kwargs)

        return [
            DorMatch(self, id=match.id, platform=match.platform, title=match.title)
            for match
            in matches
        ]

async def DorLogin(email: str, password: str) -> DorClient:
    auth: callofduty.auth.Auth = callofduty.auth.Auth(email, password)
    await auth.RegisterDevice()
    await auth.SubmitLogin()
    return DorClient(DorHTTP(auth))

def append_value(dict_obj, key, value):
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            dict_obj[key] = [dict_obj[key]]
        dict_obj[key].append(value)
    else:
        dict_obj[key] = value

def add_if_key_not_exist(dict_obj, key, value):
    if key not in dict_obj:
        dict_obj.update({key: value})
        return True



def findtime(colec, time):
    timeob = None
    for x in colec.find():
        try:
            timeob = x[time]
        except:
            pass
    return timeob

async def getmatchs_tornament(BMDclan):
    killsteam = 0
    gamelist = []
    for i in BMDclan.Players_in:
        player = BMDplayer(i)
        callofdutywebuser = await doconnect()
        clientD = await DorLogin(callofdutywebuser[0], callofdutywebuser[1])
        try:
            results = await clientD.GetPlayerMatches(platform_matcher[player.Platform], player.Game_id, Title.ModernWarfare, Mode.Warzone)
            break
        except Exception as e:
            await ErorrChannel.send(f'{e}\nwhile get game history\nuser used: {callofdutywebuser[0]}\n password used: {callofdutywebuser[1]}\n try to find: {player.Game_id}, {player.Platform}')
    usertofind = player.name_in_game
    s = findtime(timesgame, 'timeStart')
    if s is None:
        await TornamentcommandChannel.send('didnt find starttime')
    timeStart = s
    f = findtime(timesgame, 'timeEnd')
    if f is None:
        await TornamentcommandChannel.send('didnt find endtime')
    timeEnd = f
    for i in range(len(results) - 1):
        game = results[i]
        game1data = await game.details()
        timestartg = game1data["allPlayers"][0]["utcStartSeconds"]
        if timeStart < timestartg < timeEnd:
            gamelist.append(results[i])

    for j in gamelist:
        teamname = None
        teamplayers = {}
        teamplayers['clan'] = clan
        try:
            gamedata = await j.details()
        except Exception as e:
            await ErorrChannel.send(f'{e}')
        timestartg = gamedata["allPlayers"][0]["utcStartSeconds"]
        matchid = gamedata["allPlayers"][0]["matchID"]
        for i in gamedata["allPlayers"]:
            if usertofind == i["player"]["username"]:
                teamname = i["player"]["team"]
                ex = find(games, 'Team', 'teamname')
                for x in games.find():
                    if (x['Team']['matchid'] == matchid) and (x['clan'] == clan):
                        return
                find(games, 'Team', matchid)
                if (ex is not None) and (ex['Team']['matchid'] == matchid):
                    return
                else:
                    break
        if teamname is None:
            await ErorrChannel.send(f'cant find this name in game: {usertofind} beforesplit: {searchdata} belong to: {user}')
            return
        for a in gamedata["allPlayers"]:
            if teamname == a["player"]["team"]:
                kills = a["playerStats"]["kills"]
                rank = a["playerStats"]["teamPlacement"]
                teamname = a["player"]["team"]
                teamplayers[a["player"]["username"]] = {'kills': kills, 'rank': rank}
        for i in teamplayers:
            try:
                killsteam = killsteam + teamplayers[i]["kills"]
            except:
                pass
        timestartg = datetime.utcfromtimestamp(timestartg)
        teamplayers['Team'] = {'clan': clan, 'teamname': teamname, 'killsTeam': killsteam, 'rankTeam': rank, 'matchid': matchid, 'timestartg': timestartg}
        games.insert_one(teamplayers)
        return True

async def Leade_Bord():
    for x in games.find().sort("clan"):
        old1 = x
        rankTeam = x["Team"]["rankTeam"]
        killsTeam = x["Team"]["killsTeam"]
        points = int(((rankTeam)**(-1))*10) + int(killsTeam)
        games.update_one(old1, {"$set": {'points': points}})
    for f in clan.find():
        gamenum = 0
        point1 = 0
        point2 = 0
        for j in games.find().sort("points"):
            if f["clan"] == j["clan"]:
                if j["points"] >= point1:
                    point2 = point1
                    point1 = j["points"]
                elif j["points"] >= point2:
                    point2 = j["points"]
                gamenum = gamenum + 1
                channel = client.get_channel(758665316724113408)
                await channel.send(f'in game number: {gamenum}\nclan: {j["clan"]} did:\nkills: {j["Team"]["killsTeam"]}\nhis place: {j["Team"]["rankTeam"]}\npoints: {j["points"]}')
        point_total = point1 + point2
        await channel.send(f'clan: {f["clan"]} as {point_total} point at total')

async def kd(Gameid='me', member=discord.Message.author, howtosearch='defult'):
    if howtosearch == 'defult':
        info = await getinfo()
        if info == False:
            return False
        else:
            return info
    else:
        BMD_member = find_by_Game_id(Gameid)
        if len(BMD_member.info) > 0:
            ass = len(BMD_member.info) - 1
        else:
            info = await getinfo(BMD_member)
            if type(info) == bool:
                return info
            BMD_member.info.append(info)
            BMD_member.change_info()
            await giverole(member, info)
            return info
        BMD_player_info = BMDplayer_info(BMD_member.info[ass])
        time1 = time.gmtime()
        if (time1.tm_mday == BMD_player_info.time.day) and (time1.tm_mon == BMD_player_info.time.month):
            if (abs(time1.tm_min - BMD_player_info.time.minetus) >= 26) or (time1.tm_hour != BMD_player_info.time.hour):
                oldweekly = BMD_player_info.kdweekly
                info = await getinfo(BMD_member)
                if type(info) == bool:
                    return False
                deltakd = info['kdweekly'] - oldweekly
                deltakd = round(deltakd, 2)
                append_value(info, 'deltakdcompertoday', deltakd)
                BMD_member.info[ass] = info
                BMD_member.change_info()
                return info
            else:
                return BMD_member.info[ass]
        else:
            if type(info) == bool:
                return False
            if len(BMD_member.info) == 10:
                BMD_member.info[0] = BMD_member.info[9]
                BMD_member.info[1] = info
                for x in range(9, 1, -1):
                    BMD_member.info.pop(x)
                BMD_member.change_info()

            elif len(person2.info) < 10:
                BMD_member.info.append(info)
                BMD_member.change_info()
            return info


async def giverole(member, info):
    """this function get Discord.Member type and 'info'( -> dic) and give rolls in the discord(guild) to the member
    acoording to his info"""
    for r in member.roles:
        if r.name[0:3] == 'Ove' or r.name[0:3] == 'Win' or r.name[0:3] == 'Wee':  ######################### roles not to delete################################
            await member.remove_roles(r)

    i = 0
    flag = False
    while (i < 10000):
        if i <= info['wins'] < i + 50:
            winsr = int(i)
            break
        i = i + 50
    if (winsr < 50):
        forcomper = 'Wins| < 50'
    else:
        forcomper = 'Wins| ' + str(winsr) + '+'
    for k in member.guild.roles:
        if k.name == forcomper:
            await member.add_roles(k)
            flag = True
            break
    if flag == False:
            rtogive = await member.guild.create_role(name=forcomper)
            await member.add_roles(rtogive)

    i = 0
    flag = False
    while (i < 100):
        if i <= info['kd'] < i + 0.5:
            rankkd = i
            break
        i = i + 0.5
    if (rankkd < 1):
        forcomper = 'Overall KD| < 1'
    else:
        forcomper = 'Overall KD| ' + str(rankkd) + '-' + str(float(rankkd) + 0.5)
    for k in member.guild.roles:
        if k.name == forcomper:
            await member.add_roles(k)
            flag = True
            break
    if flag == False:
        rtogive = await member.guild.create_role(name=forcomper)
        await member.add_roles(rtogive)


    i = 0
    flag = False
    while (i < 100):
        if i <= info['kdweekly'] < i + 0.5:
            rankkd = i
            break
        i = i + 0.5
    if (rankkd < 1):
        forcomper = 'Weekly KD| < 1'
    else:
        forcomper = 'Weekly KD| ' + str(rankkd) + '-' + str(float(rankkd) + 0.5)

    for k in member.guild.roles:
        if k.name == forcomper:
            await member.add_roles(k)
            flag = True
            break
    if flag == False:
        rtogive = await member.guild.create_role(name=forcomper)
        await member.add_roles(rtogive)
    return info


async def clearmen(ctx='', userto=''):
   """this function get 'ctx' and a mention of Discord.Member ( ->str ) and return Discord.Member type of the member"""
    userto = userto[3:-1]
    person = userto
    userto = ctx.guild.get_member(int(person))
    return userto

async def doconnect():
    """this function use for every time the bot connect to callofduty servers to get 'info':
    its return eatch call diffrent username and password"""
    callofdutywebuser = credlist[arbi.counter % len(credlist)].split(':')
    arbi()
    return callofdutywebuser

async def stats_massgeform(info, name='worng', massage=None):
    """this function get 'info' ( -> dic) a name of memebr at discord and a Discord.Massage type
    its send the stats to the channel and delete the member massge if he got it"""
    if massage is not None:
        await discord.Message.delete(massage)
    if type(info) == bool:
        await statsChannel.send('something went Wrong Probably with get info from cod servers please try again...')
        return
    winp = str(info["winprecent"])
    kd = str(info["kd"])
    kd2 = ' (' + str(info["deltakd"]) + ')'
    kd = kd + kd2
    kdweekly = str(info["kdweekly"])
    try:
        kdweekly2 = ' (' + str(info["deltakdcompertoday"]) + ') (' + str(info["deltakdweekly"]) + ')'
    except:
        kdweekly2 = '(' + str(info["deltakdweekly"]) + ')'
    kdweekly = kdweekly + kdweekly2

    botfrom = discord.Embed(title=name + " stats", description="", color=0x00ff00)
    botfrom.add_field(name="KD: ", value=kd, inline=False)
    botfrom.add_field(name="Weekly KD(today)(last-time): ", value=kdweekly, inline=False)
    botfrom.add_field(name="Wins: ", value=info["wins"], inline=False)
    botfrom.add_field(name="Games Played: ", value=info["gamesPlayed"], inline=False)
    botfrom.add_field(name="Win Percentage: ", value=winp+'%', inline=False)
    botfrom.add_field(name="Kills: ", value=info["kills"], inline=False)
    botfrom.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg')
    await statsChannel.send(embed=botfrom)

async def Erorr_massge(member, massage, channel='def'):
    """this function get Discord.Member type massage( ->str ) and channel to send the eroor massage to"""
    masfrom = discord.Embed(title='Dear '+ member.display_name, description="", color=0xff0000)
    masfrom.add_field(name='Hello ' + member.mention, value=f"{massage}", inline=False)
    masfrom.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg')
    if channel == 'def':
        await member.send(embed=masfrom)
    else:
        await channel.send(embed=masfrom)

async def getinfo(BMD_member = 'defult'): # user: str, optionsearch = 'defult', member='a'):
    """this function get BMD_member type and get is info from call of duty server
    and retrun 'info' ( ->dic )"""
    found = 0
    first_time_search = [
        Platform.Activision,
        Platform.Xbox,
        Platform.BattleNet,
        Platform.PlayStation
    ]
    platform_matcher_convertor = {
        'Platform.Activision': 'Activision',
        'Platform.Xbox': 'Xbox',
        'Platform.BattleNet': 'BattleNet',
        'Platform.PlayStation': 'PlayStation'
    }

    if BMD_member == 'defult':
        for i in first_time_search:
            try:
                callofdutywebuser = await doconnect()
                clientD = await DorLogin(callofdutywebuser[0], callofdutywebuser[1])
                results = await clientD.SearchPlayers(first_time_search[i], BMD_member.Game_id, limit=3)
                if len(results) == 1:
                    me = results[0]
                    profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
                    optionsearch = platform_matcher_convertor[first_time_search[i]]
                    found = 1
                    break
                elif len(results) > 1:
                    await Erorr_massge(member, f"Found more than one Account ID with the following name {member.name} Please provide your entire ID as written on the platform you're using.", signupChannel)
                    return False
            except:
                results = []
    else:
        try:
            callofdutywebuser = await doconnect()
            clientD = await DorLogin(callofdutywebuser[0], callofdutywebuser[1])
            results = await clientD.SearchPlayers(platform_matcher[BMD_member.Platform], BMD_member.Game_id, limit=3)
            if len(results) == 1:
                me = results[0]
                profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
        except:
            results = []



    if len(results) == 0:
        member = BMD_member.get_his_discord_member()
        await Erorr_massge(member , 'Uh oh, Something went wrong while searching for your Account ID. Please try again!\n **in case you try to signup** Please try with battlenet|Activition insted', statsChannel)
        await ErorrChannel.send(f'user used: {callofdutywebuser[0]}\n password used: {callofdutywebuser[1]}\n try to find: {BMD_member.Game_id}, {BMD_member.Platform}')
        return False


    try:
        account = profile["username"]
    except:
        channel.send("Something went wrong, I couldn't find the ID you've provided, could you try again?")
        return False
    try:
        kd = profile["lifetime"]["mode"]["br"]["properties"]["kdRatio"]
    except:
        kd = 0
    try:
        wins = profile["lifetime"]["mode"]["br"]["properties"]["wins"]
    except:
        wins = 0
    try:
        kills = profile["lifetime"]["mode"]["br"]["properties"]["kills"]
    except:
        kills = 0
    try:
        gamesPlayed = profile["lifetime"]["mode"]["br"]["properties"]["gamesPlayed"]
    except:
        gamesPlayed = 0
    try:
        killsweeklybrsolo = profile["weekly"]["mode"]["br_brsolo"]["properties"]["kills"]
    except:
        killsweeklybrsolo = 0
    try:
        killsweeklybrduo = profile["weekly"]["mode"]["br_brduos"]["properties"]["kills"]
    except:
        killsweeklybrduo = 0
    try:
        killsweeklybrtrio = profile["weekly"]["mode"]["br_brtrios"]["properties"]["kills"]
    except:
        killsweeklybrtrio=0
    try:
        killsweeklybrquad = profile["weekly"]["mode"]["br_brquads"]["properties"]["kills"]
    except:
        killsweeklybrquad = 0
    try:
        deathsweeklybrsolo = profile["weekly"]["mode"]["br_brsolo"]["properties"]["deaths"]
    except:
        deathsweeklybrsolo = 0
    try:
        deathsweeklybrduo = profile["weekly"]["mode"]["br_brduos"]["properties"]["deaths"]
    except:
        deathsweeklybrduo = 0
    try:
        deathsweeklybrtrio = profile["weekly"]["mode"]["br_brtrios"]["properties"]["deaths"]
    except:
        deathsweeklybrtrio = 0
    try:
        deathsweeklybrquad = profile["weekly"]["mode"]["br_brquads"]["properties"]["deaths"]
    except:
        deathsweeklybrquad = 0
    try:
        mona = killsweeklybrsolo + killsweeklybrduo + killsweeklybrtrio + killsweeklybrquad
        mhane = deathsweeklybrsolo + deathsweeklybrduo + deathsweeklybrtrio + deathsweeklybrquad
        kdweekly = mona/mhane
    except:
        if mona > 0 and mhane == 0:
            kdweekly = mona
        elif mhane == 0:
            kdweekly = 0


    if type(BMD_member) is not str:
        if len(BMD_member.info) > 1:
            ass = len(BMD_member.info) - 2
            oldkdweekly = BMD_member.info[ass]['kdweekly']
            oldkd = BMD_member.info[ass]['kd']

    kd = round(kd, 2)
    kdweekly = round(kdweekly, 2)
    wins = int(wins)
    kills = int(kills)
    gamesPlayed =int(gamesPlayed)
    winprecent = (wins*100)/gamesPlayed
    winprecent = round(winprecent, 2)
    time1 = time.gmtime()
    try:
        deltakd = kd - oldkd
    except:
        deltakd = 0
    try:
        deltakdweekly = kdweekly - oldkdweekly
    except:
        deltakdweekly = 0

    deltakd = round(deltakd, 2)
    deltakdweekly = round(deltakdweekly, 2)
    containinfo = {'kd': kd, 'wins': wins, 'kills': kills, 'gamesPlayed': gamesPlayed, 'kdweekly': kdweekly, 'winprecent': winprecent, 'deltakd': deltakd, 'deltakdweekly': deltakdweekly, 'time': time1}
    return containinfo


async def datasignup(discordid, discordname, Gameid, paltformsearch):
    name_in_game = 'Dont-haveit-yet'
    check_memeber_not_exist = find_by_Game_id(Gameid)
    check_memeber_not_exist2 = find_by_discord_id(discordid)
    if check_memeber_not_exist is not None or check_memeber_not_exist2 is not None:
        return False
    if paltformsearch == 'BattleNet':
        name_in_game = Gameid.split('#')[0]
    data = {"discordid":discordid, "discord-name": discordname, "name-in-game":name_in_game, "Game-id":Gameid, "Platform" :paltformsearch, "info":[]}
    players.insert_one(data)
    return True



async def isitempty():
    for c in listc2:
        if len(c.members) == 0:
            await discord.VoiceChannel.delete(c)
            listc2.remove(c)
        elif c.name[3:] != str(listc2.index(c)):
            await c.edit(name=c.name[0:3]+str(listc2.index(c) + 1))

    for k in listc3:
        if len(k.members) == 0:
            await discord.VoiceChannel.delete(k)
            listc3.remove(k)
        elif k.name[4:] != str(listc3.index(k)):
            await k.edit(name=k.name[0:4] + str(listc3.index(k) + 1))

    for l in listc4:
        if len(l.members) == 0:
            await discord.VoiceChannel.delete(l)
            listc4.remove(l)
        elif l.name[4:] != str(listc4.index(l)):
            await l.edit(name=l.name[0:4] + str(listc4.index(l) + 1))

    for o in listp1:
        if len(o.members) == 0:
            await discord.VoiceChannel.delete(o)
            listp1.remove(o)
        elif o.name[4:] != str(listp1.index(o)):
            await o.edit(name=l.name[0:4] + str(listp1.index(o) + 1))

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    channel = member.guild.get_channel(778996231971405845)#change id for join###########################
    time.sleep(3)
    botwelcom = discord.Embed(title='Welcome to Artemis Warzone Discord', description="", color=0x00ff00)
    botwelcom.add_field(name='Hello '+member.display_name, value="Please sign up to the bot by typing your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For Example: !signup GiantPiG#3577779", inline=False)
    botwelcom.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg') ####not touch
    await channel.send(embed=botwelcom)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel == JointoclanChannle:
        await jump_to_room(member)
    if before.channel is None:
        if after.channel is not None:
            await get_stats('junck', member, 'Join/LFG')
    else:
        channel = member.guild.get_channel(778998398027300916)  # change id for join###############################
        if after.channel == channel:
            nameforroom = 'Duo' + str(len(listc2) + 1)
            chcreate2 = await member.guild.create_voice_channel(name=nameforroom, user_limit=2,
                                                               category=member.guild.categories[5])
            await member.move_to(chcreate2)
            listc2.append(chcreate2)
            time.sleep(1)

        channel2 = member.guild.get_channel(779000535071981585)  # change id for join###############################
        if after.channel == channel2:
            nameforroom = 'Trio' + str(len(listc3) + 1)
            chcreate3 = await member.guild.create_voice_channel(name=nameforroom, user_limit=3,
                                                               category=member.guild.categories[6])
            await member.move_to(chcreate3)
            listc3.append(chcreate3)
            time.sleep(1)

        channel3 = member.guild.get_channel(779000748323110912)  # change id for join###############################
        if after.channel == channel3:
            nameforroom = 'Quad' + str(len(listc4) + 1)
            chcreate4 = await member.guild.create_voice_channel(name=nameforroom, user_limit=4,
                                                               category=member.guild.categories[7])
            await member.move_to(chcreate4)
            listc4.append(chcreate4)
            time.sleep(1)

        channel4 = member.guild.get_channel(780391706486243328)  # change id for join###############################
        if after.channel == channel4:
            nameforroom = 'Trio' + str(len(listp1) + 1)
            chcreate5 = await member.guild.create_voice_channel(name=nameforroom, user_limit=3,
                                                                    category=member.guild.categories[12])
            await member.move_to(chcreate5)
            listp1.append(chcreate5)
            time.sleep(1)

        await isitempty()


async def jump_to_room(member):
    id = member.id
    for x in clan.find():
        for p in x['playerin']:
            if p["discordid"] == id:
                cid = x['channel_clan_id']
    cid = member.guild.get_channel(cid)
    await member.move_to(cid)


@client.command(name='lastmatch')
async def lastmatch_step1(ctx, numbergame=5):
    member = ctx.message.author
    BMDmember = find_by_discord_id(member.id)
    if BMDmember.name_in_game == None:
        await Erorr_massge(member, "you didn't provide your nickname in the game please do so! for more informaition"
                                   "please type '!nickname' at signup channel", lastmatchchannel)
        return

    else:
        await lastmatch_step2(BMDmember, numbergame)

async def lastmatch_step2(BMDmember, numbergame = 4):
        callofdutywebuser = await doconnect()
        clientD = await DorLogin(callofdutywebuser[0], callofdutywebuser[1])
        numbergame = int(numbergame) + 1
        try:
            results = await clientD.GetPlayerMatches(platform_matcher[BMDmember.Platform], BMDmember.Game_id, Title.ModernWarfare, Mode.Warzone, limit=numbergame)

        except Exception as e:
            await ErorrChannel.send(f'{e}\nwhile get game history\nuser used: {callofdutywebuser[0]}\n password used: {callofdutywebuser[1]}\n try to find: {BMDmember.Game_id}, {BMDmember.Platform}')
        if len(results) == 0 or results is None:
            member = BMDmember.get_his_discord_member()
            await Erorr_massge(member,'didnt get any games that weard.....', lastmatchchannel)
            await ErorrChannel.send(f'while get game history\nuser used: {callofdutywebuser[0]}\n password used: {callofdutywebuser[1]}\n try to find: {BMDmember.Game_id}, {BMDmember.Platform}')
            return
        for i in range(len(results) - 1):
            killsteam = 0
            teamplayers = {}
            game = results[i]
            gamedata = await game.details()



            timestartg = gamedata["allPlayers"][0]["utcStartSeconds"]
            gamemode = gamedata["allPlayers"][0]["mode"]
            for j in gamedata["allPlayers"]:
                if BMDmember.name_in_game.lower() == j["player"]["username"].lower():
                    teamname = j["player"]["team"]
                    break
            for a in gamedata["allPlayers"]:
                if teamname == a["player"]["team"]:
                    kills = a["playerStats"]["kills"]
                    rank = a["playerStats"]["teamPlacement"]
                    teamname = a["player"]["team"]
                    teamplayers[a["player"]["username"]] = {'kills': kills, 'rank': rank}
            for s in teamplayers:
                try:
                    killsteam = killsteam + teamplayers[s]["kills"]
                except:
                    pass
            timestartg = datetime.utcfromtimestamp(timestartg)
            teamplayers['Team'] = {'killsTeam': killsteam, 'rankTeam': rank, 'timestartg': timestartg}
            teamplayerslist = list(teamplayers)
            await lastmatchchannel.send(f'-----------------------------------------------------------------------------------------------------------')
            await lastmatchchannel.send(f'your game number: **{i + 1}**')
            for u in range(len(teamplayerslist) - 1):
                await lastmatchchannel.send(f'player number {u + 1} in the team:\n**{teamplayerslist[u]}** did: {int(teamplayers[teamplayerslist[u]]["kills"])} kills\n')
            await lastmatchchannel.send(f'your team finish at **{int(teamplayers["Team"]["rankTeam"])} place**\nyour team did **{int(teamplayers["Team"]["killsTeam"])} kills**')


@client.command(name='stats')
async def get_stats(ctx, userto='me', option='some-one-ask-for-stats'):
    if (userto == 'me'):
        person = ctx.message.author
        member = person
    else:
        person = userto
        if isinstance(person, str):
            person = await clearmen(ctx, userto)
        member = person

    BMDmember = find_by_discord_id(member.id)
    if person is not None:
        info = await kd(BMDmember.Game_id, member, BMDmember.Platform)
        if option == 'Join/LFG':
            await giverole(member, info)
            return info
        if option == 'some-one-ask-for-stats':
            ma = await ctx.send("**Fetching stats, you'll get them in no time!**")
            await stats_massgeform(info, BMDmember.discord_name, ma)
            await giverole(member, info)
    else:
        if option == 'some-one-ask-for-stats':
            await Erorr_massge(member, 'You are not in the DATABASE Please signup\n use: !signup', signupChannel)
            return
        usertype_member = client.get_user(member.id)
        usertype_member_bot = usertype_member.bot
        if usertype_member_bot == False:
            await Erorr_massge(member, 'You are not in the DATABASE Please signup\n use: !signup')

@client.command(name='דאשאד')
async def get_stats2(ctx, userto='me', option='some-one-ask-for-stats'):
    await get_stats(ctx, userto, option)

@client.command(name='signup')
async def signup(ctx, *, acid=None):
    member = ctx.message.author
    if acid is None:
        await Erorr_massge(member, 'To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For example: !signup GiantPiG#3577779', signupChannel)
        return
    if len(acid) <= 3:
        await Erorr_massge(member, 'Error!  username must be more than 3 letters', signupChannel)
        return
    masign = await ctx.send("**Checking your username, Please wait....**")
    mas = ctx.message
    time.sleep(1)
    await mas.delete()
    dosefond = await kd(acid, member, 'defult')
    if(dosefond == False):
        await discord.Message.delete(masign)
        return
    if await datasignup(member.id, member.display_name, dosefond["account"], dosefond["optionsearch"]):
        role = get(ctx.message.guild.roles, name="Artemis Member")
        await member.add_roles(role)
        info = dosefond
        await stats_massgef orm(info, member.display_name)
        await giverole(member, info)
        await discord.Message.delete(masign)
        botsign = discord.Embed(title='Welcome to Artemis Warzone Discord', description="", color=0x00ff00)
        botsign.add_field(name='Hello ' + member.display_name, value="Thank you for Signing up to ArtemisBot! from now on you can use the command !stats in #bot-stats to check your stats and update them.", inline=False)
        botsign.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg')
        await ctx.send(embed=botsign)
    else:
        await discord.Message.delete(masign)
        await ctx.send("Either your Discord account is signed up, or your Activision / Battle.net is signed up on a different Discord account.\n To update your stats, use #bot-stats and type the command !stats")

@client.command(name='resignup')
async def resignup(ctx, *, game_id = None):
    member = ctx.message.author
    if game_id is None:
        await Erorr_massge(member, 'To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For example: !signup GiantPiG#3577779', signupChannel)
        return
    masign = await ctx.send("**Resign up event has been Start!**")
    mas = ctx.message
    time.sleep(1)
    await mas.delete()
    dosefound = await kd(game_id, member)
    if(dosefound == False):
        await discord.Message.delete(masign)
        await Erorr_massge(member, f'I am Sorry but I colud not find you with {game_id}', signupChannel)
        return
    BMDmember = find_by_discord_id(member.id)
    if BMDmember is not None:
        BMDmember = BMDmember.change_Game_id(game_id)
        BMDmember.Platform = dosefound['optionsearch']
        BMDmember = BMDmember.change_Platform()
        await discord.Message.delete(masign)
        await Erorr_massge(member,f'Hi {member.display_name} Welcom to Artemis once again your ID as been update',signupChannel)
    else:
        await discord.Message.delete(masign)
        await Erorr_massge(member, f'I am Sorry but I colud not find you at the Data base. that mean you never signup yet', signupChannel)



@client.command(name='lfg')
async def lfg(ctx):
    member = ctx.message.author
    allchannels = discord.utils.get(member.guild.voice_channels)
    allchannels = allchannels.guild.voice_channels
    for k in allchannels:
        listmember = k.members
        for r in listmember:
            if r == member:
                VoiceChannel = k
    try:
        invaite = await VoiceChannel.create_invite()
    except:
        VoiceChannel = None
    info = await get_stats('junck', member, 'Join/LFG')
    kd = str(info['kd'])
    kdweekly = str(info["kdweekly"])
    wins = str(info["wins"])
    gamep = str(info["gamesPlayed"])
    winp = str(info["winprecent"])
    await LFGChannel.send('**'+member.display_name+'** looking for a group!\n**His Stats:** \nKD: '+kd+'          Weekly KD: '+kdweekly+'\nWins: '+wins+'    Game Played: '+gamep+'    Win Rate: '+winp+'%\n')
    if VoiceChannel is not None:
        await channel.send(invaite)

@client.command(name='ךכע')
async def lfg2(ctx):
    await lfg(ctx)

@client.command(name='cc')
async def clanc(ctx, clanname, pu1 ='def', pu2 ='def', pu3='def'):
    global eventopen
    global eventMode
    if eventopen == True:
        member = ctx.message.author
        if pu1 != 'def':
            pu1 = await clearmen(ctx, pu1)
        else:
            await ctx.send("you create clan with just you")
        if pu2 != 'def':
            pu2 = await clearmen(ctx, pu2)
        if pu3 != 'def':
            pu3 = await clearmen(ctx, pu3)
        clanLeader = find_by_discord_id(member.id)
        pu1 = find_by_discord_id(pu1.id)
        if pu2 != 'def':
            pu2 = find_by_discord_id(pu2.id)
        if pu3 != 'def':
            pu3 = find_by_discord_id(pu3.id)
        if pu1 is None or pu2 is None or pu3 is None:
            await ctx.send("One of the player you tag is not signup to the Bot yet.\nBecause of that reason the clan can't be create")
            return None
        p1 = clan.find_one({'peopletoc': [pu1]})
        p2 = None
        p3 = None
        if pu2 != 'def':
            p2 = check_if_player_already_invaited_to_clan(pu2)
        if pu3 != 'def':
            p3 = check_if_player_already_invaited_to_clan(pu3)
        p11 = find(clan, 'playerin', pu1)
        p12 = None
        p13 = None
        if pu2 != 'def':
            p12 = find(clan, 'playerin', pu2)
        if pu3 != 'def':
            p13 = find(clan, 'playerin', pu3)
        if all(p is not None for p in [p1, p2, p3, p11, p12, p13]):
            await ctx.send('one of your grop is ask to another clan or play in another clan')
            return None
        cc = {'clan-name': clanname}
        cc = clan.find_one(cc)
        if cc is None:
            if pu2 != 'def' and pu3 != 'def':
                data = {'clan-name':clanname, 'player-in':[clanLeader], 'player-stand-by':[pu1, pu2, pu3], 'channel_clan_id': None}
            elif pu2 != 'def' and pu3 == 'def':
                data = {'clan-name': clanname, 'player-in': [clanLeader], 'player-stand-by': [pu1, pu2], 'channel_clan_id': None}
            elif pu2 == 'def' and pu3 == 'def':
                data = {'clan-name': clanname, 'player-in': [clanLeader], 'player-stand-by': [pu1], 'channel_clan_id': None}
            clan.insert_one(data)

            user = ctx.message.guild.get_member(pu1['discordid'])
            await user.send(f'You have been invited to join {clanname} clan on the next tournament!\n to join please respond with: "!join activition-id"\n to ignore please respond with "!cancel"')
            if pu2 != 'def':
                user = ctx.message.guild.get_member(pu2['discordid'])
                await user.send(f'You have been invited to join {clanname} clan on the next tournament!\n to join please respond with: "!join activition-id"\n to ignore please respond with "!cancel"')
            if pu3 != 'def':
                user = ctx.message.guild.get_member(pu3['discordid'])
                await user.send(f'You have been invited to join {clanname} clan on the next tournament!\n to join please respond with: "!join activition-id"\n to ignore please respond with "!cancel"')
            user = ctx.message.guild.get_member(member.id)
            await user.send('To continue with Create your clan prosess please respond with !join activition-id')
        else:
            await ctx.send('Clan name is already taken')
    else:
        await ctx.send('tournament event is off')




# def find(colec, li, p):
#     for x in colec.find():
#         if p in x[li]:
#              return x
#     return None



@client.command(name='ccd')
async def clanc(ctx):
    member = ctx.message.author
    id = member.id
    clantodel = None
    for x in clan.find():
        for p in x['playerin']:
            if p["discordid"] == id:
                clantodel = x
    if clantodel is not None:
        try:
            channeltodel = clantodel['channel_clan_id']
        except:
            channeltodel = None
        if channeltodel is not None:
            channeltodel = client.get_channel(channeltodel)
            await channeltodel.delete()
        clan.delete_one(clantodel)
    else:
        await ctx.send("can't find any clan you opened.")

@client.command(name='join')
async def join(ctx, name_in_game = None):
    member = ctx.message.author
    player = find_by_discord_id(member.id)
    if player.name_in_game is None:
        if name_in_game is None:
            await ctx.send('please send your Nickname in the Game')
            return
        else:
            player.name_in_game = name_in_game
            player.change_name_in_game()
    clandata, invaitedata = player.check_if_player_already_invaited_to_clan()
    if clandata is None:
        await ctx.send('cant find you in any clan')
        return
    if invaitedata is True:
        clandata.Players_in.append(player.player_to_clan_MD())
        clandata = calndata.change_players_in()
        return
    clandata.Players_stand_by.pop(clandata.Players_stand_by.index(player.player_to_clan_MD()))
    clandata = clandata.change_players_stand_by()
    user = DG.get_member(member.id)
    await user.send(f'thanks you for join to {clandata.clan_name} clan')
    if len(clandata.Players_stand_by) == 0:
        user = DG.get_member(clandata.clan_Leader.discord_id)
        await user.send(f'Your clan {clandata.clan_name} is all set up members: ')
        for i in range(len(clandata.Players_in)):
            await user.send(f"{clandata.Players_in[i]['discord-name']}")
        await create_channel_clan(clandata.clan_name)

async def create_channel_clan(clan_name):
    channel_to_clone = DG.get_channel(784049072171778068) ################### Voice_channel id to clone #############
    channel_clan = await channel_to_clone.clone(name=clan_name)
    overwrite = discord.PermissionOverwrite()
    overwrite.connect = True
    for i in range(len(dataafter['playerin'])):
        id = dataafter['playerin'][i]['discordid']
        member = g.get_member(id)
        await channel_clan.set_permissions(member, overwrite=overwrite)
    channel_clan_id = channel_clan.id
    dataafter['channel_clan_id'] = channel_clan_id
    newvalues = {"$set": {'channel_clan_id': dataafter['channel_clan_id']}}
    cc = find(clan, 'clan', clan_name['clan'])
    clan.update_one(cc, newvalues)


@client.command(name='cancel')
async def cancel(ctx):
    member = ctx.message.author
    person = {"discordid": member.id}
    person = players.find_one(person, {"info": 0})
    cc = {'peopletoc': [person]}
    data = find(clan, 'peopletoc', person)
    if data is None:
        await ctx.send('cant find you in any clan')
        return
    own = data['playerin'][0]
    clann = data['clan']
    user = DG.get_member(own['discordid'])
    await user.send(f'{member.display_name} is cancel your invaite to the {clann} clan in the tornamenrt.')
    data['peopletoc'].pop(data['peopletoc'].index(person))
    newvalues = {"$set": {'peopletoc':data['peopletoc']}}
    clan.update_one(cc, newvalues)
    user = g.get_member(member.id)
    await user.send(f'thanks you are out form {data["clan"]} clan')
    if len(data['peopletoc']) == 0:
        id = data['playerin'][0]['discordid']
        user = DG.get_member(id)
        await user.send(f'Your clan is all set up members: ')
        for i in range(len(data['playerin'])):
            await user.send(f"{data['playerin'][i]['discord-name']}")
        await create_channel_clan(data)

@client.command(name='ton')
async def tournamenet(ctx, eventModeArgument : int):
    member = ctx.message.author

    global eventopen
    global eventMode
    eventMode = eventModeArgument
    for r in member.roles:
        if r.name == 'Private Match Manager':
            BMD_member = find_by_discord_id(member.id)
            eventMode_type = BMDevent(eventModeArgument, BMD_member)
            eventopen = True
            open_MD_laybel_for_events()
    if eventopen == False:
        await ctx.send('you dont have permtion to do so')
    else:
        await ctx.send('tournament event is ON')

@client.command(name='finish')
async def tournamenet_time_finish(ctx):
    member = ctx.message.author
    global eventopen
    for r in member.roles:
        if r.name == 'Private Match Manager':
            eventopen = False
    if eventopen == True:
        await ctx.send('you dont have permtion to do so')
    else:
        it_was_finish_time = False
        await ctx.send('tournament event is OFF')
        timeEnd = time.time()
        for x in timesgame.find():
            if 'timeEnd' in x:
                timesgame.update_one(x, {"$set": {'timeEnd': timeEnd}})
                it_was_finish_time = True
        if it_was_finish_time == False:
            timesgame.insert_one({'timeEnd': timeEnd})
        await ctx.send('time End now')
        await ctx.send('function at 5 min delay')
        for i in range(4, 0, -1):
            #time.sleep(60)
            await ctx.send(f'{i} min remaining')
        await ctx.send('done! prosses game')
        for x in clan.find():
            BMDclan_c = BMDclan(x)
            playerTeamFound = await getmatchs_tornament(BMDclan_c)

        for f in games.find():
            await ctx.send(f'{f["Team"]}')
        await ctx.send('Done for now')
        await Leade_Bord()


@client.command(name='start')
async def tournamenet_time_start(ctx):
    member = ctx.message.author
    for r in member.roles:
        if r.name == 'Private Match Manager':
            timeStart = time.time()
            timesgame.insert_one({'timeStart': timeStart})
            await ctx.send('time start now')
            return
    await ctx.send('You Dont have permission to do so')

@client.command(name='tfin')
async def tournamenet_end(ctx):
    member = ctx.message.author
    global eventopen
    for r in member.roles:
        if r.name == 'Private Match Manager':
            eventopen = False
            await clear_rooms()
            c1 ,c2 ,c3 = close_MD_laybel_for_events()
            await ctx.send(f'clan collection drop: {c1}\n games collection drop: {c2}\n times collection drop: {c3} ')

@client.command(name='!nickname')
async def nickname_add(ctx, name_in_game: str):
        member = ctx.message.author
        BMDmember = find_by_Game_id(member.id)
        if BMDmember == None:
            await Erorr_massge(member,'you need to sign up to the bot first please type "!signup" for more infomation/',signupChannel)
            return
        BMDmember.change_name_in_game(name_in_game)

async def clear_rooms():
    for i in clan.find():
        channel_del_id = i['channel_clan_id']
        if channel_del_id is not None:
            channel_del = client.get_channel(channel_del_id)
            if channel_del is not None:
                await channel_del.delete()


client.run(TOKEN)