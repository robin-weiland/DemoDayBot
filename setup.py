#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-25"
__version__ = "0.0.0"

__all__ = ()

from pathlib import Path
from setuptools import setup
from sys import argv
from shutil import rmtree
from os import remove


BUILD_DIRS = (
    'demodaybot.egg-info',
    'build',
    'dist'
)


if __name__ == '__main__':
    print('cleaning up:')
    print('deleting binaries:')
    for d in BUILD_DIRS:
        path = Path(d)
        if path.exists() and path.is_dir():
            print(f'Deleting {path}...')
            rmtree(d)
    if '--clean-logs' in argv:
        print('Deleting logs...')
        rmtree(Path('demodaybot/data') / 'logs')

    if '--clean-votes' in argv:
        print('Deleting votes...')
        remove(Path('demodaybot/data') / 'votes.json')

    if '--clean-data' in argv:
        print('Deleting data...')
        remove(Path('demodaybot/data') / 'members.json')
        remove(Path('demodaybot/data') / 'voting_channels.json')

    readme_path = Path('README.md')
    if readme_path.exists():
        with readme_path.open('r') as file:
            long_description = file.read()
    else:
        long_description = ''

    requirements_path = Path('requirements.txt')
    if requirements_path.exists():
        with requirements_path.open('r') as file:
            requirements = [line for line in file.readlines() if not line.startswith('#') and line]
    else:
        requirements = []

    setup(
        name='DemoDayBot',
        version='0.0.1',
        packages=['discord_bot'],
        url='https://github.com/robin-weiland/DemoDayBot',
        license='GPL',
        author="Robin 'r0w' Weiland",
        author_email='robinweiland@gmx.de',
        description='Discord bot for the TUM DemoDay 2021',
        long_description=long_description,
        long_description_content_type='text/markdown',
        keywords=['discord', 'bot'],
        python_requires='>=3.6',
        # https://pypi.org/classifiers/
        classifiers=[
            'Development Status :: 4 - Beta',

            'Environment :: Console',

            # Indtended Audience

            'License :: OSI Approved :: GPL License',

            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',

            # Topic

            'Typing :: Typed'
        ],
        entry_points={
            'console_scripts': [
                'demodaybot = demodaybot:run'
            ]
        }
    )
