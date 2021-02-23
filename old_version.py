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
clan = discordlab["clan"]
games = discordlab["games"]
timesgame = discordlab["timesgame"]
eventopen = False

def arbi():
    arbi.counter += 1
    if arbi.counter > 107:
        arbi.counter = 0
arbi.counter = 0


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


def find(colec, li, p):
    for x in colec.find():
        if p in x[li]:
             return x
    return None

def findtime(colec, time):
    timeob = None
    for x in colec.find():
        try:
            timeob = x[time]
        except:
            pass
    return timeob

async def getmatchs(searchdata, user: str, usernametoco, passwordtoco, clan, optionsearch = 'defult'):
    killsteam = 0
    gamelist = []
    clientD = await DorLogin(usernametoco, passwordtoco)
    try:
        if optionsearch == 'Activision':
            results = await clientD.GetPlayerMatches(Platform.Activision, user, Title.ModernWarfare, Mode.Warzone)
        elif optionsearch == 'Xbox':
            results = await clientD.GetPlayerMatches(Platform.Xbox, user, Title.ModernWarfare, Mode.Warzone)
        elif optionsearch == 'BattleNet':
            results = await clientD.GetPlayerMatches(Platform.BattleNet, user, Title.ModernWarfare, Mode.Warzone)
        elif optionsearch == 'PlayStation':
            results = await clientD.GetPlayerMatches(Platform.PlayStation, user, Title.ModernWarfare, Mode.Warzone)
    except Exception as e:
        channel = client.get_channel(786564015357689896)
        await channel.send(f'{e}\nwhile get game history\nuser used: {usernametoco}\n password used: {passwordtoco}\n try to find: {user}')
    if len(results) == 0 or results is None:
        channel = client.get_channel(778996335348023316)  # change id for join########################################
        await channel.send('didnt get any games that weard.....')
        channel = client.get_channel(786564015357689896)
        await channel.send(f'while get game history\nuser used: {usernametoco}\n password used: {passwordtoco}\n try to find: {user}')
        return
    usertofind = searchdata.split('#')
    usertofind = usertofind[0]
    s = findtime(timesgame, 'timeStart')
    if s is None:
        channel = client.get_channel(758665316724113408)  # change id for join########################################
        await channel.send('didnt find starttime')
    timeStart = s
    f = findtime(timesgame, 'timeEnd')
    if f is None:
        channel = client.get_channel(758665316724113408)  # change id for join########################################
        await channel.send('didnt find endtime')
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
            channel = client.get_channel(786564015357689896)
            await channel.send(f'{e}')
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
            channel = client.get_channel(786564015357689896)
            await channel.send(f'cant find this name in game: {usertofind} beforesplit: {searchdata} belong to: {user}')
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
        pointrank = 0
        rankTeam = x["Team"]["rankTeam"]
        killsTeam = x["Team"]["killsTeam"]
        if rankTeam == 1:
            pointrank = 15
        elif rankTeam == 2:
            pointrank = 10
        elif rankTeam == 3:
            pointrank = 8
        elif rankTeam in range[4, 6]:
            pointrank = 5
        elif rankTeam in range[6, 11]:
            pointrank = 3
        points = pointrank + int(killsTeam)
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
        callofdutywebuser = await doconnect()
        info = await getinfo(Gameid, callofdutywebuser[0], callofdutywebuser[1], howtosearch, member)
        if info == False:
            return False
        else:
            return info
    else:
        person1 = {"Game-id": Gameid}
        person2 = players.find_one(person1)
        if len(person2['info']) > 0:
            ass = len(person2['info']) - 1
        else:
            callofdutywebuser = await doconnect()
            info = await getinfo(Gameid, callofdutywebuser[0], callofdutywebuser[1], howtosearch, member)
            if type(info) == bool:
                return info
            person2['info'].append(info)

            myquery = {"Game-id": Gameid}
            newvalues = {"$set": {"info": person2['info']}}
            players.update_one(myquery,newvalues)
            await giverole(member, info)
            return info
        chack = person2['info'][ass]
        time1 = time.gmtime()
        if (time1.tm_mday == chack['time'][2]) and (time1.tm_mon == chack['time'][1]):
            if (abs(time1.tm_min - chack['time'][4]) >= 26) or (time1.tm_hour != chack['time'][3]):
                oldweekly = person2['info'][ass]['kdweekly']
                callofdutywebuser = await doconnect()
                info = await getinfo(Gameid, callofdutywebuser[0], callofdutywebuser[1], howtosearch, member)
                if type(info) == bool:
                    return False
                deltakd = info['kdweekly'] - oldweekly
                deltakd = round(deltakd, 2)
                append_value(info, 'delta', deltakd)
                person2['info'][ass] = info

                myquery = {"Game-id": Gameid}
                newvalues = {"$set": {"info": person2['info']}}
                players.update_one(myquery, newvalues)
                return info

            else:
                return chack
        else:
            callofdutywebuser = await doconnect()
            info = await getinfo(Gameid, callofdutywebuser[0], callofdutywebuser[1], howtosearch, member)
            if type(info) == bool:
                return False
            if len(person2['info']) == 10:
                person2['info'][0] = person2['info'][9]
                person2['info'][1] = info
                for x in range(9, 1, -1):
                    person2['info'].pop(x)

                myquery = {"Game-id": Gameid}
                newvalues = {"$set": {"info": person2['info']}}
                players.update_one(myquery, newvalues)

            elif len(person2['info']) < 10:
                person2['info'].append(info)

                myquery = {"Game-id": Gameid}
                newvalues = {"$set": {"info": person2['info']}}
                players.update_one(myquery, newvalues)
            return info


