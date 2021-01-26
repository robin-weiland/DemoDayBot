#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-25"
__version__ = "0.0.0"

__all__ = ()

from pathlib import Path
from setuptools import setup


if __name__ == '__main__':
    readme_path = Path('README.md')
    if readme_path.exists():
        with readme_path.open('r') as file:
            long_description = file.read()
    else: long_description = ''

    requirements_path = Path('requirements.txt')
    if requirements_path.exists():
        with requirements_path.open('r') as file:
            requirements = [line for line in file.readlines() if not line.startswith('#') and line]
    else: requirements = []


    setup(
        name='DemoDayBot',
        version='0.0.1',
        packages=['discord_bot'],
        url='https://github.com/robin-weiland/DemoDayBot',
        license='GPL',
        author='Robin 'r0w' Weiland',
        author_email='robinweiland@gmx.de',
        description='Discord bot for the TUM DemoDay 2021',
        long_description=long_description,
        long_description_content_type = 'text/markdown',
        keywords=[],  # TODO
        python_requires='',  # TODO
        classifiers=[]  # TODO
    )
