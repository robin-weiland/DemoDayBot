#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.3"

__all__ = ('VOTES_PATH', 'Data', 'load_games', 'load_members',)

from pathlib import Path
from json import loads
from itertools import chain
from operator import itemgetter
from demodaybot.storage import Storage

from typing import Any, List, Dict

VOTES_PATH = Path('./data/votes.json')
GAMES_PATH = Path('./data/games.json')


class DataNotSpecifiedException(Exception): pass


class DataSingleton:
    _shared_state: Dict[str, Any] = dict()

    def __init__(self):
        self.__dict__ = self._shared_state


class Data(DataSingleton):
    _voting_channels: Dict[str, int] = None
    _games: List[Dict[str, Any]] = None
    _members: List[int] = None
    _vote_active: bool = False
    _storage: Storage = None

    def __init__(self):
        super(Data, self).__init__()

    @property
    def voting_channels(self) -> Dict[str, int]:
        if self._voting_channels is None: raise DataNotSpecifiedException
        return self._voting_channels

    @voting_channels.setter
    def voting_channels(self, value: Dict[str, int]) -> None:
        self._voting_channels = value
        self.storage = Storage(VOTES_PATH, list(self._voting_channels.keys()), list(map(lambda x: x['name'], self.games)))

    @property
    def games(self) -> List[Dict[str, Any]]:
        if self._games is None: raise DataNotSpecifiedException
        return self._games

    @games.setter
    def games(self, value: List[Dict[str, Any]]) -> None:
        self._games = value

    @property
    def members(self) -> List[int]:
        if self._members is None: raise DataNotSpecifiedException
        return self._members

    @members.setter
    def members(self, value: List[int]) -> None:
        self._members = value

    @property
    def vote_active(self) -> bool:
        return self._vote_active

    @vote_active.setter
    def vote_active(self, value: bool) -> None:
        self._vote_active = value

    @property
    def storage(self) -> Storage:
        return self._storage

    @storage.setter
    def storage(self, value: Storage) -> None:
        self._storage = value


def load_games() -> None:
    Data().games = loads(GAMES_PATH.read_text())


def load_members() -> None:
    Data().members = list(chain.from_iterable(map(lambda x: x['members'], Data().games)))


load_games()
load_members()

if __name__ == '__main__': pass
