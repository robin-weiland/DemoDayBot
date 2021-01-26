#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.0"

__all__ = ('DDBot',)

from discord.utils import get
from demodaybot.storage import Storage
from demodaybot.data import voting_channels, VOTES_PATH
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Activity, ActivityType
from logging import getLogger

storage = Storage(VOTES_PATH)

system_logger = getLogger('System')
chat_logger = getLogger('Chat')
vote_logger = getLogger('Vote')
vote_error_logger = getLogger('VoteError')

VOTE_ACTIVE = False  # I HATE global variables


class DDBot(Bot):
    VOTE_ACTIVE: bool = False

    def __init__(self):
        super(DDBot, self).__init__(command_prefix='!')
        self.add_command(self.save)
        self.voting_channels = list()
        self.VOTE_ACTIVE = False

    async def on_ready(self):
        await self.change_presence(activity=Activity(type=ActivityType.playing, name="your cool games"))
        guild = [guild for guild in self.guilds if guild.name == 'DemoDay 2021'][0]
        self.voting_channels = [category for category in guild.categories if category.name == 'VOTING'][0].channels
        system_logger.info('Connected!')
        system_logger.debug(f'Voting-Channels: {self.voting_channels}')

    async def on_member_join(self, member):
        await self.add_roles(member, get(member.server.roles, id='791315081992077342'))  # 'Besucher' id
        system_logger.info(f'{member.name} [{member.id}] joined!')
        member.send(f'Hallo {member.name}. Willkommen auf dem DemoDay 2021!')

    async def on_message(self, message):
        if message.author == self.user: return
        await self.process_commands(message)
        chat_logger.info(f'[{message.author.name} | {message.author.id} || {message.channel.name}] {message.content}')
        # if message.channel.id not in voting_channels.values(): return
        if self.VOTE_ACTIVE and message.channel in self.voting_channels:
            try:
                number = int(message.content)
                storage[message.author.id][tuple(voting_channels.values()).index(message.channel.id) - 1] = number
                await message.author.send(f'Your vote _{number}_ for _{message.channel.name}_ has been counted!')
                vote_logger.info(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{message.content}]')
            except ValueError:
                await message.author.send(f'There was an error with your vote for the _{message.channel.name}_ category!')
                vote_error_logger.error(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{message.content}]')
            finally:
                await message.delete()
        elif message.channel.name == 'poll-admin':
            await message.delete()
            await message.author.send(f'Deleted message your message: "{message.content[:20]}{"..." if len(message.content) > 20 else ""}"')

    @commands.command(name='save')
    @commands.has_role('Orga')
    async def save(ctx) -> None:
        try:
            storage.save()
            await ctx.channel.send('Votes Saved!')
            system_logger.info(f'Votes saved by "{ctx.author.name}!"')
        except Exception as exc:
            system_logger.error(f'Vote saving attempt by "{ctx.author.name}" failed! [{exc.__class__.__name__}: {exc}]')
            await ctx.channel.send(f'Vote saving attempt failed! [{exc.__class__.__name__}: {exc}]')

    @commands.command(name='poll-activate')
    @commands.has_role('Orga')
    async def vote_activate(ctx) -> None:
        global VOTE_ACTIVE
        VOTE_ACTIVE = True
        await ctx.channel.send('Poll avitvated!')

    @commands.command(name='poll-deactivate')
    @commands.has_role('Orga')
    async def vote_activate(ctx) -> None:
        global VOTE_ACTIVE
        VOTE_ACTIVE = False
        await ctx.channel.send('Poll deactivated!')


if __name__ == '__main__': pass
