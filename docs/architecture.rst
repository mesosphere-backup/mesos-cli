==============
Architecture
==============

---------------------
High Level Decisions
---------------------

- commands and options have been copied as closely as it makes sense. They should have the same options that you're used to.
- pipe works the way you'd expect it to. You should be able to replace most host specific debug scripts easily.
- mesos itself isn't required locally. Developers want to debug their tasks without having a local copy of mesos installed.
- everything is task centric. There's no need to worry about specifying a framework if you don't want to, just put in the task id.
- lazy matching. Task IDs are long and normally require cut/paste to get exact matches. Instead, all `task` parameters are partial matches, no need to type that long thing in.
- auto-complete. Most parameters tab-complete (see the section on auto-completion to configure), just type a couple characters in and get what you're looking for.
- extensibility. Write your own subcommands. Most of the required information can be accessed via. existing subcommands (leading master resolution via. mesos-resolve), so you only need to implement what you want and not re-invent the wheel.

- Concurrency is done via. `concurrent.futures`.
- All interactions that can be done in parallel, should be done that way (fetching slave state, files, ...)

-------------------
Language Decisions
-------------------

- PEP8 is followed strictly. flake8 is used for verification as part of the test process.
- python 2.6 and 2.7 are officially supported.
- wherever possible, python 3 support is used (print statements, concurrent)

---------
Commands
---------

- All commands are `mesos-command-name`.
- There is a `mesos` command that handles command discovery. It doesn't care what language commands have been written in. The PATH is looked at for any command containing `mesos-`.
- Each command is its own script. These manifest as entry points in `setup.py`.
- The `main` function in every command is what gets executed.
- Command specific arguments use `argparse`.

--------------
Configuration
--------------

- Global options (master config, logging) go into a config file.
- Config files have a search path (see cfg.py).
- Default values are set, config file overrides them.

+++++++++++
Profiles
+++++++++++

- You can create a profile within the config and switch between it.

---------------
Master + Slave
---------------

- The master class has a CURRENT singleton that should always be used.

++++++++++++++++++
Cached Properties
++++++++++++++++++

- Any property that requires a remote request (master.state for example) uses util.CachedProperty. This will memoize it until the ttl has elapsed.
- Properties that do not change (slave.log) should be memoized and not cached.

------------
Mesos Files
------------

- Files provided by mesos have their own file implementation.
- The implementation provides a feature rich python class that lets you do all the normal file operations on it.

---------------
Tab Completion
---------------

- The library being used for tab completion hoooks into `argparse`
- For arguments that require looking up something remotely, a function is provided.
