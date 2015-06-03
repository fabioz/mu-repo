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

Using ``mu``, you register the repositories you want only once and then issue the commands to all of them at once:

    cd my-project
    mu register repo1 repo2
    mu fetch && mu checkout -b my-feature origin/master


``mu`` also provides other useful features such as:

* Creating groups of repositories
* Diffing changes for edition with WinMerge or meld
* Cloning multiple repositories
* Checking out branches by partial name matching
