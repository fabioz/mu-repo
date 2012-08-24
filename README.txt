mu-repo 
=========

Tool to help working with multiple git repositories
(short of 'Multiple repositories')

License: GPL 3, Copyright (c) 2012 by Fabio Zadrozny


INSTALLING
===========

Requisite: git (1.7.11 or higher) executable must be in your path (i.e.: at least stash -u must work).

Requisite: python (2.5 or higher) must be in your path.

Requisite for diff: winmerge must be in your path.

Then, grab mu-repo from git:

git clone git://github.com/fabioz/mu-repo.git

add the mu-repo directory to your PATH so that after that, 
doing 'mu' in the command line should give a proper message.

Note:
======

If your lines are not properly colored on Windows, please install PyWin32

Binaries may be gotten from: http://sourceforge.net/projects/pywin32/files/pywin32/


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

Tip: "mu register --all" registers all subdirs with '.git'
(and the configuration file may be edited to unregister 
repositories later on).

Note: it may also be used as a git replacement on directories 
containing a .git dir.

Commands:

* mu register repo1 repo2: Registers repo1 and repo2 to be tracked.
* mu register --all: Registers all subdirs with .git.
* mu list: Lists the currently tracked repositories.
* mu set-var git=d:/bin/git/bin/git.exe: Set git location to be used.
* mu set-var serial=0|1: Set commands to be executed serially or in parallel.
* mu get-vars: Prints the configuration file.
* mu github-request: Gets a request from github.
* mu post-review bug_id group: posts a review with the changes committed.
* mu fix-eol: Changes end of lines to '\n' on all changed files.
* mu install: Initial configuration git (username, log, etc.)
* mu auto-update: Automatically updates mu-repo
  (using git -- must have been pulled from git as in the instructions).

* mu dd:
     Creates a directory structure with working dir vs head and opens
     WinMerge with it (doing mu ac will commit exactly what's compared in this
     situation).

     Also accepts a parameter to compare with a different commit/branch. I.e.:
     mu dd HEAD^^
     mu dd 9fd88da
     mu dd development

Shortcuts:

mu st         = Nice status message for all repos (always in parallel)
mu co branch  = git checkout branch
mu mu-patch   = git diff --cached --full-index > output to file for each repo
mu mu-branch  = git rev-parse --abbrev-ref HEAD (print current branch)
mu up         = git fetch origin curr_branch:refs/remotes/origin/curr_branch
mu upd | sync = up/diff incoming changes
mu a          = git add -A
mu c msg      = git commit -m "Message" (the message must always be passed)
mu ac msg     = git add -A & git commit -m (the message must always be passed)
mu acp msg    = same as 'mu ac' + git push origin current branch.
mu p          = git push origin current branch.
mu rb         = git rebase origin/current branch.
mu shell      = On msysgit, call sh --login -i (linux-like env)

Any other command is passed directly to git for each repository:
I.e.:

mu pull
mu fetch
mu push
mu checkout release

Note: Some actions considered 'safe' may always be executed in parallel (i.e.: mu st)


DIFFING MULTIPLE REPOSITORIES
==============================

The command 'mu dd' provides the means to diff the multiple repository structures 
with the winmerge tool so that the file can be changed while seeing the differences 
of the working copy with the head in the repository.

It's similar to what would be achieved in the Eclipse synchronize view (where the 
file may be edited to change the original file -- as the structure is created with 
links to the original files, so files edited in winmerge will properly change the 
original files).


PARALLELISM
============

mu-repo by default will execute commands in serial, but it's also possible
to enable commands to be run in parallel, but note that in this mode,
actions that require input will not work (and depending on the action,
may even block if input is required -- i.e.: password). It's possible 
to force it to run in parallel mode, by setting the 'serial' flag to false.

i.e.: mu set-var serial=false

(and to go back to having commands run in serial, do mu set-var serial=true)


GIT
====

If for some reason you don't have git in the path, it's possible to force 
its location by doing:

mu set-var git=d:\bin\git\bin\git.exe

 