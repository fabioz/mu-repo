# License: LGPL
#
# Copyright: Brainwy Software
'''
To use, create a SystemMutex, check if it was acquired (get_mutex_aquired()) and if acquired the
mutex is kept until the instance is collected or release_mutex is called.

I.e.:

mutex = SystemMutex('my_unique_name')
if mutex.get_mutex_aquired():
    print('acquired')
else:
    print('not acquired')
'''

from mu_repo.null import NULL
import re
import sys
import tempfile
import traceback
import weakref


def check_valid_mutex_name(mutex_name):
    # To be windows/linux compatible we can't use non-valid filesystem names
    # (as on linux it's a file-based lock).

    regexp = re.compile(r'[\*\?"<>|/\\:]')
    result = regexp.findall(mutex_name)
    if result is not None and len(result) > 0:
        raise AssertionError('Mutex name is invalid: %s' % (mutex_name,))

if sys.platform == 'win32':

    import os

    class SystemMutex(object):

        def __init__(self, mutex_name):
            check_valid_mutex_name(mutex_name)
            filename = self.filename = os.path.join(tempfile.gettempdir(), mutex_name)
            try:
                os.unlink(filename)
            except:
                pass
            try:
                handle = os.open(filename, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                self.handle = handle
            except:
                self._release_mutex = NULL
                self._acquired = False
            else:
                def release_mutex(*args, **kwargs):
                    # Note: can't use self here!
                    if not getattr(release_mutex, 'called', False):
                        release_mutex.called = True
                        try:
                            os.close(handle)
                        except:
                            traceback.print_exc()
                        try:
                            # Removing is optional as we'll try to remove on startup anyways (but
                            # let's do it to keep the filesystem cleaner).
                            os.unlink(filename)
                        except:
                            pass

                # Don't use __del__: this approach doesn't have as many pitfalls.
                self._ref = weakref.ref(self, release_mutex)

                self._release_mutex = release_mutex
                self._acquired = True

        def write(self, s):
            os.write(self.handle, s)

        def get_mutex_aquired(self):
            return self._acquired

        def release_mutex(self):
            self._release_mutex()

else:  # Linux
    import os
    import fcntl

    class SystemMutex(object):

        def __init__(self, mutex_name):
            check_valid_mutex_name(mutex_name)
            filename = self.filename = os.path.join(tempfile.gettempdir(), mutex_name)
            try:
                handle = open(filename, 'w')
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.handle = handle
            except:
                self._release_mutex = NULL
                self._acquired = False
                try:
                    handle.close()
                except:
                    pass
            else:
                def release_mutex(*args, **kwargs):
                    # Note: can't use self here!
                    if not getattr(release_mutex, 'called', False):
                        release_mutex.called = True
                        try:
                            fcntl.flock(handle, fcntl.LOCK_UN)
                        except:
                            traceback.print_exc()
                        try:
                            handle.close()
                        except:
                            traceback.print_exc()
                        try:
                            # Removing is pretty much optional (but let's do it to keep the
                            # filesystem cleaner).
                            os.unlink(filename)
                        except:
                            pass

                # Don't use __del__: this approach doesn't have as many pitfalls.
                self._ref = weakref.ref(self, release_mutex)

                self._release_mutex = release_mutex
                self._acquired = True

        def write(self, s):
            self.handle.write(s)

        def get_mutex_aquired(self):
            return self._acquired

        def release_mutex(self):
            self._release_mutex()

def create_system_mutex_for_current_dir():
    import hashlib
    s = hashlib.sha1()
    s.update(os.path.normcase(os.path.normpath(os.path.abspath(os.curdir))).encode('utf-8'))
    return SystemMutex(s.hexdigest() + '.mu_repo_mutex')
