'''
Created on May 23, 2012

@author: Fabio Zadrozny
'''
import shutil
import os

#===================================================================================================
# _OnError
#===================================================================================================
def _OnError(func, path, exc_info):
    """
    See: http://stackoverflow.com/questions/2656322/python-shutil-rmtree-fails-on-windows-with-access-is-denied
    
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, _OnError=_OnError)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

#===================================================================================================
# RmTree
#===================================================================================================
def RmTree(path, ignore_errors=False, onerror=None):
    return shutil.rmtree(path, ignore_errors, onerror or _OnError)