async def giverole(member, info):
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
    userto = userto[3:-1]
    person = userto
    userto = ctx.guild.get_member(int(person))
    return userto

async def doconnect():
    callofdutywebuser = credlist[arbi.counter % len(credlist)].split(':')
    arbi()
    return callofdutywebuser

async def massgeform(info, name='worng', massage=None):
    if massage is not None:
        await discord.Message.delete(massage)
    if type(info) == bool:
        channel = client.get_channel(778996335348023316)  # change id for join########################################
        await channel.send('something went Wrong Probably with get info from cod servers please try again...')
        return
    winp = str(info["winprecent"])
    kd = str(info["kd"])
    kd2 = ' (' + str(info["deltakd"]) + ')'
    kd = kd + kd2
    kdweekly = str(info["kdweekly"])
    try:
        kdweekly2 = ' (' + str(info["delta"]) + ') (' + str(info["deltakdweekly"]) + ')'
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
    channel = client.get_channel(778996335348023316)#change id for join########################################
    await channel.send(embed=botfrom)

async def massgeformsend(member, massage, channel='def'):
    g = client.get_guild(710393755299217492)  ################### discord id #############
    user = g.get_member(member.id)
    masfrom = discord.Embed(title='Dear '+ member.display_name, description="", color=0xff0000)
    masfrom.add_field(name='Hello ' + member.display_name, value=f"{massage}", inline=False)
    masfrom.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg')
    if channel == 'def':
        await user.send(embed=masfrom)
    else:
        await channel.send(embed=masfrom)

