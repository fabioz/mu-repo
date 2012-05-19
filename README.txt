mu-repo 
=========

Tool to help in dealing with multiple repositories
(currently only supporting git repositories -- in the same dir)

License: GPL 3, Copyright (c) 2012 by Fabio Zadrozny


INSTALLING
===========

Requisite: the python and git executables must be in your path.

Then, grab mu-repo from git:

git clone git://github.com/fabioz/mu-repo.git

add the mu-repo directory to your PATH so that after that, 
doing 'mu' in the command line should give a proper message.


USING
=======

The idea is that you have a structure such as:

/workspace
    .mu_repo <- configuration file (created by mu commands)
    /repo1   <- git repository name (i.e.: directory name with .git file)
        /.git
    /repo2
        /.git
    ...
    
Then go to the root directory containing the repositories 
(in this case cd /workspace), add the repositories you want 
to work with and issue commands to all registered repos.

mu register repo1 repo2 <-- register repo1 and repo2 in mu-repo.

mu list <-- will print a list of the repositories registered.

mu status <-- will go into each subdir and do 'git status'.

mu checkout release <-- will go into each subdir and do 'git checkout release'.      


PARALLELISM
============

mu-repo by default will execute commands in parallel, but in this mode,
actions that require input will not work (and depending on the action,
may even block), so, it's possible to force it to run in serial mode, where
no buffering is done by setting the 'serial' flag to 1.

i.e.: mu set_var serial=1

(and to go back to having commands run in parallel, do mu set_var serial=0)


GIT
====

If for some reason you don't have git in the path, it's possible to force 
its location by doing:

mu set_var git=d:\bin\git\bin\git.exe

 