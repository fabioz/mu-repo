Configuration
-------------

#### PARALLELISM


mu-repo will execute commands in serial mode by default, but it's also possible
to enable all commands to be run in parallel by setting the **serial** flag to false:

    mu set-var serial=false
    
**Note: Some actions considered 'safe' will always be executed in parallel by mu-repo (i.e.: mu st) even without the serial flag set to false.**

#### Caveats

* Actions that require input will not work (and depending on the action, may even block if input is required -- i.e.: waiting for password).
* The output of commands will be buffered when running in parallel, so, the output may not appear colored as it would when executing in serial mode.



#### GIT

If for some reason you don't have git in the path, it's possible to force 
its location by doing:

    mu set-var git=d:\bin\git\bin\git.exe

 
