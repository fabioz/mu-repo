Cloning Multiple Repositories
------------------------------

mu-repo allows clones to work in multiple projects at once, although some prep-work is needed for it to work:

### The remote base url(s) have to be configured.

Say that you're working with 2 projects: `projectA` and `projectB` and `projectB` depends on `projectA`
and they're all available on `https://github.com/myuser`

The urls in this case to be checked out would be something as:

* `ssh://git@github.com:myuser/projectXXX`
* `https://github.com/myuser/projectXXX`

So, the url: `https://github.com/myuser` or `git@github.com:myuser` has to be configured as a
remote host for clones by doing:

`git config --global --add mu-repo.remote-base-url ssh://git@github.com:myuser`

Note that it's possible to add as many urls as wanted.

To check what are the actual urls that mu-repo will use (and the order in which they'll be
tried, it's possible to do):

`git config --get-regexp mu-repo.remote-base-url`

By doing so, it'll be possible to do `mu clone projectA` without specifying the base-url. This
is nice on itself, but to go one step further and actually clone multiple projects, we need to
configure the projects themselves by adding the dependency info (this is done by [grouping by project directories][tips_and_tricks.md]).


    # Given a project structure with:
    /libA
    /projectA (depends on libA)
    
    # Go into projectA and make it depend on libA: 
    >> cd projectA
    >> mu register ../libA
    
    # Actually commit the .mu_repo so that the dependency is available when cloning:
    >> mu add .mu_repo
    >> mu commit -m "Adding dependency to mu-repo"

Then, by cloning with ``mu clone projectA``, both `projectA` and `libA` will be cloned (and by going
to `projectA` and using any `mu` command there, the commands will be propagated to `libA`).

**Note:** Dependencies are not recursively calculated, so, if `projectC` depends on `projectB`
which in turn depends on `projectA`, `projectA` has to be registered in `projectC` and in `projectB`. 