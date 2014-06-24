
import mesos_cli

with open("README.rst") as f:
  readme = f.read()

requires = [
    "argcomplete>=0.8.0",
    "blessings>=1.5.1",
    "gevent>=1.0.1",
    "kazoo>=2.0",
    "prettytable>=0.7.2",
    "protobuf>=2.5.0",
    "requests>=2.2.1"
]

config = {
    'name': 'mesos_cli',
    'version': mesos_cli.__version__,
    'description': 'Mesos CLI Tools',
    'long_description': readme,
    'author': 'Thomas Rampelberg',
    'author_email': 'thomas@mesosphere.io',
    'maintainer': 'Mesosphere',
    'maintainer_email': 'support@mesosphere.io',
    'url': 'https://github.com/mesosphere/mesos-cli',
    'packages': [
        'mesos_cli'
    ],
    'entry_points': {
        'console_scripts': [
            'mesos = mesos_cli:main',

            # helpers
            'mesos-completion = mesos_cli.completion:main',

            # coreutils
            'mesos-cat = mesos_cli.cat:main',
            'mesos-find = mesos_cli.find:main',
            'mesos-head = mesos_cli.head:main',
            'mesos-help = mesos_cli.help:main',
            'mesos-ls = mesos_cli.ls:main',
            'mesos-ps = mesos_cli.ps:main',
            'mesos-resolve = mesos_cli.resolve:main',
            'mesos-scp = mesos_cli.scp:main',
            'mesos-ssh = mesos_cli.ssh:main',
            'mesos-tail = mesos_cli.tail:main'
        ]
    },
    'install_requires': requires,
    'scripts': [
        'bin/mesos-zsh-completion.sh'
    ]
}

from setuptools import setup

setup(**config)
