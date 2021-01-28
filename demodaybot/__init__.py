#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-12-24"
__version__ = "0.0.0"

__all__ = ('run',)

from os import getenv
from dotenv import load_dotenv
from demodaybot.commands import DDBot
from demodaybot.log import *
from pathlib import Path


def run() -> None:
    env = Path('./data/.env')
    if env.exists(): load_dotenv(env)
    DDBot().run(getenv('DDB_TOKEN'))


if __name__ == '__main__':
    pass
