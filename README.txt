mu-repo 
========================

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
        