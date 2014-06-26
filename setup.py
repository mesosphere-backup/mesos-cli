
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
            'mesos = mesos_cli.main:main',

            # helpers
            'mesos-completion = mesos_cli.completion:main',
            'mesos-config = mesos_cli.config:main',
            'mesos-resolve = mesos_cli.resolve:main',
            'mesos-state = mesos_cli.state:main',

            # coreutils
            'mesos-cat = mesos_cli.cat:main',
            'mesos-find = mesos_cli.find:main',
            'mesos-head = mesos_cli.head:main',
            'mesos-help = mesos_cli.help:main',
            'mesos-ls = mesos_cli.ls:main',
            'mesos-ps = mesos_cli.ps:main',
            'mesos-scp = mesos_cli.scp:main',
            'mesos-ssh = mesos_cli.ssh:main',
            'mesos-tail = mesos_cli.tail:main'
        ]
    },
    'setup_requires': [
        "nose>=1.3.3",
        "tox>=1.7.1"
    ],
    'install_requires': requires,
    'tests_require': [
        'coverage>=3.7.1',
        'mock>=1.0.1',
        'zake>=0.0.20'
    ],
    'test_suite': 'nose.collector',
    'scripts': [
        'bin/mesos-zsh-completion.sh'
    ]
}

from setuptools import setup

setup(**config)