async def getinfo(user: str, usernametoco, passwordtoco, optionsearch = 'defult', member='a'):
    member = member
    channel = member.guild.get_channel(778996231971405845)
    client = await DorLogin(usernametoco, passwordtoco)
    found = 0
    if optionsearch == 'Activision' or optionsearch == 'defult':
        try:
            results = await client.SearchPlayers(Platform.Activision, user, limit=3)
            if len(results) == 1:
                me = results[0]
                profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
                if profile["username"].lower() == user.lower():
                    optionsearch = 'Activision'
                    found = 1
        except:
            results = []

    if optionsearch == 'BattleNet' or (optionsearch == 'defult' and found == 0):
        try:
            callofdutywebuser = await doconnect()
            usernametoco = callofdutywebuser[0]
            passwordtoco = callofdutywebuser[1]
            client = await DorLogin(usernametoco, passwordtoco)
            results = await client.SearchPlayers(Platform.BattleNet, user, limit=3)
            if len(results) == 1:
                me = results[0]
                profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
                if profile["username"].lower() == user.lower():
                    optionsearch = 'BattleNet'
                    found = 1
        except:
            results = []

    if optionsearch == 'PlayStation' or (optionsearch == 'defult' and found == 0):
        try:
            callofdutywebuser = await doconnect()
            usernametoco = callofdutywebuser[0]
            passwordtoco = callofdutywebuser[1]
            client = await DorLogin(usernametoco, passwordtoco)
            results = await client.SearchPlayers(Platform.PlayStation, user, limit=3)
            if len(results) == 1:
                me = results[0]
                profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
                if profile["username"].lower() == user.lower():
                    optionsearch = 'PlayStation'
                    found = 1
        except:
            results = []
    if optionsearch == 'Xbox' or (optionsearch == 'defult' and found == 0):
        try:
            callofdutywebuser = await doconnect()
            usernametoco = callofdutywebuser[0]
            passwordtoco = callofdutywebuser[1]
            client = await DorLogin(usernametoco, passwordtoco)
            results = await client.SearchPlayers(Platform.Xbox, user, limit=3)
            if len(results) == 1:
                me = results[0]
                profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
                if profile["username"].lower() == user.lower():
                    optionsearch = 'Xbox'
                    found = 1
        except:
            results = []


    if len(results) == 0:
        await massgeformsend(member, 'Uh oh, Something went wrong while searching for your Account ID. Please try again!\n **in case you try to signup** Please try with battlenet|Activition insted', channel)
        channel = member.guild.get_channel(786564015357689896)
        await channel.send(f'user used: {usernametoco}\n password used: {passwordtoco}\n try to find: {user}')
        return False
    if len(results) != 1:
        await massgeformsend(member, f"Found more than one Account ID with the following name {member.name} Please provide your entire ID as written on the platform you're using.", channel)
        return False
    me = results[0]
    profile = await me.profile(Title.ModernWarfare, Mode.Warzone)
    # f = open("info_form.txt", "w")
    # f.write(str(profile) + "\n")

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

    person1 = {"Game-id": user}
    person2 = players.find_one(person1)
    if(person2 is not None):
        if len(person2['info']) > 1:
            ass = len(person2['info']) - 2
            oldkdweekly = person2['info'][ass]['kdweekly']
            oldkd = person2['info'][ass]['kd']

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
    containinfo = {'kd': kd, 'wins': wins, 'kills': kills, 'gamesPlayed': gamesPlayed, 'kdweekly': kdweekly, 'winprecent': winprecent, 'account': account, 'optionsearch': optionsearch, 'deltakd': deltakd, 'deltakdweekly': deltakdweekly, 'time': time1}
    return containinfo


async def datasignup(discordid, discordname, Gameid, paltformsearch):
    person2 = {"Game-id":Gameid}
    person = {"discordid":discordid}
    person = players.find_one(person)
    person2 = players.find_one(person2)
    if person is not None or person2 is not None:
        return False
    data = {"discordid":discordid, "discord-name": discordname, "Game-id":Gameid, "Platform" :paltformsearch, "info":[]}
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
    channelclan = member.guild.get_channel(780391706486243328)
    if after.channel == channelclan:
        await jump_to_room(member)
    if before.channel is None:
        if after.channel is not None:
            await get_stats('junck', member, '2')
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
async def lastmatch_step1(ctx, gamename='d', numbergame=5):
    if gamename.isdigit():
        numbergame = gamename
        gamename = 'd'
    member = ctx.message.author
    person = {"discordid": member.id}
    person = players.find_one(person, {"info": 0})
    if person["Platform"] != 'Activision':
        if gamename == 'd':
            await ctx.send("can't do because I dont have your activition-id in the database\n"
                           "to complete the function please write:\n"
                           "!lastmatch NameInGame\n"
                           "your name in game is your activition id without the numbers\n"
                           "for Exemple if activition id= GiantPiG#3577779\n"
                           "please write !lastmatch GiantPiG")
        else:
            callofdutywebuser = await doconnect()
            await lastmatch_step2(callofdutywebuser[0], callofdutywebuser[1], person['Game-id'], person['Platform'], gamename, numbergame)
    else:
        callofdutywebuser = await doconnect()
        await lastmatch_step2(callofdutywebuser[0], callofdutywebuser[1], person['Game-id'], person['Platform'], gamename, numbergame)

