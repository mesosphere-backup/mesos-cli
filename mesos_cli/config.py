import os
import json
import errno

DEFAULT_CONFIG = os.environ.get(
    'MESOS_CLI_CONFIG_DIR',
    os.path.expanduser('~/.mesos_cli.json')
)

class Config(dict):

    DEFAULTS = {
        "master": "localhost:5050",
        "log_level": "warning",
        "log_file": None
    }

    def __init__(self):
        self.update(self.DEFAULTS)
        self.load()

    def _get_path(self):
        return DEFAULT_CONFIG

    def __getattr__(self, item):
        return self[item]

    def load(self):
        try:
            with open(self._get_path(), 'rt') as f:
                try:
                    data = json.load(f)
                except ValueError as e:
                    raise ValueError(
                        'Invalid %s JSON: %s [%s]' %
                        (type(self).__name__, e.message, self.path)
                    )
                self.update(data)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
