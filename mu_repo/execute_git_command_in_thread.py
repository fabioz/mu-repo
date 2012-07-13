import threading
import subprocess
from mu_repo.print_ import Print, PrintError
from .print_ import START_COLOR, RESET_COLOR
from mu_repo.backwards import AsStr

#===================================================================================================
# Indent
#===================================================================================================
def Indent(txt):
    return '\n'.join(('    ' + line.lstrip()) for line in  txt.splitlines())


#===================================================================================================
# Output
#===================================================================================================
class Output(object):

    __slots__ = ['repo', 'msg', 'stdout']

    def __init__(self, repo, msg, stdout):
        self.repo = repo
        self.msg = msg
        self.stdout = stdout

    def __str__(self):
        return self.msg

#===================================================================================================
# ExecuteGitCommandThread
#===================================================================================================
class ExecuteGitCommandThread(threading.Thread):

    def __init__(self, repo, cmd, output_queue):
        threading.Thread.__init__(self)
        self.repo = repo
        self.cmd = cmd
        self.output_queue = output_queue



    class ReaderThread(threading.Thread):

        def __init__(self, stream):
            threading.Thread.__init__(self)
            self._output = []
            self._full_output = []
            self._stream = stream

        def GetPartialOutput(self):
            output = self._output
            self._output = []
            return ''.join(output)

        def GetFullOutput(self):
            return ''.join(self._full_output)

        def run(self):
            try:
                for line in self._stream.readlines():
                    line = AsStr(line)
                    self._output.append(line)
                    self._full_output.append(line)
            except:
                import traceback;traceback.print_exc()


    def _CreateReaderThread(self, p, stream_name):
        '''
        @param stream_name: 'stdout' or 'stderr'
        '''
        stream = getattr(p, stream_name)
        thread = self.ReaderThread(stream)
        thread.setDaemon(True)
        thread.start()
        return thread


    def run(self, serial=False):
        repo = self.repo
        cmd = self.cmd
        msg = ' '.join([START_COLOR, '\n', repo, ':'] + cmd + [RESET_COLOR])

        if serial:
            #Print directly to stdout/stderr without buffering.
            Print(msg)
            try:
                p = subprocess.Popen(cmd, cwd=repo)
            except:
                PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
            p.wait()

        else:
            try:
                p = subprocess.Popen(
                    cmd,
                    cwd=repo,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            except:
                PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
                self.output_queue.put(Output(repo, 'Error executing: %s on repo: %s' % (cmd, repo), ''))
                return

            self.stdout_thread = self._CreateReaderThread(p, 'stdout')
            self.stderr_thread = self._CreateReaderThread(p, 'stderr')

            p.wait()
            self.stdout_thread.join()
            self.stderr_thread.join()
            stdout = AsStr(self.stdout_thread.GetFullOutput())

            self._HandleOutput(msg, stdout)

    def GetPartialStderrOutput(self):
        stderr_thread = getattr(self, 'stderr_thread', None)
        if stderr_thread is not None:
            return stderr_thread.GetPartialOutput()

    def GetFullStderrOutput(self):
        stderr_thread = getattr(self, 'stderr_thread', None)
        if stderr_thread is not None:
            return stderr_thread.GetFullOutput()

    def __str__(self):
        return '%s : git %s' % (self.repo, ' '.join(self.cmd[1:])) #Remove the 'git' from the first part.


    def _HandleOutput(self, msg, stdout):
        stdout = stdout.strip()
        if not stdout:
            self.output_queue.put(Output(self.repo, msg + ': ' + 'empty', stdout))
        else:
            self.output_queue.put(Output(self.repo, msg + '\n' + Indent(stdout), stdout))


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
                if action is self.FINISH_PROCESSING_ITEM:
                    return
                if isinstance(action, Output):
                    self.on_output(action)
                else:
                    Print(action) #Progress message.
            except:
                PrintError()

            finally:
                self.output_queue.task_done()


#===================================================================================================
# ExecuteThreadsHandlingOutputQueue
#===================================================================================================
def ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output):
    '''
    :param on_output: callable(Output)
        A callable that's called with the Output generated by each thread executed.
    '''
    queue_printer_thread = OnOutputThread(output_queue, on_output)

    for t in threads:
        t.start()

    queue_printer_thread.start()

    for t in threads:
        try:
            total_timeout = 0.0
            progress_on_timeout = 5.0
            while True:
                t.join(timeout=progress_on_timeout)
                if t.isAlive():
                    total_timeout += progress_on_timeout
                    partial_output = t.GetPartialStderrOutput()
                    if partial_output:
                        output_queue.put('\n  %s (already waited %.2f seconds)\n%s\n' % (
                            t, total_timeout, Indent(partial_output)))
                    else:
                        output_queue.put('  %s (already waited %.2f seconds)\n' % (t, total_timeout))
                else:
                    #When on_output=Print, we may want to add stderr to the output too.
                    #full_output = t.GetFullStderrOutput()
                    #if full_output:
                    #    output_queue.put('\n  %s\n%s\n' % (
                    #        t, Indent(full_output)))
                    break

        except (KeyboardInterrupt, SystemExit):
            Print('Stopping when executing: %s' % (t,))
            raise

    output_queue.put(OnOutputThread.FINISH_PROCESSING_ITEM)
    output_queue.join()
