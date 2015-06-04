mu-repo 
=========

Tool to help working with multiple git repositories
(short for *Multiple Repositories*).

Overview
--------

``mu`` is a command line tool that helps you execute the same commands in multiple ``git`` repositories.

Suppose you have repositories that are related, and want to execute the same ``git`` commands in each (for instance, create
a branch with the same name in all of them).


    $ cd my-project
    $ ls 
    repo1 repo2
    $ cd repo1
    $ git fetch && git checkout -b my-feature origin/master
    ...
    $ cd repo2
    $ git fetch && git checkout -b my-feature origin/master
    ...


Besides being tedious, it is easy to forget some of the repositories when you're dealing with several.

Using ``mu``, you register the repositories you want only once and then issue commands to all of them at once:

    cd my-project
    mu register repo1 repo2
    mu fetch && mu checkout -b my-feature origin/master


``mu`` also provides other useful features such as:

* [Cloning multiple repositories](cloning.md)
* [Creating groups of repositories](grouping.md)
* Diffing changes for edition with WinMerge or meld (see [mu dd on Commands](commands.md))
* Checking out branches by partial name matching (`mu co v1.2` would checkout branch `prog_v1.2`) 
* Preview incoming changes on current branch (see [mu upd on Commands](commands.md))
* [Shortcuts](shortcuts.md) for common git operations.

Proceed to:

* [Install](install.md)
* [Configuration](config.md)
* [Commands](commands.md)
* [Shortcuts](shortcuts.md)
* [Grouping Repositories](grouping.md)
* [Cloning Multiple Repositories](cloning.md)
* [Tips & Tricks](tips_and_tricks.md)

