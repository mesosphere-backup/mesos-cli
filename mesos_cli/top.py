
import os
import sys

from . import cli
from . import master
from . import slave
from . import task

parser = cli.parser(
    description="display and update sorted information about tasks"
)

def main():
    cfg, args, m = cli.init(parser)
