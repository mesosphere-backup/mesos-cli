
import blessings
import collections
import prettytable
import util

from . import cli
from .master import current as master

parser = cli.parser(
    description="process status"
)

parser.add_argument(
    "-i", "--inactive", action="store_true",
    help="show inactive tasks as well"
)

def get_memory(x):
    if x.mem_limit == 0:
        return "0"
    else:
        return "{:.2f}".format((x.rss / (x.mem_limit * 1.0)) * 100)

def main():
    term = blessings.Terminal()
    max_pid = term.width - 70

    table_generator = collections.OrderedDict([
        # user_time + system_time
        ("time", lambda x: x.cpu_time),
        # mem_rss
        ("rss", lambda x: util.humanize_bytes(x.rss)),
        # cpus_limit
        ("cpu", lambda x: x.cpu_limit),
        # mem_rss / mem_limit
        ("%mem", get_memory),
        # executor.name
        ("command", lambda x: x.command),
        ("user", lambda x: x.user),
        # slave_pid:task_id
        ("pid", lambda x: str(x).split('@')[-1][:max_pid]),
    ])

    cfg, args = cli.init(parser)

    tb = prettytable.PrettyTable(
        [x.upper() for x in table_generator.keys()],
        border=False,
        max_table_width=term.width,
        hrules=prettytable.NONE,
        vrules=prettytable.NONE,
        left_padding_width=0,
        right_padding_width=1
    )

    for t in master.tasks(active_only=(not args.inactive)):
        tb.add_row([fn(t) for fn in table_generator.values()])
    print tb
