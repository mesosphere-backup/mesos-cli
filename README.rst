=========
mesos-cli
=========

**This project has been deprecated and is no longer being actively maintained. Please use the** `DCOS CLI`_.

CLI tools to work with mesos.

-----------------------------
What problem does this solve?
-----------------------------

I am comfortable debugging programs from the command line. I have a set of tools that I use from coreutils that end up being used every day. A day doesn't go by when I've not used grep, find, or cat.

While mesos allows you to treat all the nodes in your data center as anonymous resources, debugging still needs to be done on specific hosts. Currently, it requires multiple tools and context switches to gather the pieces that you need to look at what a specific task is doing. Most of these existing tools don't work well with the command line and I'm unable to use the workflow that I've become comfortable with.

--------------------------
How is the problem solved?
--------------------------

To solve the problem, some of the coreutil commands have been re-implemented to work across the entire data center instead of a single host.

- commands and options have been copied as closely as it makes sense. They should have the same options that you're used to.
- pipe works the way you'd expect it to. You should be able to replace most host specific debug scripts easily.
- mesos itself isn't required locally. Developers want to debug their tasks without having a local copy of mesos installed.
- everything is task centric. There's no need to worry about specifying a framework if you don't want to, just put in the task id.
- lazy matching. Task IDs are long and normally require cut/paste to get exact matches. Instead, all `task` parameters are partial matches, no need to type that long thing in.
- auto-complete. Most parameters tab-complete (see the section on auto-completion to configure), just type a couple characters in and get what you're looking for.
- extensibility. Write your own subcommands. Most of the required information can be accessed via. existing subcommands (leading master resolution via. mesos-resolve), so you only need to implement what you want and not re-invent the wheel.

-------
Install
-------

Note that if you've already installed `mesos` locally, you can either install this to a location other than `/usr/local/bin` via. pip options or remove `/usr/local/bin/mesos`. There should be no downsides to just removing it.

From PyPI:

.. code-block:: bash

    pip install mesos.cli

From this repo:

.. code-block:: bash

    python setup.py install

------------------
Create Environment
------------------

.. code-block:: bash

    make env
    source env/bin/activate

-----
Build
-----

.. code-block:: bash

    python setup.py build

----
Test
----

.. code-block:: bash

    make test

-------------------
Command Completion
-------------------

Task IDs? File names? Complete all the things! Configure command completion and you'll be able to tab complete most everything.

+++++
BASH
+++++

Add the following to your startup scripts:

.. code-block:: bash

    complete -C mesos-completion mesos

++++
ZSH
++++

Add the following to your `.zshrc`:

.. code-block:: bash

    source mesos-zsh-completion.sh

Note that `bashcompinit` is being used. If you're running an older version of ZSH, it won't work. Take a look at `bin/mesos-zsh-completion.sh` for information.

-------------
Configuration
-------------

Place a configuration file at any of the following:

.. code-block:: bash

    ./.mesos.json
    ~/.mesos.json
    /etc/.mesos.json
    /usr/etc/.mesos.json
    /usr/local/etc/.mesos.json

You can override the location of this config via. `MESOS_CLI_CONFIG`.

If you're using a non-local master, you'll need to configure where the master should be found like so:

.. code-block:: bash

    mesos config master zk://localhost:2181/mesos

Alternatively, you can create the config file yourself.

.. code-block:: json

    {
        "profile": "default",
        "default": {
            "master": "zk://localhost:2181/mesos",
            "log_level": "warning",
            "log_file": "/tmp/mesos-cli.log"
        }
    }

Note that master accepts all values that mesos normally does, eg:

.. code-block:: bash

    localhost:5050
    zk://localhost:2181/mesos
    file:///path/to/config/above

+++++++++
Profiles
+++++++++

Want to access multiple mesos clusters without changing config? You're in luck!

To change your profile, you can run:

.. code-block:: bash

    mesos config profile new-profile

The old config will be maintained and can be switched back to at any point.

