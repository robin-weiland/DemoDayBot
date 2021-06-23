#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-12-24"
__version__ = "0.0.3"

__all__ = ('run',)

from pathlib import Path
from os import chdir

chdir(str(Path(__file__).parent))


from os import getenv
from demodaybot.bot import DDBot
from demodaybot.log import *
from demodaybot.messages import CONSOLE
from argparse import ArgumentParser
from sys import exit, executable

try: from dotenv import load_dotenv
except ImportError:
    print('Module: python-dotenv not found! Installing it now!\n')
    from subprocess import check_call
    check_call([executable, '-m', 'pip', 'install', 'python-dotenv'])
    from dotenv import load_dotenv


TOKEN_NAME: str = 'DDB_TOKEN'


def error(message: str, code: int) -> None:
    print(message + '\nABORTING!\n')
    exit(code)


def run() -> None:
    parser = ArgumentParser(prog='DemoDayBot', description='TUM DemoDay Discord Bot',
                            usage='demodaybot [-p .] [-t .]',
                            epilog=f'demodaybot v{__version__} [{__date__}] by {__author__}')
    parser.add_argument(
        '-p',
        '--path',
        type=Path,
        default=None,
        help='Path to the .env file with the discord application key!'
    )

    parser.add_argument(
        '-t',
        '--token',
        type=str,
        default=None,
        help='Discord Application Key to pass directly!'
    )

    print(CONSOLE)

    args = parser.parse_args()

    if args.token is not None:
        print('Using the passed API key!\n')
        DDBot().run(args.token)
    elif args.path is not None:
        if not args.path.exists():
            error('Provided .env file could not be found!', -1)
        else:
            load_dotenv(args.path)
            if not getenv(TOKEN_NAME):
                error('Token not found although it was loaded from the provided file!', -2)
            else:
                print('Using the API key from the provided .env file!\n')
                DDBot().run(getenv(TOKEN_NAME))
    else:
        print('No Application Token provided!\nABORTING!\n\n')
        parser.print_help()
        exit(-3)


if __name__ == '__main__':
    pass
