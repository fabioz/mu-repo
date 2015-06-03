Tips & Tricks
---------------

#### Grouping by project directories

To make the most out of `mu-repo`, it's recommended that the projects you work with specify
their own dependencies by committing the `.mu_repo` file with relative dirs so that it's
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
to create a group identify a subset of the repositories (See the [Grouping Repositories](grouping.md) for further details). 

#### .mu_repo

The `.mu_repo` file has a simple format (each line must be something as name=var or name=var1, var2), so, it's straightforward
to edit it with your favorite editor.
