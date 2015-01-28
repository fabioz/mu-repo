mu-repo 
=========

Tool to help working with multiple git repositories
(short for *Multiple Repositories*).

Note: in case you're seeing this repo wondering why the last commit
was so long ago, I'd like to mention that this is because it's a
pretty stable tool and seldomly needs maintanance
(i.e.: it hasn't become abandoned -- quite the contrary,
I use it daily without any hiccups).


Overview
--------

``mu`` is a command line tool that helps you execute the same commands in multiple ``git`` repositories.

Suppose you have repositories that are related, and want to execute the same ``git`` commands in each (for instance, create
a branch with the same name in all of them).


.. code-block:: bash

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

Using ``mu``, you register the repositories you want only once:

.. code-block:: bash
    
    cd my-project
    mu register repo1 repo2
    mu fetch && mu checkout -b my-feature origin/master


INSTALLING
----------

**Requirements** 

- Python 2.5+, 3.2+
- git 1.7.11+ (executable must be in your path. Make sure at least ``git stash -u`` works)
- winmerge (optional, for diffing, Windows)
- pywin32_ for lines coloring (Windows).

.. _PyWin32: http://sourceforge.net/projects/pywin32/files/pywin32

Then, grab mu-repo from git::

    git clone git://github.com/fabioz/mu-repo.git

add the mu-repo directory to your ``PATH`` so that after that, 
executing ``mu`` in the command line should give a proper message.

USING
-----

The idea is that you have a structure such as::

    /workspace
        .mu_repo <- configuration file (created by mu commands)
        /repo1   <- git repository 
            /.git
        /repo2
            /.git
        ...
    
Then go to the root directory containing the repositories 
(in this case ``cd /workspace``), add the repositories you want 
to work with and issue commands to all registered repos.

**Tip:** ``mu register --all`` registers all sub directories that contain
a ``.git`` subdirectory.

**Note:** it may also be used as a git replacement on directories 
containing a ``.git`` dir.

Commands
~~~~~~~~

* ``mu register repo1 repo2`` 
    Registers repo1 and repo2 to be tracked. Also accepts an ``--all`` parameter, that automatically
    adds all repositories found in the current directory (but not recursively).

* ``mu unregister repo1 repo2``
    Unregisters previously tracked repositories (also accepts ``--all``).

* ``mu list``
    Lists the currently tracked repositories.

* ``mu set-var git=d:/bin/git/bin/git.exe``
    Set git location to be used. Only needed if git is not found in your ``PATH``.

* ``mu set-var serial=0|1``
    Set commands to be executed serially or in parallel_.

* ``mu get-vars``
    Prints the configuration file.

* ``mu github-request``
    Gets a request from github.

* ``mu post-review bug_id group``
    Posts a review with the changes committed.

* ``mu fix-eol``
    Changes end of lines to ``'\n'`` on all changed files.

* ``mu find-branch pattern``
    Finds and prints the branches which match a given pattern 
    (fnmatch style with auto-surrounded with asterisk).

* ``mu install``
    Initial configuration git (username, log, etc.)

* ``mu auto-update``
    Automatically updates mu-repo (using git -- must have been pulled from git as in the instructions).

* ``mu dd``:
     Creates a directory structure with working dir vs head and opens
     WinMerge on Windows or meld on Linux with it (doing mu ac will commit exactly 
     what's compared in this situation).

     Also accepts a parameter to compare with a different commit/branch. I.e.::

         mu dd HEAD^^
         mu dd 9fd88da
         mu dd development
     
* ``mu group``:
    Grouping can be used so you can have separate sets of projects that may not be related to each
    other. For instance, suppose you work on project A, which depends on this repositories::
    
        /libA
        /mylib
        /projectA
    
    And project B, which depends on::
    
        /libB
        /mylib
        /projectB
    
    Grouping enables you to switch easily between the two projects. To create a group to work on 
    projectA and its dependencies, use "mu group add <name>" to create the new group::
    
        ] mu group add pA --empty   # not passing --empty means using the current repositories as starting point
        ] mu register libA mylib projectA
        ] mu list
        Tracked repositories:
        
        libA
        mylib
        projectA
   
    The same goes for project B::
    
        ] mu group add pB  --empty
        ] mu register libB mylib projectB
        ] mu list
        Tracked repositories:
        
        libB
        mylib
        projectB
    
    You can see which group you're on::
    
        ] mu group
          pA
        * pB
        
    And switch between the two::
    
        ] mu group switch pA
        Switched to group "pA".
    
    If you are done with a group, use "mu group rm" to remove it::
        
        ] mu group rm pA
        Group "pA" removed (no current group).
    
Shortcuts:

* mu st         = Nice status message for all repos (always in parallel)
* mu co branch  = git checkout branch
* mu mu-patch   = git diff --cached --full-index > output to file for each repo
* mu mu-branch  = git rev-parse --abbrev-ref HEAD (print current branch)
* mu up         = git fetch origin curr_branch:refs/remotes/origin/curr_branch
* mu upd | sync = up/diff incoming changes
* mu a          = git add -A
* mu c msg      = git commit -m "Message" (the message must always be passed)
* mu ac msg     = git add -A & git commit -m (the message must always be passed)
* mu acp msg    = same as 'mu ac' + git push origin current branch.
* mu p          = git push origin current branch.
* mu rb         = git rebase origin/current branch.
* mu shell      = On msysgit, call sh --login -i (linux-like env)

Any other command is passed directly to git for each repository, for example::

    mu pull
    mu fetch
    mu push
    mu checkout release


DIFFING MULTIPLE REPOSITORIES
-----------------------------

The command ``mu dd`` provides the means to diff the multiple repository structures 
with winmerge (Windows) or meld (Linux) so that the file can be changed 
while seeing the differences of the working copy with the head in the repository.

It's similar to what would be achieved in the Eclipse synchronize view (where the 
file may be edited to change the original file -- as the structure is created with 
links to the original files, so files edited in winmerge/meld will properly change the 
original files).


.. _parallel:

PARALLELISM
-----------

mu-repo by default will execute commands in serial, but it's also possible
to enable commands to be run in parallel, but note that in this mode,
actions that require input will not work (and depending on the action,
may even block if input is required -- i.e.: password). It's possible 
to force it to run in parallel mode, by setting the 'serial' flag to false::

    mu set-var serial=false


.. note:: Some actions considered 'safe' will always be executed in parallel (i.e.: mu st)

GIT
---

If for some reason you don't have git in the path, it's possible to force 
its location by doing::

    mu set-var git=d:\bin\git\bin\git.exe

 
LICENSE
-------

GPL 3, Copyright (c) 2012-2014 by Fabio Zadrozny

