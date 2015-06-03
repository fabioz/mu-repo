INSTALLING
----------

**Requirements** 

- Python 2.5+, 3.2+
- git 1.7.11+ (executable must be in your path. Make sure at least ``git stash -u`` works)
- winmerge (optional, for diffing, Windows)
- meld (optional, for diffing, Linux)
- pywin32_ for lines coloring (Windows).

.. _PyWin32: http://sourceforge.net/projects/pywin32/files/pywin32


Then if you want to get the last released version, you can do:

``pip install mu-repo``


If you want to develop it, you can clone it from the path:

``git clone git://github.com/fabioz/mu-repo.git``

and then add the mu-repo directory to your ``PATH``, that way, 
executing ``mu`` in the command line should give a proper message.
