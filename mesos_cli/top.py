
import curses
import os
import sys
import time

from . import cli
from .master import current as master
from . import slave
from . import task

REFRESH = 1

parser = cli.parser(
    description="display and update sorted information about tasks"
)

def top(stdscr, cfg, args):
    while 1:

        stdscr.addstr(0, 0, time.strftime('%H:%M:%S'))
        stdscr.refresh()

        time.sleep(REFRESH)

        stdscr.erase()

def main():
    curses.wrapper(top, *cli.init(parser))
