=========
mesos-cli
=========

CLI tools to work with mesos.

-----------------------------
What problem does this solve?
-----------------------------

I am comfortable debugging programs from the command line. I have a set of tools that I use from coreutils that end up being used every day. A day doesn't go by when I've not used grep, find, or cat.

While mesos allows you to treat all the nodes in your data center as anonymous resources, debugging still needs to be done on specific hosts. Currently, it requires multiple tools and context switches to gather the pieces that you need to look at what a specific task is doing. Most of these existing tools don't work well with the command line and I'm unable to use the workflow that I've become comfortable with.

--------------------------
How is the problem solved?
--------------------------

To solve the problem, some of the coreutil commands have been re-implemented to work on the scale of a data center instead of a single host.

- commands and options have been copied as closely as it makes sense. They should have the same options that you're used to.
- pipe works the way you'd expect it to. You should be able to replace most host specific debug scripts easily.
- mesos itself isn't required locally. Developers want to debug their tasks without having a local copy of mesos installed.
- everything is task centric. There's no need to worry about specifying a framework if you don't want to, just put in the task id.
- complete/match everything. Task IDs are long and normally require cut/paste to get exact matches. Instead, all `task` parameters are partial matches, no need to type that long thing in. Also, most parameters tab-complete (see the section on auto-completion to configure), just type a couple characters in and get what you're looking for.
- extensibility. Write your own subcommands. Most of the required information can be accessed via. existing subcommands (leading master resolution via. mesos-resolve), so you only need to implement what you want and not re-invent the wheel.

------------
Installation
------------

This currently relies on mesos being installed locally. Make sure that `mesos` is on your path.

.. code-block:: bash

    sudo pip install git+ssh://github.com:mesosphere/mesos-cli.git@master

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

Place a configuration file at:

.. code-block:: bash

    ~/.mesos_cli.json

If you're using a non-local master, you'll need to configure where the master should be found like so:

.. code-block:: json

    {
        "master": "zk://localhost:2181/mesos"
    }

Note that this accepts all values that mesos normally does, eg:

.. code-block:: bash

    localhost:5050
    zk://localhost:2181/mesos
    file:///path/to/config/above

========
Commands
========

All commands have their own options and parameters. Make sure you run `mesos command --help` to get the potential options.

Most commands take a `task-id` as parameter. This does not need to be an exact match and for commands where it makes sense, can match multiple tasks. Supposed your cluster is running the following tasks:

    hadoop.myjob.12345-1928731

    rails.48271236-1231234

    app-10.89934ht-2398hriwuher

    app-20.9845uih-9823hriu-2938u422

- A task-id of app will match both app-10 and app-20.
- A task-id of myjob will only match the hadoop task.
- A task-id of 1231234 will only match the rails task.

---
ssh
---

.. code-block:: bash

    mesos ssh task-id

This will SSH into the sandbox of the specified task on the slave that it is running on. Note that you need to have SSH access to this slave/sandbox.

--
ls
--

.. code-block:: ls

    mesos ls task-id [path]

The default view is `ls -la`. When multiple tasks match task-id, headers will be printed between their results.

----
find
----

.. code-block:: find

    mesos find task-id [path]

When multiple tasks match task-id, headers will be printed between their results.

---
cat
---

.. code-block:: cat

    mesos cat task-id file [file]

----
head
----

.. code-block:: head

    mesos head -n 10 task-id file [file]

----
tail
----

.. code-block:: tail

    mesos tail -n 10 task-id file [file]

This also implements follow. Unlike normal tail, it will look for tasks/files being created on your mesos cluster and begin to follow those files as they are written to. You can start tail in --follow mode and then launch your tasks to watch everything has it happens.
