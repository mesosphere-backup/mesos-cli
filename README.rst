=========
mesos-cli
=========

Additional CLI tools to work with mesos.

------------
Installation
------------

This currently relies on mesos being installed locally. Make sure that `mesos` is on your path.

.. code-block:: bash

    sudo pip install git+ssh://github.com:mesosphere/mesos-cli.git@master

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
