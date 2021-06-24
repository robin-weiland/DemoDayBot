#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.3"

__all__ = ('DDBot',)

from demodaybot.data import Data, load_games, load_members
from demodaybot.security import safe_format
from demodaybot.messages import WELCOME, MOBILE
from discord.ext.commands import Bot, Command
from discord.ext import commands
from discord.utils import get
from discord import Activity, ActivityType, File, Intents, Guild, Role, DMChannel
from logging import getLogger
from operator import attrgetter
from asyncio import sleep
from random import randint, choice

from typing import Dict

intents = Intents.default()
intents.members = True

data: Data = Data()

system_logger = getLogger('System')
chat_logger = getLogger('Chat')
vote_logger = getLogger('Vote')
vote_error_logger = getLogger('VoteError')


class DDBot(Bot):
    guild: Guild
    roles: Dict[str, Role]

    def __init__(self):
        super(DDBot, self).__init__(command_prefix='+', intents=intents)

        for f in self.__class__.__dict__.values():
            if isinstance(f, Command): self.add_command(f)

        self.remove_command('help')

    async def on_ready(self):
        try:
            await self.change_presence(activity=Activity(type=ActivityType.playing, name="your cool games"))
            self.guild = [guild for guild in self.guilds if guild.id == 791303033371099177][0]
            self.roles = dict((role.name, get(self.guild.roles, name=role.name)) for role in self.guild.roles)
            vchannels = [category for category in self.guild.categories if category.name == 'Voting'][0].channels
            data.voting_channels = dict(zip(map(attrgetter('name'), vchannels), map(attrgetter('id'), vchannels)))
            for member in self.guild.members:
                if member.id in [325354358734848020,
                                 285848592802119681,
                                 633391262795300883,
                                 200307065737052160,
                                 476484387324690450,
                                 317234575568928768,
                                 496296790400696330,
                                 413650836737097728,
                                 ]: continue
                if len(member.roles) == 1:
                    await member.add_roles(self.roles['Besucher'])
            system_logger.info('Connected!')
            await self.loop.create_task(self.change_status_after_time())
            await self.loop.create_task(self.save_poll())
        except Exception as ex:
            system_logger.warning(f'Error occured: on_ready(): {ex.__class__.__name__}: {ex}')

    async def on_member_join(self, member):
        try:
            system_logger.info(f'{member.name} [{member.id}|{member.top_role.name}] joined!')
            await member.send(safe_format(WELCOME, member=member.name))
            if member.is_on_mobile(): await member.send(MOBILE)
            await member.add_roles(self.roles['Besucher'])
        except Exception as ex:
            system_logger.warning(f'Error occured: on_member_join({member.id}): {ex.__class__.__name__}: {ex}')

    async def on_message(self, message):
        try:
            if message.author == self.user: return
            await self.process_commands(message)
            content = message.content.encode('utf-8')
            if isinstance(message.channel, DMChannel):
                await message.channel.send('Momentan kann ich Dir noch nicht helfen!')
                chat_logger.info(f'[{message.author.name} | {message.author.id} || DM] {content}')
            else:
                chat_logger.info(f'[{message.author.name} | {message.author.id} || {message.channel.name}] {content}')
            if message.channel.id in data.voting_channels.values():
                if data.vote_active:
                    try:
                        number = int(content)
                        if number not in range(len(data.games)): raise IndexError
                        data.storage[message.author.id][tuple(data.voting_channels.values()).index(message.channel.id)] = number
                        await message.author.send(
                            f'Deine Stimme **{data.games[number]["name"]}** für die Kategorie _{message.channel.name}_ wurde erfolgreich gezählt!'
                        )
                        vote_logger.info(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{content}]')
                    except ValueError:
                        await message.author.send(f'Es trat ein Fehler bei Deiner Wahl für _{message.channel.name}_ auf!')
                        vote_error_logger.error(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{content}]')
                    except (IndexError, OverflowError,):
                        await message.author.send(f'Es können nur `0` (Rücknahme der Stimme) bis `{len(data.games) - 1}` gewählt werden!')
                        vote_error_logger.error(f'[{message.author.name}|{message.author.id}][{message.channel.name}][{content}]')
                    finally:
                        await message.delete()
                else:
                    await message.delete()
                    await message.author.send(f'Die Abstimmung ist (noch) nicht aktiviert!')
        except Exception as ex:
            system_logger.warning(f'Error occured: on_message({message.id}): {ex.__class__.__name__}: {ex}')

    @commands.command(name='reload')
    @commands.has_role('Orga')
    async def reload(ctx, module) -> None:
        {
            'all': lambda: load_games() or load_members(),
            'members': lambda: load_members(),
            'games': lambda: load_games(),
        }[module]()

    @commands.command(name='games')
    @commands.has_role('Orga')
    async def games(ctx) -> None:
        from operator import itemgetter
        from itertools import chain
        await ctx.channel.send('\n'.join(map(itemgetter('name'), Data().games)))

    @commands.command(name='poll-save')
    @commands.has_role('Orga')
    async def poll_save(ctx) -> None:
        try:
            data.storage.save()
            await ctx.channel.send('Votes Saved!')
            system_logger.info(f'Votes saved by "{ctx.author.name}!"')
        except Exception as exc:
            system_logger.error(f'Vote saving attempt by "{ctx.author.name}" failed! [{exc.__class__.__name__}: {exc}]')
            await ctx.channel.send(f'Vote saving attempt failed! [{exc.__class__.__name__}: {exc}]')

    @commands.command(name='poll-activate')
    @commands.has_role('Orga')
    async def poll_activate(ctx) -> None:
        Data().vote_active = True
        system_logger.info(f'Poll activated by {ctx.author.name}!')
        await ctx.channel.send('Poll activated!')

    @commands.command(name='poll-deactivate')
    @commands.has_role('Orga')
    async def poll_deactivate(ctx) -> None:
        Data().vote_active = False
        data.storage.save()
        system_logger.info(f'Poll deactivated by {ctx.author.name}!')
        await ctx.channel.send('Poll deactivated!')

    @commands.command(name='poll-status')
    @commands.has_role('Orga')
    async def poll_status(ctx) -> None:
        system_logger.info(f'Poll status requested by {ctx.author.name}!')
        await ctx.channel.send(f'Poll is **{"active" if Data().vote_active else "inactive"}**!\n**{len(data.storage)}** people have at least partially voted!')

    @commands.command(name='poll-result')
    @commands.has_role('Orga')
    async def poll_result(ctx, *names) -> None:
        try:
            cats = list(Data().voting_channels.keys())
            if 'cat' in names:
                await ctx.send(', '.join(cats))
                return

            for name in names:
                if name == 'best': continue
                key = list()
                if name in cats or (key := [key for key in cats if name in key]):
                    if key: name = key[0]
                    cats.remove(name)
                    with data.storage.result(name) as file:
                        await ctx.send(file=File(file, filename=f'{name}.png'))

            # if 'art' in names or not names:
            #     with data.storage.result('best-art') as file:
            #         await ctx.send(file=File(file, filename=f'best-art.png'))
            # if 'tech' in names or not names:
            #     with data.storage.result('best-technology') as file:
            #         await ctx.send(file=File(file, filename=f'best-technology.png'))
            # if 'design' in names or not names:
            #     with data.storage.result('best-design') as file:
            #         await ctx.send(file=File(file, filename=f'best-design.png'))
            # if 'story' in names or not names:
            #     with data.storage.result('best-story') as file:
            #         await ctx.send(file=File(file, filename=f'best-story.png'))
            # if 'sound' in names or not names:
            #     with data.storage.result('best-sound') as file:
            #         await ctx.send(file=File(file, filename=f'best-sound.png'))
            # if 'poster' in names or not names:
            #     with data.storage.result('best-poster') as file:
            #         await ctx.send(file=File(file, filename=f'best-poster.png'))
            # if 'humor' in names or not names:
            #     with data.storage.result('best-humor') as file:
            #         await ctx.send(file=File(file, filename=f'best-humor.png'))
            # if 'inclusive' in names or not names:
            #     with data.storage.result('most-inclusive') as file:
            #         await ctx.send(file=File(file, filename=f'most-inclusive.png'))
            # if 'booth' in names or not names:
            #     with data.storage.result('best-booth') as file:
            #         await ctx.send(file=File(file, filename=f'best-booth.png'))
            # if 'experimental' in names or not names:
            #     with data.storage.result('experimental-projects') as file:
            #         await ctx.send(file=File(file, filename=f'experimental-projects.png'))
        except Exception as exc:
            await ctx.channel.send(f'Failed to get results! {exc.__class__.__name__}: {exc}')

    async def change_status_after_time(self) -> None:
        games = list(map(lambda x: x['name'], data.games))
        games.pop(0)
        while True:
            await sleep(randint(30, 90))
            await self.change_presence(activity=Activity(type=ActivityType.playing, name=choice(games or ['your cool games'])))

    async def save_poll(self) -> None:
        await sleep(300)
        if data.vote_active:
            data.storage.save()


if __name__ == '__main__': pass