async def lastmatch_step2(usernametoco, passwordtoco, user, optionsearch, nameGame, numbergame: int):
        clientD = await DorLogin(usernametoco, passwordtoco)
        numbergame = int(numbergame) + 1
        platform_matcher = {
            'Activision': Platform.Activision,
            'Xbox': Platform.Xbox,
            'BattleNet': Platform.BattleNet,
            'PlayStation': Platform.PlayStation,
        }

        try:
            results = await clientD.GetPlayerMatches(platform_matcher[optionsearch], user, Title.ModernWarfare, Mode.Warzone, limit=numbergame)

        except Exception as e:
            channel = client.get_channel(786564015357689896)
            await channel.send(
                f'{e}\nwhile get game history\nuser used: {usernametoco}\n password used: {passwordtoco}\n try to find: {user}')
        if len(results) == 0 or results is None:
            channel = client.get_channel(778996335348023316)  # change id for join########################################
            await channel.send('didnt get any games that weard.....')
            channel = client.get_channel(786564015357689896)
            await channel.send(
                f'while get game history\nuser used: {usernametoco}\n password used: {passwordtoco}\n try to find: {user}')
            return
        if nameGame == 'd':
            usertofind = user.split('#')
            usertofind = usertofind[0]
            for i in range(len(results) - 1):
                killsteam = 0
                teamplayers = {}
                game = results[i]
                gamedata = await game.details()
                timestartg = gamedata["allPlayers"][0]["utcStartSeconds"]
                for j in gamedata["allPlayers"]:
                    if usertofind.lower() == j["player"]["username"].lower():
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
                channel = client.get_channel(787705808762568724)  # change id for join########################################
                teamplayerslist = list(teamplayers)
                await channel.send(f'-----------------------------------------------------------------------------------------------------------')
                await channel.send(f'your game number: **{i + 1}**')
                for u in range(len(teamplayerslist) - 1):
                    await channel.send(f'player number {u + 1} in the team:\n**{teamplayerslist[u]}** did: {int(teamplayers[teamplayerslist[u]]["kills"])} kills\n')
                await channel.send(f'your team finish at **{int(teamplayers["Team"]["rankTeam"])} place**\nyour team did **{int(teamplayers["Team"]["killsTeam"])} kills**')

        else:
            if '#' in nameGame:
                nameGame = nameGame.split('#')
                usertofind = nameGame[0]
            else:
                usertofind = nameGame
            for i in range(len(results) - 1):
                killsteam = 0
                teamname = None
                teamplayers = {}
                game = results[i]
                gamedata = await game.details()
                f = open("myfile.txt", "w")
                f.write(str(gamedata)+"\n")
                if 'br_dmz_plnbld' in gamedata["allPlayers"][0]["mode"]:
                    channel = client.get_channel(787705808762568724)
                    await channel.send(
                        f'-----------------------------------------------------------------------------------------------------------')
                    await channel.send(f'your game number {i + 1} is plunder so skip it')
                    break
                timestartg = gamedata["allPlayers"][0]["utcStartSeconds"]
                for j in gamedata["allPlayers"]:
                    if usertofind.lower() == j["player"]["username"].lower():
                        teamname = j["player"]["team"]
                        break
                if teamname is None:
                    channel = client.get_channel(787705808762568724)  # change id for join########################################
                    await channel.send('didnt find the name you provid in the game')
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
                channel = client.get_channel(787705808762568724)  # change id for join########################################
                teamplayerslist = list(teamplayers)
                await channel.send(f'-----------------------------------------------------------------------------------------------------------')
                await channel.send(f'your game number: **{i + 1}**')
                for u in range(len(teamplayerslist) - 1):
                    await channel.send(
                        f'player number {u + 1} in the team:\n**{teamplayerslist[u]}** did: {int(teamplayers[teamplayerslist[u]]["kills"])} kills\n')
                await channel.send(f'your team finish at **{int(teamplayers["Team"]["rankTeam"])} place**\nyour team did **{int(teamplayers["Team"]["killsTeam"])} kills**')



