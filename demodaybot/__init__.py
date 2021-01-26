#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-12-24"
__version__ = "0.0.0"

__all__ = ('run',)

from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from demodaybot.commands import DDBot
from demodaybot.log import *


def run() -> None:
    load_dotenv(Path('./data/.env'))
    DDBot().run(getenv('TOKEN'))


if __name__ == '__main__':
    pass
