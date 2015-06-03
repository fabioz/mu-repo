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

**Tip:** ``mu register --recursive`` registers all sub directories that contain
a ``.git`` subdirectory. To register only sub directories within the current
directory, issue ``mu register --current``.

**Tip:** ``mu`` accepts registering relative paths for repositories, so, it's possible
to register relative paths in a project repository to handle dependencies 
(see [Grouping by project directories at Tips & Tricks](tips_and_tricks.md) for more details).

**Tip:** it may also be used as a git replacement on directories 
containing a ``.git`` dir.



Available commands
-------------------

* ``mu register repo1 repo2`` 
    Registers repo1 and repo2 to be tracked. Also accepts a ``--all`` or
    ``--current`` parameter, that automatically adds all repositories found in
    the current directory (but not recursively). To automatically add all
    repositories recursively, use ``--recursive``.

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

* ``mu find-branch [-r] pattern``
    Finds and prints the branches which match a given pattern. 
    (fnmatch style with auto-surrounded with asterisk)
    (-r to match remote branches) 
    Note: a shortcut exists for find-branch: mu fb  [-r] pattern

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
     
* ``mu clone``:

    mu-repo allows clones to work in multiple projects at once.
    
    For this to work, 2 things are needed:
    
    1. The base remote hosts have to be configured (through git)
    
    i.e.:

        Say that someone is working with 2 projects: projectA and projectB and projectB depends on projectA
        and they're all available on https://github.com/myuser
    
        The urls in this case to be checked out would be something as:
    
        ssh://git@github.com:myuser/projectXXX
        https://github.com/myuser/projectXXX
    
        So, the url: https://github.com/myuser or git@github.com:myuser has to be configured as a
        remote host for clones:
    
        `git config --global --add mu-repo.remote-host ssh://git@github.com:myuser`
    
        Note that it's possible to add as many urls as wanted (they'll all be checked later on
        when cloning the project).
    
        To check what are the actual urls that mu-repo will use (and the order in which they'll be
        tried, it's possible to execute):
    
        `git config --get-regexp mu-repo.remote-host`
    
    
    2. Each directory has to be configured to add the projects of the dependent projects (by committing a .mu_repo file with that information)::
    
        /libA
        /projectA (depends on libA)
        
        >> cd projectA
        >> mu register ../libA
        >> mu add .mu_repo
        >> mu commit -m "Adding dependency to mu-repo"
        
    Then, by cloning with ``mu clone projectA``, both projectA and libA will be cloned (and by going
    to projectA and using any mu command there, the commands will be propagated to dependent projects).
