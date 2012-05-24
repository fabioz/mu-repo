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
# OnOutputThread
#===================================================================================================
class OnOutputThread(threading.Thread):

    FINISH_PROCESSING_ITEM = ()

    def __init__(self, output_queue, on_output):
        threading.Thread.__init__(self)
        self.output_queue = output_queue
        self.on_output = on_output
        self.setDaemon(True)


    def run(self):
        while True:
            action = self.output_queue.get(True)
            try:
                if action == self.FINISH_PROCESSING_ITEM:
                    return
                self.on_output(action)
            finally:
                self.output_queue.task_done()


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    on_output = Print

    args = params.args
    stream = params.stream
    config = params.config
    import Queue
    output_queue = Queue.Queue()

    arg0 = args[0]
    if arg0 == 'st':
        args[0] = 'status'
        if len(args) == 1:
            args.insert(1, '--porcelain')

    elif arg0 == 'co':
        args[0] = 'checkout'

    elif len(args) == 1:
        if arg0 == 'mu-branch':
            args[0] = 'rev-parse'
            args.insert(1, '--abbrev-ref')
            args.insert(2, 'HEAD')

        elif arg0 == 'mu-patch':
            args[0] = 'diff'
            args.insert(1, '--cached')
            args.insert(2, '--full-index')
            config.serial = False #Always exec in parallel mode!
            def OnOutput(output):
                stdout = output.stdout
                if stdout.strip():
                    Print('Writing diff --cached for: ', output.repo)
                    with open('__diff__.' + output.repo + '.patch', 'w') as f:
                        f.write(stdout)
                else:
                    Print('EMPTY diff --cached for: ', output.repo)
            on_output = OnOutput

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg, file=stream)
        return Status(msg, True, config)

    threads = []
    for repo in config.repos:
        if not os.path.exists(repo):
            Print('%s does not exist' % (repo,), file=stream)
        else:
            t = ExecuteGitCommandThread(
                repo, args, config, output_queue)

            threads.append(t)

    if config.serial:
        for t in threads:
            t.run(serial=True) #When serial will print as is executing.
    else:
        queue_printer_thread = OnOutputThread(output_queue, on_output)

        for t in threads:
            t.start()

        queue_printer_thread.start()

        for t in threads:
            t.join()

        output_queue.put(OnOutputThread.FINISH_PROCESSING_ITEM)
        output_queue.join()

    return Status('Finished', True)

