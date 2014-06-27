
import mesoscli

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
    'name': 'mesoscli',
    'version': mesoscli.__version__,
    'description': 'Mesos CLI Tools',
    'long_description': readme,
    'author': 'Thomas Rampelberg',
    'author_email': 'thomas@mesosphere.io',
    'maintainer': 'Mesosphere',
    'maintainer_email': 'support@mesosphere.io',
    'url': 'https://github.com/mesosphere/mesos-cli',
    'packages': [
        'mesoscli'
    ],
    'entry_points': {
        'console_scripts': [
            'mesos = mesoscli.main:main',

            # helpers
            'mesos-completion = mesoscli.completion:main',
            'mesos-config = mesoscli.config:main',
            'mesos-resolve = mesoscli.resolve:main',
            'mesos-state = mesoscli.state:main',

            # coreutils
            'mesos-cat = mesoscli.cat:main',
            'mesos-find = mesoscli.find:main',
            'mesos-head = mesoscli.head:main',
            'mesos-help = mesoscli.help:main',
            'mesos-ls = mesoscli.ls:main',
            'mesos-ps = mesoscli.ps:main',
            'mesos-scp = mesoscli.scp:main',
            'mesos-ssh = mesoscli.ssh:main',
            'mesos-tail = mesoscli.tail:main'
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
