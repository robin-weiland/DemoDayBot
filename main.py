#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-22"
__version__ = "0.0.0"

__all__ = ()

from os import chdir
chdir('demodaybot')  # ugly workaround

from demodaybot import run


if __name__ == '__main__':
    run()
