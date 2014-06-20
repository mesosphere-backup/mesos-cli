
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
            # Need a better way to handle these already implemented by mesos
            'mesos-c = mesos_cli.cat:main',
            'mesos-t = mesos_cli.tail:main',

            'mesos-find = mesos_cli.find:main',
            'mesos-head = mesos_cli.head:main',
            'mesos-ls = mesos_cli.ls:main',
            'mesos-ssh = mesos_cli.ssh:main',
            'mesos-top = mesos_cli.top:main'
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
