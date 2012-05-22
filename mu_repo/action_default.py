'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print
import os.path
import threading
from mu_repo import Status
from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread


#===================================================================================================
# QueuePrinterThread
#===================================================================================================
class QueuePrinterThread(threading.Thread):

    FINISH_PROCESSING_ITEM = ()

    def __init__(self, output_queue, stream):
        threading.Thread.__init__(self)
        self.output_queue = output_queue
        self.stream = stream
        self.setDaemon(True)


    def run(self):
        while True:
            action = self.output_queue.get(True)
            try:
                if action == self.FINISH_PROCESSING_ITEM:
                    return
                Print(action, file=self.stream)
            finally:
                self.output_queue.task_done()


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args
    stream = params.stream
    config = params.config
    import Queue
    output_queue = Queue.Queue()

    if args[0] == 'st':
        args[0] = 'status'
        if len(args) == 1:
            args.insert(1, '--porcelain')

    elif args[0] == 'co':
        args[0] = 'checkout'

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg, file=stream)
        return Status(msg, True, config)

    threads = []
    for repo in config.repos:
        if not os.path.exists(repo):
            Print('%s does not exist' % (repo,), file=stream)
        else:
            t = ExecuteGitCommandThread(repo, args, config, output_queue)
            threads.append(t)

    if config.serial:
        for t in threads:
            t.run(serial=True) #When serial will print as is executing.
    else:
        queue_printer_thread = QueuePrinterThread(output_queue, stream)

        for t in threads:
            t.start()

        queue_printer_thread.start()

        for t in threads:
            t.join()

        output_queue.put(QueuePrinterThread.FINISH_PROCESSING_ITEM)
        output_queue.join()

    return Status('Finished', True)

