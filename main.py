import itertools
import time
from typing import Optional
import discord
import discord.ext
import discord.abc
from callofduty import Title, Mode
from discord.ext.commands import Context
import callofduty
from call_of_duty_handler import CodClient
from database_player import DATABase_Player
from player_stats import make_player_stats_from_JSON_DATA
from player_stats import PlayerStats
from avoid_loop_import import myMongo,discordlab,players,ERROR_THUMBNAIL_URL,Bot_Embed_Massage_THUMBNAIL_URL,SIGNUP_CHANNEL_NAME,STATS_CHANNEL,LFG_CHANNEL,LAST_MATCH_CHANNEL,ERROR_CHANNEL,GILD_MEMBER_ROLE,Minutes_to_pull_data_again,platform_matcher,get_channel_by_name,raise_error,get_role_by_name,initialize_bot,read_token,bot_client



async def Bot_Embed_Massage(member: discord.Member, title: str, massage: str, channel):
    message_sender = member if channel is None else channel
    botsign = discord.Embed(title=title, description="", color=0x00ff00)
    botsign.add_field(name='Dear ' + member.display_name,
                      value=massage,
                      inline=False)
    botsign.set_thumbnail(url=Bot_Embed_Massage_THUMBNAIL_URL)
    await message_sender.send(embed=botsign)


