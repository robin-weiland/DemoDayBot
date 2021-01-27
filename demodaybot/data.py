#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.0"

__all__ = ('VOTES_PATH', 'members', 'voting_channels', 'games', 'orga',)

from pathlib import Path
from json import loads
from itertools import chain, takewhile

MEMBERS_PATH = Path('./data/members.json')
VOTES_PATH = Path('./data/votes_test.json')
VOTING_CHANNELS_PATH = Path('./data/voting_channels.json')
GAMES_PATH = Path('./data/games_test.json')
ORGA_PATH = Path('./data/orga')

# members_ = loads(MEMBERS_PATH.read_text())
voting_channels = loads(VOTING_CHANNELS_PATH.read_text())
games = loads(GAMES_PATH.read_text())
members = list(chain.from_iterable(map(lambda x: x['members'], games)))
orga = list(int(m) for m in [''.join(takewhile(lambda x: x != '#', member)) for member in ORGA_PATH.read_text().splitlines(keepends=False)] if m)


if __name__ == '__main__': pass