@client.command(name='stats')
async def get_stats(ctx, userto='me', option='1'):
    if (userto == 'me'):
        person = ctx.message.author
        member = person
    else:
        person = userto
        if isinstance(person, str):
            person = await clearmen(ctx, userto)
        member = person

    person = {"discordid": member.id}
    person = players.find_one(person)
    if person is not None:
        if option == '1':
            ma = await ctx.send("**Fetching stats, you'll get them in no time!**")
        info = await kd(person["Game-id"], member, person["Platform"])
        if option == '2':
            await giverole(member, info)
            return info
        if option == '1':
            await massgeform(info, person["discord-name"], ma)
            await giverole(member, info)
    else:
        if option == '1':
            channel = member.guild.get_channel(778996335348023316)
            await massgeformsend(member, 'You are not in the DATABASE Please signup\n use: !signup', channel)
            return
        usertype_member = client.get_user(member.id)
        usertype_member_bot = usertype_member.bot
        if usertype_member_bot == False:
            await massgeformsend(member, 'You are not in the DATABASE Please signup\n use: !signup')

@client.command(name='דאשאד')
async def get_stats2(ctx, userto='me', option='1'):
    await get_stats(ctx, userto, option)

@client.command(name='signup')
async def signup(ctx, *, acid=None):
    member = ctx.message.author
    if acid is None:
        channel = client.get_channel(778996231971405845)
        await massgeformsend(member, 'To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For example: !signup GiantPiG#3577779', channel)
        return
    if len(acid) <= 3:
        channel = client.get_channel(778996231971405845)
        await massgeformsend(member, 'Error!  username must be more than 3 letters', channel)
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
        if dosefond != False:
            role = get(ctx.message.guild.roles, name="Artemis Member")
            await member.add_roles(role)
            info = dosefond
            await massgeform(info, member.display_name)
            await giverole(member, info)
            await discord.Message.delete(masign)
            botsign = discord.Embed(title='Welcome to Artemis Warzone Discord', description="", color=0x00ff00)
            botsign.add_field(name='Hello ' + member.display_name, value="Thank you for Signing up to ArtemisBot! from now on you can use the command !stats in #bot-stats to check your stats and update them.", inline=False)
            botsign.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg')
            await ctx.send(embed=botsign)
        else:
            await discord.Message.delete(masign)
            await ctx.send("Account hasn't been found, please copy your ID correctly.")
    else:
        await discord.Message.delete(masign)
        await ctx.send("Either your Discord account is signed up, or your Activision / Battle.net is signed up on a different Discord account.\n To update your stats, use #bot-stats and type the command !stats")

@client.command(name='resignup')
async def resignup(ctx, *, acid=None):
    member = ctx.message.author
    channel = member.guild.get_channel(778996231971405845)
    if acid is None:
        await ctx.send('To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For example: !signup GiantPiG#3577779')
        return
    masign = await ctx.send("**Resign up event has been Start!**")
    mas = ctx.message
    time.sleep(1)
    await mas.delete()
    dosefond = await kd(acid, member)
    if(dosefond == False):
        await discord.Message.delete(masign)
        await massgeformsend(member, f'I am Sorry but I colud not find you with {acid}', channel)
        return
    person = {"discordid": member.id}
    person = players.find_one(person)
    if person is not None:
        newvalues = {"$set": {"Game-id": acid}}
        players.update_one(person, newvalues)

        person = {"discordid": member.id}
        person = players.find_one(person)
        newvalues = {"$set": {"Platform": dosefond['optionsearch']}}
        players.update_one(person, newvalues)
        await discord.Message.delete(masign)
        await massgeformsend(member,f'Hi {member.display_name} Welcom to Artemis once again your ID as been update',channel)
    else:
        await discord.Message.delete(masign)
        await massgeformsend(member, f'I am Sorry but I colud not find you at the Data base. that mean you never signup yet', channel)



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
    info = await get_stats('junck', member, '2')
    kd = str(info['kd'])
    kdweekly =str(info["kdweekly"])
    wins = str(info["wins"])
    gamep = str(info["gamesPlayed"])
    winp = str(info["winprecent"])
    channel = member.guild.get_channel(778996619520901150)
    await channel.send('**'+member.display_name+'** looking for a group!\n**His Stats:** \nKD: '+kd+'          Weekly KD: '+kdweekly+'\nWins: '+wins+'    Game Played: '+gamep+'    Win Rate: '+winp+'%\n')
    if VoiceChannel is not None:
        await channel.send(invaite)

