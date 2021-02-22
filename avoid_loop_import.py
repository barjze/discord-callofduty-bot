import discord
import discord.ext
import discord.abc
from discord.ext.commands import Context
from discord.utils import get
import pymongo
import pathlib
from callofduty import Platform

myMongo = pymongo.MongoClient('mongodb://localhost:1111/')
discordlab = myMongo["discord-data"]
players = discordlab["players"]

ERROR_THUMBNAIL_URL = 'https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg'
Bot_Embed_Massage_THUMBNAIL_URL = 'https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg'
SIGNUP_CHANNEL_NAME = 'bot-signup'
STATS_CHANNEL = "bot-stats"
LFG_CHANNEL = "bot-lfg"
LAST_MATCH_CHANNEL = "bot-last-matches"
ERROR_CHANNEL = "error-bot"
GILD_MEMBER_ROLE = "Artemis Member"
Minutes_to_pull_data_again = 30

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

def read_token(path: pathlib.Path = pathlib.Path('DISCORD_TOKEN.env')) -> str:
    return path.read_text().split("=")[1]

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


async def raise_error(member: discord.Member, message: str, channel=None):

    message_sender = member if channel is None else channel

    error_message = discord.Embed(
        title=f'Dear {member.display_name} this is error message',
        description='',
        color=0xff0000
    )

    error_message.add_field(
        name=f'Hello {member.display_name}',
        value=message,
        inline=False
    )

    error_message.set_thumbnail(url=ERROR_THUMBNAIL_URL)

    await message_sender.send(embed=error_message)


def get_role_by_name(ctx: Context, name_of_role: str, guild: discord.Guild = None):
    """this function get ctx: Context and name_of_role: str, return role type"""
    if guild is not None:
        role = get(guild.roles, name=f"{name_of_role}")
        return role
    role = get(ctx.message.guild.roles, name=f"{name_of_role}")
    return role


