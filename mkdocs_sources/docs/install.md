INSTALLING
----------

**Requirements** 

- Python 2.5+, 3.2+
- git 1.7.11+ (executable must be in your path. Make sure at least ``git stash -u`` works)
- WinMerge (optional, for diffing, Windows)
- Meld (optional, for diffing, Linux)
- [pywin32](http://sourceforge.net/projects/pywin32/files/pywin32) for lines coloring (Windows).


Then if you want to get the last released version, you can do:

``pip install mu-repo``


If you want to grab from Github directly (which may be even better if you have multiple Python installs around), you can clone it from the path:

``git clone git://github.com/fabioz/mu-repo.git``

and then add the mu-repo directory to your ``PATH``, that way, 
executing ``mu`` in the command line should give a proper message.

**Note**: if you installed from Github, `mu auto-update` can be used to grab the latest changes (if you used `pip`, use `pip` itself to upgrade `mu-repo`).