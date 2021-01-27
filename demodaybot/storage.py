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
from numpy import array, stack, ndarray, int8
# from pandas import Dataframe
import pandas as pd
from collections import Counter
from logging import getLogger
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from io import BytesIO

from typing import Union, Dict

Votes = namedtuple('Votes', 'game art design stuff good bad')  # use later for calculating results
NUMBER_OF_GAMES: int = 9  # TODO get number of games

logger = getLogger('System')

games = list(map(lambda x: x['name'], loads(Path('data/games_test.json').read_text())))
categories = list(loads(Path('data/voting_channels.json').read_text()).keys())[1:]
print(categories)


class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def decoder(dct):
    return dict(zip(map(int, dct.keys()), map(partial(array, dtype=int8), dct.values())))


def default_factory(): return [0] * NUMBER_OF_GAMES

# np.stack(tuple(d.values()), axis=0)


class Storage(defaultdict, Dict[int, ndarray]):
    path: Path

    __slots__ = ('path',)

    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)
        super(Storage, self).__init__(partial(ndarray, NUMBER_OF_GAMES, dtype=int8))
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

    def result(self, cat) -> BytesIO:
        if not len(self):
            logger.warning('Cannot get results from empty data!')
            return None
        if isinstance(cat, str): cat = categories.index(cat)
        name = categories[cat]

        data = pd.DataFrame(self.matrix[:, cat])
        rdata = data.value_counts().sort_values(ascending=False)
        rdata.index = rdata.index.map(lambda x: games[x[0]])
        fig = plt.figure()
        fig.patch.set_facecolor('#36393f')
        plt.title(name)
        # plt.rcParams['axes.facecolor'] = '#36393f'
        ax = plt.figure().gca()
        ax.set_title(name)
        ax.patch.set_facecolor('#36393f')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        rdata.plot.bar()
        plt.tight_layout()
        plt.grid(axis='y')
        plt.close(fig)

        # plt.show(facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png', facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
        buffer.seek(0)
        return buffer


if __name__ == '__main__':
    from random import randint, choice
    storage = Storage('data/votes_test.json')
    # # count = 0
    # # for vote in storage.values():
    # #     if vote[0] == 24: count += 1
    # # print(count)
    storage.result('best-art')
    # from string import ascii_letters, digits
    # symbols = ascii_letters + digits
    # data = list()
    # data.append({'name': 'Enthaltung', 'short': '', 'members': []})
    # for _ in range(25):
    #     data.append({'name': ''.join(choice(symbols) for a in range(10)), 'short': '', 'members': []})
    # Path('data/games_test.json').write_text(dumps(data, indent=2))

    # storage.result()
    # print(storage["0"][4])

# 19     5
# 20     6
# 14     6
# 9      8
# 25     9
# 16     9
# 18     9
# 13     9
# 22     9
# 17    10
# 6     10
# 21    10
# 10    10
# 0     10
# 1     10
# 11    11
# 12    11
# 23    12
# 4     12
# 24    15
# 15    16
# 5     17
# 3     18
# 8     19
# 7     19
# 2     20
