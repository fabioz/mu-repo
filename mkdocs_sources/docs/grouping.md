Grouping repositories
----------------------

Usually [grouping by project directories](tips_and_tricks.md) is enough for most use-cases, but sometimes
you need even finer grained control over the repositories to issue a command.

For that, `mu-repo` allows the creation of groups through `mu group`.


* ``mu group``:
    Grouping can be used so you can have separate sets of projects that may not be related to each
    other. For instance, suppose you work on project A, which depends on this repositories:
    
        /libA
        /mylib
        /projectA
    
    And project B, which depends on:
    
        /libB
        /mylib
        /projectB
    
    Grouping enables you to switch easily between the two projects. To create a group to work on 
    projectA and its dependencies, use "mu group add <name>" to create the new group:
    
        >> mu group add pA --empty   # not passing --empty means using the current repositories as starting point
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
    
    If you are done with a group, use "mu group rm" to remove it:
        
        >> mu group rm pA
        Group "pA" removed (no current group).
