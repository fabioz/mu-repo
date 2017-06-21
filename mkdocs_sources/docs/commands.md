USING
-----

The idea is that you have a structure such as:

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

**Tip:** the `.mu_repo` file is used to store the state used by `mu`, and its format
is pretty simple, so, at times it may be easier to edit it directly instead of issuing
commands. 


Custom commands
----------------

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
    Set commands to be executed serially or in parallel.

* ``mu get-vars``
    Prints the configuration file.

* ``mu fix-eol``
    Changes end of lines to ``'\n'`` on all changed files.

* ``mu find-branch [-r] pattern``

        Finds and prints the branches which match a given pattern. 
        (fnmatch style auto-surrounded with asterisk)
        (-r to match remote branches) 
        
    Note: a shortcut exists for find-branch: `mu fb  [-r] pattern`

* ``mu git-init-config``
    Initial configuration git (username, log, etc.)

* ``mu auto-update``
    Automatically updates mu-repo (using git -- only works if it has been pulled from git, if it was installed with pip, use pip to update it).

* `mu upd` Fetches changes for the current branch and compares the current branch with the fetched changes (using WinMerge or meld) -- useful to preview incoming changes.

* `mu rb` 
    Stashes your current changes, performs a rebase so that your current committed changes are put on top of incoming changes and then unstashes what has been stashed.
    Note: be careful as it'll do rebase, so, if your changes are already pushed in another branch don't use this command and do a manual merge instead. 

* ``mu dd``
    Creates a directory structure with working dir vs head (for the multiple repositores) and opens
    WinMerge on Windows or Meld on Linux with it (doing mu ac will commit exactly 
    what's compared in this situation).

    Note that the structure is created with links to the original files (or automatically synchronized 
    if links are not supported), so files edited in WinMerg/Meld will properly change the 
    original files).


    Also accepts a parameter to compare with a different commit/branch. I.e.:

        mu dd HEAD^^
        mu dd 9fd88da
        mu dd development
     
* ``mu clone``

    Clones repositories with dependencies. See: [Cloning](cloning.md) for details.
    
* ``mu group``

    Allows grouping repositories. See: [Grouping](grouping.md) for details.

* ``mu sh <command line>``

    Allows calling any command line in the registered repositories
    
    i.e.: `mu sh ls -la` will call `ls -la` on all registered repositories.
   
Also see:

* [Shortcuts](shortcuts.md)
* [Tips & Tricks](tips_and_tricks.md)
