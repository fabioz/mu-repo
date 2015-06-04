Tips & Tricks
---------------

### Grouping by project directories

To make the most out of `mu-repo`, it's recommended that the projects you work with specify
their own dependencies by committing the `.mu_repo` file with relative paths so that it's
possible to go inside any of those repository dirs and issue commands not only to the repository,
but all the dependent repositories at once (and this will also enable you to [clone](cloning.md) the all
the needed repositories at once).

Example:

Say you have `projectA`, `projectB` and `projectC` and have a dependency so that:

    projectC -> projectB, projectA
    projectB -> projectA 

It's recommended that you go into projectC and do:

    mu register ../projectA
    mu register ../projectB

and in projectB:

    mu register ../projectA

By doing so, when going into projectC and doing a command using `mu`, the command will also be issued
to `projectB` and `projectA` and by going into `projectB` it'll also execute commands in `projectA`.

Also, this will enable the command `mu clone projectC` to clone `projectB` and `projectC` all at once
(See the [Cloning](cloning.md) for further details).


**Tip:** If you have several projects and need even finer grained control over where to execute a command, it's possible
to create a group to identify a subset of the repositories (See the [Grouping Repositories](grouping.md) for further details). 


### .mu_repo

The `.mu_repo` file has a simple format (each line must be something as name=var or name=var1, var2), so, it's straightforward
to edit it with your favorite editor.


### mu acp

mu provides some [shortcuts](shortcuts.md) which extend a bit on git and the `mu acp <commit message>` (which stands for `add -A`, `commit -m <commit message>`, `push`) is
a really handy one, so, if you just checked your structure (with `mu dd` and want to add all the changes, commit them and push in a single
command, use `mu acp` (also, just `mu a` or `mu ac <commit message>` or `mu c <commit message>` can be used just for one of those parts).  

### Calling a different executable

The whole concept of `mu-repo` is calling git on multiple repositories, but it's actually possible
to specify any executable for it to work on (by assiging it to the `git` variable): 

    mu set-var git=c:\bin\myexecutable.exe

 