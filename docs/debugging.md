
# Debugging tasks on mesos

- What is happening with my task?

    To get a listing of the running tasks on your mesos cluster:

        mesos ps

- What if my task isn't running?

    Well, you can see all the inactive tasks too!

        mesos ps -i

- That list is huge, how can I narrow it down?

    You can use all the normal unix tools.

        mesos ps -i | grep task

- I'd like to see if something is bouncing, can I do that?

    Sure enough!

        watch mesos ps -i

- Alright, my task is bouncing up and down. How do I find the logs?

    Well, there's no need to ssh to a ton of boxes, all you need to do is tail.

        mesos tail task

- I really don't want to type my task name (simple.732a53b4-1c2c-11e4-88de-36cd2b7b1e01). Is there a way that I don't have to?

    There are actually a couple ways. First off, most commands let you partial match task names. For example, using the task id from above, this is all we'd have to type for tail.

        mesos tail simple

    You would now tail stdout for all the tasks that begin with simple.

    For some commands, you still need to put in the precise task id (ssh for example). If you enable tab completion in your shell of choice, you'll be able to tab complete task names too.

- Well, that shows me something but tasks are starting and dying quickly. Is there a way to watch all of that?

    Sure enough, you can follow stdout/stderr anywhere on the entire cluster.

        mesos tail -f task stdout stderr

    This will pick up new tasks matching the `task` pattern anywhere in your data center. There's no reason for you to worry about where these tasks are running.

- Whew, that helped me narrow it down a little bit. Something is wrong with a file. Is there a way to see what's going on?

    Luckily, you can see what is in your task's sandbox.

        mesos find task

- Well, my file is there but the size is odd. Can I see what is in the file?

    You can look at the contents of any file in a task's sandbox.

        mesos cat task config_file.json

- I guess there is something on the slaves themselves getting in the way. How do I find out where a task is running?

    There's no need to find out where a task is running, you can ssh directly to it given the task id.

        mesos ssh full-task-id