@client.command(name='ךכע')
async def lfg2(ctx):
    await lfg(ctx)

@client.command(name='cc')
async def clanc(ctx, clanname, pu1, pu2 ='def', pu3='def'):
    global eventopen
    if eventopen == True:
        member = ctx.message.author
        pu1 = await clearmen(ctx, pu1)
        if pu2 != 'def':
            pu2 = await clearmen(ctx, pu2)
        if pu3 != 'def':
            pu3 = await clearmen(ctx, pu3)
        person = {"discordid": member.id}
        person = players.find_one(person, {"info": 0})
        pu1 = {"discordid": pu1.id}
        pu1 = players.find_one(pu1, {"info": 0})
        if pu2 != 'def':
            pu2 = {"discordid": pu2.id}
            pu2 = players.find_one(pu2, {"info": 0})
        if pu3 != 'def':
            pu3 = {"discordid": pu3.id}
            pu3 = players.find_one(pu3, {"info": 0})
        if pu1 is None or pu2 is None or pu3 is None:
            await ctx.send("One of the player you tag is not signup to the Bot yet.\nBecause of that reason the clan can't be create")
            return None
        p1 = clan.find_one({'peopletoc': [pu1]})
        p2 = None
        p3 = None
        if pu2 != 'def':
            p2 = find(clan, 'peopletoc', pu2)
        if pu3 != 'def':
            p3 = find(clan, 'peopletoc', pu3)
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
        cc = {'clan': clanname}
        cc = clan.find_one(cc)
        if cc is None:
            if pu2 != 'def' and pu3 != 'def':
                data = {'clan':clanname, 'playerin':[person], 'peopletoc':[pu1, pu2, pu3], 'channel_clan_id': None}
            elif pu2 != 'def' and pu3 == 'def':
                data = {'clan': clanname, 'playerin': [person], 'peopletoc': [pu1, pu2], 'channel_clan_id': None}
            elif pu2 == 'def' and pu3 == 'def':
                data = {'clan': clanname, 'playerin': [person], 'peopletoc': [pu1], 'channel_clan_id': None}
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
async def join(ctx, actouser = None):
    member = ctx.message.author
    if actouser is None:
        await ctx.send('please send your activition-id')
        return
    person = {"discordid": member.id}
    person = players.find_one(person, {"info": 0})
    data = find(clan, 'peopletoc', person)
    dataowe = find(clan, 'playerin', person)
    if data is None and dataowe is None:
        await ctx.send('cant find you in any clan')
        return
    if dataowe is not None:
        append_value(person, 'usergame', actouser)
        dataowe['playerin'][0] = person
        person1 = {"discordid": member.id}
        person1 = players.find_one(person1, {"info": 0})
        newvalues = {"$set": {'playerin': dataowe['playerin']}}
        dd = find(clan, 'playerin', person1)
        clan.update_one(dd, newvalues)
        return
    data['peopletoc'].pop(data['peopletoc'].index(person))
    append_value(person, 'usergame', actouser)
    data['playerin'].append(person)
    kk = data['playerin'][0]
    newvalues = {"$set": {'playerin': data['playerin']}}
    person1 = {"discordid": member.id}
    person1 = players.find_one(person1, {"info": 0})
    cc = find(clan, 'playerin', kk)
    clan.update_one(cc, newvalues)
    newvalues = {"$set": {'peopletoc':data['peopletoc']}}
    cc = find(clan, 'peopletoc', person1)
    clan.update_one(cc, newvalues)
    g = client.get_guild(710393755299217492) ################### discord id ############
    user = g.get_member(member.id)
    await user.send(f'thanks you for join to {data["clan"]} clan')
    if len(data['peopletoc']) == 0:
        id = data['playerin'][0]['discordid']
        g = client.get_guild(710393755299217492) ################### discord id #############
        user = g.get_member(id)
        await user.send(f'Your clan {data["clan"]} is all set up members: ')
        for i in range(len(data['playerin'])):
            await user.send(f"{data['playerin'][i]['discord-name']}")
        await create_channel_clan(data)

