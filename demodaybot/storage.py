#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.0"

__all__ = ('Storage',)

from collections import defaultdict, namedtuple
from json import loads, dumps, JSONEncoder
from pathlib import Path
from functools import partial
from numpy import array, ndarray, int8

from typing import Union, Dict

Votes = namedtuple('Votes', 'game art design stuff good bad')  # use later for calculating results
NUMBER_OF_GAMES: int = 8  # TODO get number of games


class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def decoder(dct):
    return dict(zip(dct.keys(), map(partial(array, dtype=int8), dct.values())))


def default_factory(): return [0] * NUMBER_OF_GAMES

# np.stack(tuple(d.values()), axis=0)


class Storage(defaultdict, Dict[str, ndarray]):
    path: Path

    __slots__ = ('path',)

    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)
        super(Storage, self).__init__(partial(ndarray, NUMBER_OF_GAMES, dtype=int8))
        self.load()

    def save(self) -> None:
        self.path.write_text(dumps(dict(zip(self.keys(), self.values())), cls=NumpyEncoder, indent=2))

    def load(self) -> None:
        if not self.path.exists(): self.path.touch()
        super(Storage, self).update(loads(self.path.read_text(), object_hook=decoder))


if __name__ == '__main__':
    storage = Storage('data/votes.json')
    print(storage["0"][4])
