==========================
Write a new command
==========================

1. Go to `entry_points` in `setup.py` and add your command::

  'mesos-my-command = mesos.cli.cmds.my_command:main'

2. Create the command file::

  touch mesos/cli/cmds/my_command.py

3. Add the basic structure::

  from __future__ import absolute_import, print_function

  from .. import cli

  parser = cli.parser(
      description="what my command does"
  )

  @cli.init(parser)
  def main(args):
      pass

4. Implement your task!

  - There are helpers for most common command line arguments, see `parser.py` for a list.
  - Looking for master state? Take a look at `mesos.cli.cmds.state` for the pattern to use.
  - Doing something with files? You can probably use `mesos.cli.cluster`. Take a peek at `mesos.cli.cmds.cat` for an example of how to use it.
  - Interested in performance data? Look at `mesos.cli.cmds.ps`.

5. Create a test::

  touch tests/integration/test_my_command.py

6. Setup the skeleton::

  from __future__ import absolute_import, print_function

  import mock

  import mesos.cli.cmds.my_command

  from .. import utils


  class TestCat(utils.MockState):
    pass

7. Write the test!

  - Master state and slave state are mocked out. You shouldn't need to do anything special.
  - When calling each test, you will need to patch the args. Take a look at `tests/integration/test_cat.py` for an example.

8. Verify style::

  make test

9. Test against all python versions::

  tox