async def get_player_stats_by_game_id(member: discord.Member, game_id: str) -> Optional[callofduty.Player]:
    """This function get member: discord.Member and game_id: str and return PlayerStats: PlayerStats, Platform"""
    client = CodClient()

    potential_players = list(itertools.chain.from_iterable(
        client.SearchPlayers(platform, game_id, limit=3)
        for platform
        in callofduty.Platform
    ))

    if len(potential_players) > 1:
        await raise_error(
            member,
            f"Found more than one Account ID with the following name {member.name} "
            f"Please provide your entire ID as written on the platform you're using.",
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return None

    if len(potential_players) == 0:
        await raise_error(
            member,
            'Uh oh, Something went wrong while searching for your Account ID. Please try again!\n'
            ' **in case you try to signup** Please try with battlenet|Activition insted',
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return None

    return make_player_stats_from_JSON_DATA(potential_players[0].profile(Title.ModernWarfare, Mode.Warzone)), potential_players[0].platform

def find_player_by_Game_id(Gameid, member: discord.Member):
    x = {"Game-id": Gameid}
    person = players.find_one(x)
    if person == None:
        return None
    player_member = DATABase_Player(discord_guild=member.guild,
                                    discord_id=member.id,
                                    game_id=person['Game-id'],
                                    platform=platform_matcher[person['Platform']],
                                    player_stats_list=person['info'],
                                    name_in_game=person['name-in-game'])
    return player_member

def find_player_by_discord_id(member: discord.Member):
    x = {"discord-id": member.id}
    person = players.find_one(x)
    if person == None:
        return None
    player_member = DATABase_Player(discord_guild=member.guild,
                                    discord_id=member.id,
                                    game_id=person['Game-id'],
                                    platform=platform_matcher[person['Platform']],
                                    player_stats_list=person['info'],
                                    name_in_game=person['name-in-game'])
    return player_member

def mention_to_member(ctx: Context, userto: str):
    """this function get 'ctx' and a mention of Discord.Member ( ->str ) and return Discord.Member type of the member"""
    userto = userto[3:-1]
    member = ctx.guild.get_member(int(userto))
    return member



def add_player_to_data_base(member: discord.Member, player_stats: PlayerStats, Platform, Game_id):
    data = {"discord-id": member.id, "discord-name": member.display_name, "name-in-game": "did'nt_provide_yet",
            "Game-id": Game_id, "Platform": Platform, "info": [player_stats.asdict()]}
    players.insert_one(data)
    return DATABase_Player(
        discord_guild=member.guild,
        discord_id=member.id,
        game_id=Game_id,
        name_in_game="did'nt_provide_yet",
        platform=Platform,
        player_stats_list=[player_stats]
        )



@bot_client.event
async def on_ready():
    print(f'{bot_client.user.name} has connected to Discord!')

@bot_client.event
async def on_member_join(member):
    botwelcom = discord.Embed(title='Welcome to Artemis Warzone Discord', description="", color=0x00ff00)
    botwelcom.add_field(name='Hello '+member.display_name, value="Please sign up to the bot by typing your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For Example: !signup GiantPiG#3577779", inline=False)
    botwelcom.set_thumbnail(url='https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg') ####not touch
    await member.send(embed=botwelcom)

@bot_client.command(name='signup')
async def signup_command(ctx: Context, *, game_id: str = None):
    member = ctx.author

    if game_id is None:
        await raise_error(
            member,
            'To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID '
            'at the end of the command.\n For example: !signup GiantPiG#3577779',
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return

    is_he_already_exist = find_player_by_Game_id(game_id, member)
    if is_he_already_exist is not None:
        await raise_error(
            member,
            f'Another discord member: {is_he_already_exist.discord_name} is already signup with this game id you provide: {game_id}',
            get_channel_by_name(SIGNUP_CHANNEL_NAME))
        return

    is_he_already_exist = find_player_by_discord_id(member)
    if is_he_already_exist is not None:
        await raise_error(
            member,
            f'You already sign with: {is_he_already_exist.game_id} if you do like to change use "!resignup" command',
            get_channel_by_name(SIGNUP_CHANNEL_NAME))
        return


    wait_message = await ctx.send('**Checking your username, Please wait....**')
    await ctx.message.delete()

    member_player_stats, Platform_player = get_player_stats_by_game_id(member, game_id)

    if member_player_stats is None:
        await wait_message.delete()
        await raise_error(
            member,
            f'Didnt find any player with: {game_id} at call of duty api, that can be ether your profile is still privet or a bug.\nif you are sure you are not privet and is it your correct game id just try again',
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return

    else:
        DATABase_Player = add_player_to_data_base(member, member_player_stats, Platform_player, game_id)
        role = get_role_by_name(ctx, GILD_MEMBER_ROLE)
        await member.add_roles(role)
        await DATABase_Player.give_KD_roles()
        await member_player_stats.stats_massage_form(member,"stats", wait_message)
        await Bot_Embed_Massage(
            member,
            'Welcome to Artemis Warzone Discord',
            'Thank you for Signing up to ArtemisBot! from now on you can use the command !stats in #bot-stats to check your stats and update them.',
        get_channel_by_name(SIGNUP_CHANNEL_NAME))

@bot_client.command(name='resignup')
async def re_signup_command(ctx: Context, *, game_id: str = None):
    member = ctx.message.author
    if game_id is None:
        await raise_error(member,
                          'To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID at the end of the command.\n For example: !signup GiantPiG#3577779',
                          get_channel_by_name(SIGNUP_CHANNEL_NAME))
        return
    wait_message = await ctx.send("**Resign up event has been Start!**")
    message_member_send = ctx.message
    time.sleep(1)
    await message_member_send.delete()

    player_member = find_player_by_discord_id(member)
    if player_member is None:
        await raise_error(member,
                          'you are not in the database yet please signup first',
                          get_channel_by_name(SIGNUP_CHANNEL_NAME))
        return

    player_member = find_player_by_Game_id(game_id)
    if player_member is not None:
        await raise_error(member,
                          f'i am sorry but {player_member.discord_name} is signup with {game_id} already',
                          get_channel_by_name(SIGNUP_CHANNEL_NAME))
        return


    player_stats_member, his_paltform = get_player_stats_by_game_id(member, game_id)
    if player_stats_member is None:
        await wait_message.delete()
        await raise_error(
            member,
            f'Didnt find any player with: {game_id} at call of duty api, that can be ether your profile is still privet or a bug.\nif you are sure you are not privet and is it your correct game id just try again',
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return
    else:
        player_member.change_game_id_and_platform(game_id, his_paltform)
        await player_stats_member.stats_massage_form(member, "stats", wait_message)
        await Bot_Embed_Massage(
            member,
            'Welcome to Artemis Warzone Discord Once again!',
            'Thank you for Signing up to ArtemisBot! from now on you can use the command !stats in #bot-stats to check your stats and update them.',
            get_channel_by_name(SIGNUP_CHANNEL_NAME))

@bot_client.command(name='nickname')
async def nickname_add_command(ctx: Context, name_in_game: str):
    member = ctx.author
    player_member = find_player_by_discord_id(member.id)
    if player_member is not None:
        if player_member.name_in_game == "did'nt_provide_yet":
            player_member.change_name_in_game(name_in_game)
            await Bot_Embed_Massage(member,
                                    "You set your nickname"
                                    "thanks for provide your name in the game now we can look for your stats at matches",
                                    ctx.channel)
        else:
            await Bot_Embed_Massage(member,
                                    "You already have nickname"
                                    f"your nickname is: {player_member.name_in_game} to change it use '!change_nickname'",
                                    ctx.channel)
    else:
        await raise_error(member,
                          "You are not in the database please signup first",
                          ctx.channel)

@bot_client.command(name='change_nickname')
async def change_nickname_command(ctx: Context, name_in_game: str):
    member = ctx.author
    player_member = find_player_by_discord_id(member.id)
    if player_member is not None:
        player_member.change_name_in_game(name_in_game)
        await Bot_Embed_Massage(member,
                                "You set your nickname"
                                "thanks once again for provide your name in the game now we can look for your stats at matches",
                                ctx.channel)
    else:
        await raise_error(member,
                          "You are not in the database please signup first",
                          ctx.channel)

@bot_client.command(name='stats')
async def stats_command(ctx: Context, userto: str ='me'):
    if (userto == 'me'):
        member = ctx.message.author
    else:
        member = mention_to_member(ctx, userto)

    player_member = find_player_by_discord_id(member)
    if player_member is not None:
        if player_member.check_if_to_pull_again_stats:
            member_player_stats = await player_member.pull_new_stats()
            player_member.add_stats(member_player_stats)
            await player_member.last_stats().stats_massage_form(member, "stats")
            await player_member.give_KD_roles()
        else:
            await player_member.last_stats().stats_massage_form(member, "stats")
    else:
        await raise_error(member,
                          "you are not in the database yet please signup first",
                          get_channel_by_name(STATS_CHANNEL))

@bot_client.command(name='דאשאד')
async def stats_command2(ctx: Context, userto: str ='me'):
    await stats_command(ctx, userto)

@bot_client.command(name='lfg')
async def lfg_command(ctx: Context):
    member = ctx.message.author
    LFG = get_channel_by_name(LFG_CHANNEL)
    player_member = find_player_by_discord_id(member)
    if player_member is not None:
        if player_member.check_if_to_pull_again_stats:
            member_player_stats = await player_member.pull_new_stats()
            player_member.add_stats(member_player_stats)
        await player_member.last_stats().stats_massage_form(member, "lfg")
        if member.voice is not None:
            voice_channel = member.voice.channel
            invite = await voice_channel.create_invite()
            await LFG.send(invite)
    else:
        await raise_error(member,
                          "you are not in the database yet please signup first",
                          LFG)

@bot_client.command(name='ךכע')
async def lfg_command_2(ctx: Context):
    await lfg_command(ctx)

@bot_client.command(name='lastmatch')
async def last_match_command(ctx: Context, Number_of_maches: int = 5):
    member = ctx.author
    player_member = find_player_by_discord_id(member)
    if player_member is None:
        await raise_error(member,
                    "you are not in the database yet please signup first",
                    get_channel_by_name(LAST_MATCH_CHANNEL))
        return
    if player_member.name_in_game == "did'nt_provide_yet":
        await raise_error(member,
                          "We need your nickname in the game for be able to do that please use '!nickname' first"
                          "and then try again",
                          get_channel_by_name(LAST_MATCH_CHANNEL))
        return
    await player_member.last_matches(Number_of_maches)

if __name__ == '__main__':
    bot_client.run(read_token())
