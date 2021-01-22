#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-12-24"
__version__ = "0.0.0"

__all__ = ()

from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from discord_bot.commands import DDBot

load_dotenv(Path('../data/.env'))


if __name__ == '__main__':
    DDBot().run(getenv('TOKEN'))