+++++++++++++++
Config Options
+++++++++++++++

.. code-block:: json

    {
        // Show stack traces on keyboard interrupt
        "debug": "false",

        // Path to where you'd like the log file
        "log_file": None,

        // Log level to use.
        "log_level": "warning",

        // Location of your master, this can be any of the values that mesos
        // supports which includes the following:
        //     localhost:5050
        //     zk://localhost:2181/mesos
        //     file:///path/to/config
        "master": "localhost:5050",

        // Scheme to use when connecting to mesos, can be either http or https
        "scheme": "http"
    }

========
Commands
========

All commands have their own options and parameters. Make sure you run `mesos [command] --help` to get the potential options.

Most commands take a `task-id` as parameter. This does not need to be an exact match and for commands where it makes sense, can match multiple tasks. Suppose your cluster is running the following tasks:

    hadoop.myjob.12345-1928731

    rails.48271236-1231234

    app-10.89934ht-2398hriwuher

    app-20.9845uih-9823hriu-2938u422

- A task-id of `app` will match both app-10 and app-20.
- A task-id of `myjob` will only match the hadoop task.
- A task-id of `1231234` will only match the rails task.

---
cat
---

.. code-block:: bash

    mesos cat task-id file [file]

------
events
------

.. code-block:: bash

    mesos events

observe events from the cluster. You will see the events occurring on the master and all slaves in the cluster (including new slaves as they arrive) as they occur.

----
find
----

.. code-block:: bash

    mesos find task-id [path]

When multiple tasks match task-id, headers will be printed between their results.

----
head
----

.. code-block:: bash

    mesos head -n 10 task-id file [file]

--
ls
--

.. code-block:: bash

    mesos ls task-id [path]

The default view is `ls -la`. When multiple tasks match task-id, headers will be printed between their results.

--
ps
--

.. code-block:: bash

    mesos ps

Output time, memory, cpu, command, user and slave/task_id information for currently running tasks.

---
scp
---

.. code-block:: bash

    mesos scp file [file ...] remote_path

Upload local file(s) to the remote_path on every slave. Note that you will need to have SSH access to every slave you'd like to upload to.

---
ssh
---

.. code-block:: bash

    mesos ssh task-id

This will SSH into the sandbox of the specified task on the slave that it is running on. Note that you need to have SSH access to this slave/sandbox.

----
tail
----

.. code-block:: tail

    mesos tail -n 10 task-id file [file]

This also implements follow. Unlike normal tail, it will look for tasks/files being created on your mesos cluster and begin to follow those files as they are written to. You can start tail in --follow mode and then launch your tasks to watch everything has it happens.

===============
Adding Commands
===============

Commands are all separate scripts. The `mesos` script inspects your path and looks for everything that starts with `mesos-`. To add a new command, just name the script `mesos-new-name` and you'll have a new command. This makes it possible to write new sub-commands in whatever language you'd like.

There are some utils that are nice to have when you're doing a new command. While all of them are available in python via. this package, a subset is available via. existing commands. This allows you to focus on the new functionality you'd like in your command (in the language you're comfortable with).

------
config
------

.. code-block:: bash

    mesos config [key] [value]


Output a json object containing all the mesos-cli config or you can get/set specific values in the configuration.

-------
resolve
-------

.. code-block:: bash

    mesos resolve [master-config]

Take either the existing configured master or the one passed on the command line and discover where the leading master is. You'll be able to use the following format:

.. code-block:: bash

    localhost:5050
    zk://localhost:2181/mesos
    file:///path/to/config/above

-----
state
-----

.. code-block:: bash

    mesos state [slave-id]

Return the full JSON state of either the master or slave (partial matches are valid).

=======
Testing
=======

There are two ways to do testing. If you'd like to just test with your local setup:

    python setup.py nosetests

For a full virtualenv + specific python versions (py26, py27), you can use tox:

    tox

.. _`DCOS CLI`: https://github.com/mesosphere/dcos-cli