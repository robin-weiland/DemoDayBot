#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.0"

__all__ = ('DDBot',)

from discord.utils import get
from discord_bot.storage import Storage
from discord_bot.data import voting_channels, VOTES_PATH
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Activity, ActivityType

storage = Storage(VOTES_PATH)


class DDBot(Bot):
    def __init__(self):
        super(DDBot, self).__init__(command_prefix='!')
        self.add_command(self.save)
        self.voting_channels = list()

    async def on_ready(self):
        await self.change_presence(activity=Activity(type=ActivityType.playing, name="your cool games"))
        guild = [guild for guild in self.guilds if guild.name == 'DemoDay 2021'][0]
        self.voting_channels = [category for category in guild.categories if category.name == 'VOTING'][0].channels
        print('Connected!')

    async def on_member_join(self, member):
        await self.add_roles(member, get(member.server.roles, id='791315081992077342'))  # 'Besucher' id

    async def on_message(self, message):
        await self.process_commands(message)
        if message.author == self.user: return
        if message.channel.id not in voting_channels.values(): return
        if message.channel in self.voting_channels:
            try:
                number = int(message.content)
                storage[message.author.id][tuple(voting_channels.values()).index(message.channel.id) - 1] = number
                await message.author.send(f'Your vote _{number}_ for _{message.channel.name}_ has been counted!')
                print(storage)
            except ValueError:
                await message.author.send(f'There was an error with your vote for the _{message.channel.name}_ category!')
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
            await ctx.channel.send('Votes Saved')
        except Exception as exc:
            print(exc)
            return


if __name__ == '__main__': pass
