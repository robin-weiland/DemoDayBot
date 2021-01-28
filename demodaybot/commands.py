#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.0"

__all__ = ('DDBot',)

from discord.utils import get
from demodaybot.storage import Storage
from demodaybot.data import voting_channels, games, orga, members, VOTES_PATH
from discord.ext.commands import Bot, Command
from discord.ext import commands
from discord import Activity, ActivityType, File, Intents, Guild, Role
from logging import getLogger

intents = Intents.default()
intents.members = True


storage = Storage(VOTES_PATH)

system_logger = getLogger('System')
chat_logger = getLogger('Chat')
vote_logger = getLogger('Vote')
vote_error_logger = getLogger('VoteError')

VOTE_ACTIVE = False  # I HATE global variables


class DDBot(Bot):
    VOTE_ACTIVE: bool = False
    guild: Guild
    ORGA: Role
    EXPO: Role
    VISITOR: Role

    def __init__(self):
        super(DDBot, self).__init__(command_prefix='!', intents=intents)

        for f in self.__class__.__dict__.values():
            if isinstance(f, Command): self.add_command(f)

        self.voting_channels = list()
        self.VOTE_ACTIVE = False

    async def on_ready(self):
        await self.change_presence(activity=Activity(type=ActivityType.playing, name="your cool games"))
        self.guild = [guild for guild in self.guilds if guild.name == 'DemoDay 2021'][0]
        self.voting_channels = [category for category in self.guild.categories if category.name == 'VOTING'][0].channels
        # self.ORGA = get(self.guild.roles, id='791315139898114088')
        # self.EXPO = get(self.guild.roles, id='791315170215460864')
        # self.VISITOR = get(self.guild.roles, id='791315081992077342')
        self.ORGA = get(self.guild.roles, name='Orga')
        self.EXPO = get(self.guild.roles, name='Aussteller')
        self.VISITOR = get(self.guild.roles, name='Besucher')
        system_logger.info('Connected!')
        system_logger.debug(f'Voting-Channels: {self.voting_channels}')

    async def on_member_join(self, member):
        system_logger.info(f'{member.name} [{member.id}|{member.top_role.name}] joined!')
        await member.send(f'Hallo **{member.name}**. Willkommen auf dem DemoDay 2021!')
        return  # apparently
        if member.id in orga:
            await member.add_roles(self.ORGA)
            await member.edit(nick=f'{member.name} (Orga)')
        elif member.id in members:
            await member.add_roles(self.EXPO)
            for game in games:
                if member.id in game['members']:
                    await member.edit(nick=f'{member.name} [{game["short"]}]')
                    break
        else:
            await member.add_roles(self.VISITOR)


    async def on_message(self, message):
        if message.author == self.user: return
        await self.process_commands(message)
        chat_logger.info(f'[{message.author.name} | {message.author.id} || {message.channel.name}] {message.content}')
        # if message.channel.id not in voting_channels.values(): return
        if message.channel in self.voting_channels:
            if VOTE_ACTIVE:
                try:
                    number = int(message.content) - 1
                    storage[message.author.id][tuple(voting_channels.values()).index(message.channel.id) - 1] = number
                    await message.author.send(
                        f'Deine Stimme **{games[number]["name"]}** für die Kategorie _{message.channel.name}_ wurde erfolgreich gezählt!'
                    )
                    vote_logger.info(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{message.content}]')
                except ValueError:
                    await message.author.send(f'Es trat ein Fehler bei Deiner Wahl für _{message.channel.name}_ auf!')
                    vote_error_logger.error(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{message.content}]')
                except (IndexError, OverflowError,):
                    await message.author.send(f'Es können nur `0` (Rücknahme der Stimme) bis {len(games)} gewählt werden!')
                    vote_error_logger.error(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{message.content}]')
                finally:
                    await message.delete()
            else:
                await message.delete()
                await message.author.send(f'Die Abstimmung ist (noch) nicht aktiviert!')

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
    async def poll_activate(ctx) -> None:
        global VOTE_ACTIVE
        VOTE_ACTIVE = True
        system_logger.info(f'Poll activated by {ctx.author.name}!')
        await ctx.channel.send('Poll activated!')

    @commands.command(name='poll-deactivate')
    @commands.has_role('Orga')
    async def poll_deactivate(ctx) -> None:
        global VOTE_ACTIVE
        VOTE_ACTIVE = False
        system_logger.info(f'Poll deactivated by {ctx.author.name}!')
        await ctx.channel.send('Poll deactivated!')

    @commands.command(name='poll-status')
    @commands.has_role('Orga')
    async def poll_status(ctx) -> None:
        system_logger.info(f'Poll status requested by {ctx.author.name}!')
        await ctx.channel.send(f'Poll is **{"active" if VOTE_ACTIVE else "inactive"}**!\n**{len(storage)}** people have at least partially voted!')

    @commands.command(name='poll-result')
    @commands.has_role('Orga')
    async def poll_result(ctx, *names) -> None:
        try:
            if 'art' in names or not names:
                with storage.result('best-art') as file:
                    await ctx.send(file=File(file, filename=f'best-art.png'))
            if 'tech' in names or not names:
                with storage.result('best-technology') as file:
                    await ctx.send(file=File(file, filename=f'best-technology.png'))
            if 'design' in names or not names:
                with storage.result('best-design') as file:
                    await ctx.send(file=File(file, filename=f'best-design.png'))
            if 'story' in names or not names:
                with storage.result('best-story') as file:
                    await ctx.send(file=File(file, filename=f'best-story.png'))
            if 'sound' in names or not names:
                with storage.result('best-sound') as file:
                    await ctx.send(file=File(file, filename=f'best-sound.png'))
            if 'meme' in names or not names:
                with storage.result('best-meme') as file:
                    await ctx.send(file=File(file, filename=f'best-meme.png'))
            if 'inclusive' in names or not names:
                with storage.result('most-inclusive') as file:
                    await ctx.send(file=File(file, filename=f'most-inclusive.png'))
            if 'poster' in names or not names:
                with storage.result('best-poster') as file:
                    await ctx.send(file=File(file, filename=f'best-poster.png'))
            if 'experimental' in names or not names:
                with storage.result('experimental-projects') as file:
                    await ctx.send(file=File(file, filename=f'experimental-projects.png'))
        except Exception as exc:
            await ctx.channel.send(f'Failed to get results! {exc.__class__.__name__}: {exc}')


if __name__ == '__main__': pass
