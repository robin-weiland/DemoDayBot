#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2021-01-31"
__version__ = "0.0.3"

__all__ = ('WELCOME', 'CONSOLE', 'MOBILE',)

console_spaces = " " * (23 - len(__version__) - len(__date__) + 16)  # black magic

CONSOLE: str = rf"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   ______     ═╦═║ ║╔═╦═╗    ______           ______       _       ┃
┃   |  _  \     ║ ╚═╝║ ║ ║    |  _  \          | ___ \     | |      ┃
┃   | | | |___ _ __ ___   ___ | | | |__ _ _   _| |_/ / ___ | |_     ┃
┃   | | | / _ \ '_ ` _ \ / _ \| | | / _` | | | | ___ \/ _ \| __|    ┃
┃   | |/ /  __/ | | | | | (_) | |/ / (_| | |_| | |_/ / (_) | |_     ┃
┃   |___/ \___|_| |_| |_|\___/|___/ \__,_|\__, \____/ \___/ \__|    ┃
┃   ══════════════════════════════════════ __/ | ═══════════════    ┃
┃                                         |___/                     ┃ 
┃    v{__version__} [{__date__}]{console_spaces}         GPL-3.0    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

WELCOME: str = 'Hallo **{member}**. Willkommen auf dem DemoDay 2021!\n' \
               'Lies Dir bitte zuerst <#791303033371099179> durch.\n' \
               'Ich war mal so frei und habe Dir die Besucher-Rolle gegeben. Wenn Du hier bist, um Dein Spiel\n' \
               'zu zeigen, kannst Du in <#805447044910284811> die Rolle _Aussteller_ auswählen.\n' \
               'In der <#799932766933745664> siehst Du dann, was heute angeboten wird und in <#791303033371099180>\n' \
               'werden wir Dich während des Events auf dem Laufen halten. Ach <#799940173264846859> gibt es auch noch!'

MOBILE: str = 'Oh... Es sieht so aus als würdest Du gerade an einem mobilen Gerät sein.\n' \
              'Das ist eigentlich total in Ordnung, aber wenn Du nachher einen Hubs Raum\n' \
              'besuchen willst, kann es sein, dass Du an eimen Computer eine bessere Erfahrung\n' \
              'haben wirst!'

if __name__ == '__main__': pass
