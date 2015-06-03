Grouping repositories
----------------------

Note: the recommended approach is [grouping by project directories](tips_and_tricks.md) as that way
[mu clone](cloning.md) may be used to clone several repositories at once too (mu-repo **1.1.0** onwards).

The `mu group` command is available for when finer grained control over grouping of repositories is needed.

`mu group` can be used so you can have separate sets of projects that may not be related to each other. 
For instance, suppose you work on project A, which depends on this repositories:
 
    /libA
    /mylib
    /projectA

And project B, which depends on:

    /libB
    /mylib
    /projectB

Grouping enables you to switch easily between the two projects. To create a group to work on 
projectA and its dependencies, use `mu group add <name>` to create the new group:

    # Note: not passing --empty means using the current repositories as starting point
    >> mu group add pA --empty 
    >> mu register libA mylib projectA
    >> mu list
    
    Tracked repositories:
    
    libA
    mylib
    projectA

The same goes for project B:

    >> mu group add pB  --empty
    >> mu register libB mylib projectB
    >> mu list
    
    Tracked repositories:
    
    libB
    mylib
    projectB

You can see which group you're on:

    >> mu group
      pA
    * pB
    
And switch between the two:

    >> mu group switch pA
    Switched to group "pA".

Or alternatively just use `mu group switch` without parameters:

    >> mu group switch
    Please choose which group you want to switch to:
    [0]: pA
    [1]: pB
    
    [C]: Cancel

If you are done with a group, use "mu group rm" to remove it:
    
    >> mu group rm pA
    Group "pA" removed (no current group).