async def create_channel_clan(data):
    dataafter = find(clan, 'clan', data['clan'])
    g = client.get_guild(710393755299217492)  ################### discord id #############
    channel_to_clone = g.get_channel(784049072171778068) ################### Voice_channel id to clone #############
    channel_clan = await channel_to_clone.clone(name=dataafter["clan"])
    overwrite = discord.PermissionOverwrite()
    overwrite.connect = True
    for i in range(len(dataafter['playerin'])):
        id = dataafter['playerin'][i]['discordid']
        member = g.get_member(id)
        await channel_clan.set_permissions(member, overwrite=overwrite)
    channel_clan_id = channel_clan.id
    dataafter['channel_clan_id'] = channel_clan_id
    newvalues = {"$set": {'channel_clan_id': dataafter['channel_clan_id']}}
    cc = find(clan, 'clan', data['clan'])
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
    g = client.get_guild(710393755299217492)   ################### discord id ############
    user = g.get_member(own['discordid'])
    await user.send(f'{member.display_name} is cancel your invaite to the {clann} clan in the tornamenrt.')
    data['peopletoc'].pop(data['peopletoc'].index(person))
    newvalues = {"$set": {'peopletoc':data['peopletoc']}}
    clan.update_one(cc, newvalues)
    user = g.get_member(member.id)
    await user.send(f'thanks you are out form {data["clan"]} clan')
    if len(data['peopletoc']) == 0:
        id = data['playerin'][0]['discordid']
        g = client.get_guild(710393755299217492) ################### discord id #############
        user = g.get_member(id)
        await user.send(f'Your clan is all set up members: ')
        for i in range(len(data['playerin'])):
            await user.send(f"{data['playerin'][i]['discord-name']}")
        await create_channel_clan(data)

@client.command(name='ton')
async def tournamenet(ctx):
    member = ctx.message.author
    global eventopen
    global clan
    global games
    global timesgame
    for r in member.roles:
        if r.name == 'Private Match Manager':
            eventopen = True
            clan = discordlab["clan"]
            games = discordlab["games"]
            timesgame = discordlab["timesgame"]
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
            for i in x['playerin']:
                callofdutywebuser = await doconnect()
                playerTeamFound = await getmatchs(i['usergame'], i["Game-id"], callofdutywebuser[0], callofdutywebuser[1], x['clan'], i['Platform'])
                if playerTeamFound:
                    break
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
    global clan
    global games
    for r in member.roles:
        if r.name == 'Private Match Manager':
            eventopen = False
            await clear_rooms()
            c1 = clan.drop_collection()
            c2 = games.drop_collection()
            c3 = timesgame.drop_collection()
            await ctx.send(f'clan collection drop: {c1}\n games collection drop: {c2}\n times collection drop: {c3} ')

async def clear_rooms():
    for i in clan.find():
        channel_del_id = i['channel_clan_id']
        if channel_del_id is not None:
            channel_del = client.get_channel(channel_del_id)
            if channel_del is not None:
                await channel_del.delete()

@client.command(name='onetime')
async def onetime_function(ctx):
    member = ctx.message.author
    for _ in players.find():
        myquery = {"discordid": _["discordid"]}
        newvalues = {"$set": {}}
        players.update_one(myquery, newvalues)
    await ctx.send("done add")


client.run(TOKEN)