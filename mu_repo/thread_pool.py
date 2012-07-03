try:
    from Queue import Queue
except ImportError:
    from queue import Queue
from threading import Thread

#===================================================================================================
# _Worker
#===================================================================================================
class _Worker(Thread):


    def __init__(self, task_queue):
        Thread.__init__(self)
        self.tasks_queue = task_queue
        self.setDaemon(True)


    def run(self):
        while True:
            func = self.tasks_queue.get()
            try:
                try:
                    func()
                except:
                    from mu_repo.print_ import PrintError
                    PrintError()
            finally:
                self.tasks_queue.task_done()

#===================================================================================================
# _ThreadPool
#===================================================================================================
class _ThreadPool(object):

    def __init__(self, num_threads=None):
        if num_threads is None:
            #Only for Python 2.6+
            try:
                import multiprocessing
                num_threads = multiprocessing.cpu_count() * 2
            except:
                num_threads = 8


        self.tasks_queue = Queue()
        self.workers = []
        for _i in xrange(num_threads):
            w = _Worker(self.tasks_queue)
            w.start()
            self.workers.append(w)


    def AddTask(self, func):
        self.tasks_queue.put(func)


    def Join(self):
        self.tasks_queue.join()


#===================================================================================================
# Default thread pool instance
#===================================================================================================
_thread_pool = _ThreadPool()


#===================================================================================================
# AddTask
#===================================================================================================
def AddTask(func):
    _thread_pool.AddTask(func)


#===================================================================================================
# Join
#===================================================================================================
def Join():
    _thread_pool.Join()

