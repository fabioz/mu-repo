'''
Created on 20/05/2012

@author: Fabio Zadrozny


This module was done to be used when linking is not available for the given platform nor user.
It'll do a polling strategy to keep 2 files synchronized, so, if one of the file changes, the
other one will be copied over its sync pair.

Public API:
    KeepInSync(file1, file2)
    
    and to make sure that a full sync happened in the thread:
    WaitSync() 
    or 
    StopSyncs() -- which will also stop the polling from happening. 
    
    
'''
import threading
import Queue
import os
from mu_repo.print_ import Print
import shutil



#===================================================================================================
# KeepInSync
#===================================================================================================
def KeepInSync(file1, file2):
    if _KeepInSyncThread._instance is None:
        _KeepInSyncThread._instance = _KeepInSyncThread()
        _KeepInSyncThread._instance.start()
    _KeepInSyncThread._instance.files_to_keep_in_sync_queue.put(_KeepInSyncStruct(file1, file2))



#===================================================================================================
# StopSync
#===================================================================================================
def StopSyncs():
    if _KeepInSyncThread._instance is None:
        return
    #size 0... we'll put it and only on its release we'll keep on going...
    semaphore = threading.Semaphore(0)
    _KeepInSyncThread._instance.semaphore_sync_queue.put((semaphore, 'stop'))
    semaphore.acquire()
    _KeepInSyncThread._instance = None


#===================================================================================================
# WaitSync
#===================================================================================================
def WaitSync():
    if _KeepInSyncThread._instance is None:
        return

    #size 0... we'll put it and only on its release we'll keep on going...
    semaphore = threading.Semaphore(0)
    _KeepInSyncThread._instance.semaphore_sync_queue.put((semaphore, 'regular'))
    semaphore.acquire()



#===================================================================================================
# _KeepInSyncStruct
#===================================================================================================
class _KeepInSyncStruct(object):


    __slots__ = ['file1', 'file2', 'file1_time', 'file2_time', 'file1_size', 'file2_size']


    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self._CollectStats()


    def _CollectStats(self):
        st1 = os.stat(self.file1)
        self.file1_size = st1.st_size
        self.file1_time = st1.st_mtime

        st2 = os.stat(self.file2)
        self.file2_time = st2.st_mtime
        self.file2_size = st2.st_size


    def Sync(self):
        try:
            st1 = os.stat(self.file1)
            st2 = os.stat(self.file2)
        except:
            #If any of those fails, we either don't have access or the file was removed.
            return

        changed_file_1 = self.file1_time != st1.st_mtime or self.file1_size != st1.st_size
        changed_file_2 = self.file2_time != st2.st_mtime or self.file2_size != st2.st_size

        if changed_file_1 or changed_file_2:
            if changed_file_1 and changed_file_2:
                Print('Unable to synchronize: both files: %s and %s are changed.' % (self.file1, self.file2))
                return
            if changed_file_1:
                shutil.copyfile(self.file1, self.file2)
            else:
                shutil.copyfile(self.file2, self.file1)
            self._CollectStats()


#===================================================================================================
# _KeepInSyncThread
#===================================================================================================
class _KeepInSyncThread(threading.Thread):


    _instance = None
    _TIMEOUT = 0.2 #Each 300 millis, do a full sync.


    def __init__(self):
        threading.Thread.__init__(self)
        self.files_to_keep_in_sync_queue = Queue.Queue()
        self.semaphore_sync_queue = Queue.Queue()
        self.setDaemon(True)
        self._files = []


    def run(self):
        stop = False
        while not stop:
            try:
                semaphores_to_release = []
                while True:
                    try:
                        semaphores_to_release.append(self.semaphore_sync_queue.get(False))
                    except Queue.Empty:
                        break #Break the inner while

                try:
                    while True:
                        try:
                            self._files.append(self.files_to_keep_in_sync_queue.get(False))
                        except Queue.Empty:
                            break #Break the inner while

                    #Ok, files collected without any timeout... let's see if some other arrives with
                    #a timeout.
                    try:
                        self._files.append(self.files_to_keep_in_sync_queue.get(True, self._TIMEOUT))
                    except Queue.Empty:
                        pass

                    for f in self._files:
                        f.Sync()
                finally:
                    for semaphore, cmd in semaphores_to_release:
                        if cmd == 'stop':
                            stop = True
                        semaphore.release()

            except:
                #Should not happen...
                import traceback;traceback.print_exc()




