mu-repo 
=========

Tool to help in dealing with multiple repositories
(currently only supporting git repositories -- in the same dir)

License: GPL 3, Copyright (c) 2012 by Fabio Zadrozny


INSTALLING
===========

Requisite: the python, git executables must be in your path.
Requisite for diff: winmerge must be in your path.

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

mu dd <-- will create a temporary structure and will invoke winmerge to check that structure.

mu mu-branch <-- will print the current branch for each repository tracked.

mu mu-patch <-- will create a file with diff --cached for each repository in the current dir. 

DIFFING MULTIPLE REPOSITORIES
==============================

The command 'mu dd' provides the means to diff the multiple repository structures with the 
winmerge tool so that the file can be changed while seeing the differences of the working
copy with the head in the repository.

It's similar to what would be achieved in the Eclipse synchronize view (where the file may
be edited to change the original file -- as the structure is created with links to the original
files, so files edited in winmerge will properly change the original files).


PARALLELISM
============

mu-repo by default will execute commands in parallel, but in this mode,
actions that require input will not work (and depending on the action,
may even block), so, it's possible to force it to run in serial mode, where
no buffering is done by setting the 'serial' flag to 1.

i.e.: mu set-var serial=1

(and to go back to having commands run in parallel, do mu set-var serial=0)


GIT
====

If for some reason you don't have git in the path, it's possible to force 
its location by doing:

mu set-var git=d:\bin\git\bin\git.exe

 