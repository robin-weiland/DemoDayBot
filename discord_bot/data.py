#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.0"

__all__ = ('VOTES_PATH', 'members', 'voting_channels',)

from pathlib import Path
from json import loads

MEMBERS_PATH = Path('./data/members.json')
VOTES_PATH = Path('./data/votes.json')
VOTING_CHANNELS_PATH = Path('./data/voting_channels.json')


members = loads(MEMBERS_PATH.read_text())
voting_channels = loads(VOTING_CHANNELS_PATH.read_text())


if __name__ == '__main__': pass
