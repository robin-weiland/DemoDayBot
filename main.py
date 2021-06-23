#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-22"
__version__ = "0.0.0"

__all__ = ()

from os import chdir
chdir('demodaybot')  # ugly workaround

from demodaybot import run
from logging import getLogger

logger = getLogger('System')


if __name__ == '__main__':
    while True:
        logger.info('Started Bot!')
        run()
