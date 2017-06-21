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
* [Open Url](open_url.md) for opening the browser to create pull requests over multiple repositories.
* Run **arbitrary commands** on registered repositories (through `mu sh <command to execute>`).

### New on 1.6.0

Created `mu sh` action to execute non git commands (i.e.: `mu sh make` or `mu sh python setup.py install` or `mu mvn install`).

Fixed issue in `mu open-url` action when dealing with relative repositories. See [Open Url](open_url.md).

### New on 1.5.0

Fixed issue where the colors were not being properly shown on Python 3.

Fixed issue on `mu clone` on Python 3.

Created `mu open-url` action to help on creating pull requests on multiple repositories at once. See [Open Url](open_url.md).

### New on 1.4.0

Fix for issue on mu-repo not working if `.mu_repo` file was still not created.

If a commit message is not given on `mu ac`, open the git-configured editor and ask for it.

Fixed issue on **mu dd** when executed with a repository referencing ano ther repository in the same level (i.e.: ./A references ../B).

### New on 1.3.0

This version allows you to call `mu` in subdirectories (it'll search directories upwards for the first
directory containing a .mu_repo file or a .git directory).

### New on 1.2.0

This version allows you to clone multiple repositories at once. See:
[Cloning multiple repositories](cloning.md)

### Proceed to:

* [Install](install.md)
* [Configuration](config.md)
* [Commands](commands.md)
* [Shortcuts](shortcuts.md)
* [Grouping Repositories](grouping.md)
* [Cloning Multiple Repositories](cloning.md)
* [Tips & Tricks](tips_and_tricks.md)
* [Open Url (Create pull requests)](open_url.md)

