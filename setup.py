
with open("README.rst") as f:
  readme = f.read()

config = {
    'name': 'mesos_cli',
    'version': '0.0.0',
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

            'mesos-cat = mesos_cli.cat:main',
            'mesos-find = mesos_cli.find:main',
            'mesos-head = mesos_cli.head:main',
            'mesos-help = mesos_cli.help:main',
            'mesos-ls = mesos_cli.ls:main',
            'mesos-resolve = mesos_cli.resolve:main',
            'mesos-ssh = mesos_cli.ssh:main',
            'mesos-tail = mesos_cli.tail:main'
        ]
    },
    'install_requires': [
        "blessings",
        "kazoo",
        "protobuf",
        "requests"
    ]
}

from setuptools import setup

setup(**config)
