import itertools
import pathlib

from typing import Optional

import discord
import discord.ext
import discord.abc
from callofduty import Title, Mode
from discord.ext.commands import Context

import callofduty

from call_of_duty_handler import get_cod_client


ERROR_THUMBNAIL_URL = 'https://i.ibb.co/QJVMZwD/Whats-App-Image-2020-11-16-at-13-24-22.jpg'
SIGNUP_CHANNEL_NAME = 'bot-signup'

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


async def get_player_by_game_id(member: discord.Member, game_id: str) -> Optional[callofduty.Player]:
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

    return potential_players[0]


@bot_client.command(name='signup')
async def signup(ctx: Context, *, game_id: str = None):
    member = ctx.author

    if game_id is None:
        await raise_error(
            member,
            'To sign up please type your Activision ID | Battle.Net ID | PSN | Xbox-ID '
            'at the end of the command.\n For example: !signup GiantPiG#3577779',
            get_channel_by_name(SIGNUP_CHANNEL_NAME)
        )
        return

    if game_id is in use:

    if discord member already signed up:


    wait_message = await ctx.send('**Checking your username, Please wait....**')

    await ctx.message.delete()

    cod_user = get_player_by_game_id(member, game_id)

    if cod_user is None:
        await wait_message.delete()
        return





if __name__ == '__main__':
    bot_client.run(read_token())
