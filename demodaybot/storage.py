#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-21"
__version__ = "0.0.3"

__all__ = ('Storage',)

from collections import defaultdict
from json import loads, dumps, JSONEncoder
from pathlib import Path
from functools import partial
from numpy import array, stack, ndarray, int8
import pandas as pd
from logging import getLogger
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from io import BytesIO

from typing import Union, Optional, List, Dict

logger = getLogger('System')


class NoDataException(Exception): pass


class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def decoder(dct):
    return dict(zip(map(int, dct.keys()), map(partial(array, dtype=int8), dct.values())))


class Storage(defaultdict, Dict[int, ndarray]):
    path: Path
    games: List[str]
    categories: List[str]

    __slots__ = ('path', 'games', 'categories',)

    def __init__(self, path: Union[Path, str], categories: List[str], games: List[str]):
        self.path = Path(path)
        self.games = games
        self.categories = categories
        super(Storage, self).__init__(partial(ndarray, len(categories), dtype=int8))
        self.load()

    def save(self) -> None:
        self.path.write_text(dumps(dict(zip(self.keys(), self.values())), cls=NumpyEncoder, indent=2))

    def load(self) -> None:
        if not self.path.exists(): self.path.write_text('{}')
        super(Storage, self).update(loads(self.path.read_text(), object_hook=decoder))

    def clear(self) -> None:
        super(Storage, self).clear()
        self.save()

    @property
    def matrix(self):
        return stack(list(self.values()), axis=0)

    def result(self, cat) -> Optional[BytesIO]:
        if not len(self):
            logger.warning('Cannot get results from empty data!')
            raise NoDataException
        if isinstance(cat, str): cat = self.categories.index(cat)
        name = self.categories[cat]

        data = pd.DataFrame(self.matrix[:, cat])
        rdata = data.value_counts().sort_values(ascending=False)[:3]
        rdata.index = rdata.index.map(lambda x: self.games[x[0]])

        plt.style.use('dark_background')
        fig = plt.figure()
        ax = plt.figure().gca()
        ax.set_title(name)
        ax.patch.set_facecolor('#36393f')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        rdata.plot.bar()
        plt.tight_layout()
        plt.grid(axis='y')

        buffer = BytesIO()
        plt.savefig(buffer, format='png', facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
        plt.close(fig)
        buffer.seek(0)
        return buffer


def fill_random():
    from random import choice
    from string import ascii_letters, digits
    symbols = ascii_letters + digits
    data = list()
    data.append({'name': 'Enthaltung', 'short': '', 'members': []})
    for _ in range(25):
        data.append({'name': ''.join(choice(symbols) for _ in range(10)), 'short': '', 'members': []})
    Path('data/games_test.json').write_text(dumps(data, indent=2))


if __name__ == '__main__': pass
