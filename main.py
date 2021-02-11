import itertools
import pathlib
import pymongo
from typing import Optional
import discord
import discord.ext
import discord.abc
from callofduty import Title, Mode
from discord.ext.commands import Context
from discord.ext import commands
import callofduty
from discord.utils import get
from call_of_duty_handler import get_cod_client
from player import Player

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

myMongo = pymongo.MongoClient('mongodb://localhost:1111/')
discordlab = myMongo["discord-data"]
players = discordlab["players"]

ERROR_THUMBNAIL_URL = 'https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg'
SIGNUP_CHANNEL_NAME = 'bot-signup'
GILD_MEMBER_ROLE = "Artemis Member"

platform_matcher = {
            'Activision': Platform.Activision,
            'Xbox': Platform.Xbox,
            'BattleNet': Platform.BattleNet,
            'PlayStation': Platform.PlayStation,
        }

def initialize_bot() -> discord.ext.commands.Bot:
    intents = discord.Intents.default()
    intents.members = True

    return discord.ext.commands.Bot(command_prefix='!', intents=intents)


def read_token(path: pathlib.Path = pathlib.Path('DISCORD_TOKEN')) -> str:
    return path.read_text()


bot_client = initialize_bot()


def get_channel_by_name(channel_name: str) -> discord.abc.GuildChannel:
    relevant_channels = [
        channel
        for channel
        in bot_client.get_all_channels()
        if channel.name == channel_name
    ]

    if len(relevant_channels) != 1:
        raise ValueError('No such channel!')

    return relevant_channels[0]


async def raise_error(member: discord.Member, message: str, channel=Optional[discord.TextChannel]):

    message_sender = member if channel is None else channel

    error_message = discord.Embed(
        title=f'Dear {member.display_name}',
        description='',
        color=0xff0000
    )

    error_message.add_field(
        name=f'Hello {member.mention}',
        value=message,
        inline=False
    )

    error_message.set_thumbnail(url=ERROR_THUMBNAIL_URL)

    await message_sender.send(embed=error_message)


async def get_player_stats_by_game_id(member: discord.Member, game_id: str) -> Optional[callofduty.Player]:
    client = get_cod_client()

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

    return potential_players[0].profile

def find_player_by_Game_id(Gameid, member: discord.Member):
    x = {"Game-id": Gameid}
    person = players.find_one(x)
    if person == None:
        return None
    person = Player(member.guild, member.id, Gameid, platform_matcher[person['Platform']])
    return person

def find_player_by_discord_id(member: discord.Member):
    x = {"discordid": member.id}
    person = players.find_one(x)
    if person == None:
        return None
    person = Player(member.guild, member.id, person['Game-id'], platform_matcher[person['Platform']])
    return person

def get_role_by_name(ctx: Context, name_of_role: str):
    role = get(ctx.message.guild.roles, name=f"{name_of_role}")
    return role

def add_player_to_data_base(data: dict):
    players.insert_one(data)

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

    cod_user = get_player_stats_by_game_id(member, game_id)

    if cod_user is None:
        await wait_message.delete()
        await raise_error(
            member,
            f'Didnt find any player with: {game_id} at call of duty api, that can be ether your profile is still privet or a bug.\nif you are sure you are not privet and is it your correct game id just try again',
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return
    else:
        data = {"discordid": member.id, "discord-name": member.display_name, "name-in-game": name_in_game, "Game-id": game_id, "Platform": paltformsearch, "info": []}
        add_player_to_data_base(data)
        role = get_role_by_name(ctx, GILD_MEMBER_ROLE)
        await member.add_roles(role)






if __name__ == '__main__':
    bot_client.run(read_token())
