#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-22"
__version__ = "0.0.0"

__all__ = ()

from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG

system_logger = getLogger('System')
system_logger.setLevel(DEBUG)

system_formatter = Formatter('[%(levelname)s] [%(asctime)s] [%(message)s]', '%Y-%m-%d %H:%M:%S')
file_formatter = Formatter('[%(asctime)s] [%(message)s]', '%Y-%m-%d %H:%M:%S')

sytem_stream_handler = StreamHandler()
sytem_stream_handler.setFormatter(system_formatter)
file_handler = FileHandler('./data/logs/system.log')
file_handler.setFormatter(system_formatter)
system_logger.addHandler(sytem_stream_handler)
system_logger.addHandler(file_handler)


chat_logger = getLogger('Chat')
chat_logger.setLevel(DEBUG)
chat_file_handler = FileHandler('./data/logs/chat.log')
chat_file_handler.setFormatter(file_formatter)
chat_logger.addHandler(chat_file_handler)


vote_logger = getLogger('Vote')
vote_logger.setLevel(DEBUG)
vote_file_handler = FileHandler('./data/logs/vote.log')
vote_file_handler.setFormatter(file_formatter)
vote_logger.addHandler(vote_file_handler)


vote_error_logger = getLogger('VoteError')
vote_error_logger.setLevel(DEBUG)
vote_file_handler = FileHandler('./data/logs/vote-error.log')
vote_file_handler.setFormatter(file_formatter)
vote_error_logger.addHandler(vote_file_handler)


if __name__ == '__main__': pass
