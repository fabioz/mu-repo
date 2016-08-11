from .print_ import RESET_COLOR, START_COLOR
from mu_repo.backwards import AsStr
from mu_repo.config import UseShellOnSubprocess
from mu_repo.print_ import Print, PrintError
import subprocess
import threading

#===================================================================================================
# Indent
#===================================================================================================
def Indent(txt):
    return '\n'.join(('    ' + line.lstrip()) for line in  txt.splitlines())


#===================================================================================================
# Output
#===================================================================================================
class Output(object):

    __slots__ = ['repo', 'msg', 'stdout', 'stderr']

    def __init__(self, repo, msg, stdout, stderr):
        self.repo = repo
        self.msg = msg
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return self.msg

    def __repr__(self, *args, **kwargs):
        return 'Output: %s\nStderr: %s\nStdout: %s\nMessage: %s' % (
            self.repo, self.stderr, self.stdout, self.msg)

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

        shell = UseShellOnSubprocess()
        if serial:
            #Print directly to stdout/stderr without buffering.
            Print(msg)
            p = None
            try:
                p = subprocess.Popen(cmd, cwd=repo, shell=shell)
            except:
                PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
            if p is not None:
                p.wait()

        else:
            try:
                p = subprocess.Popen(
                    cmd,
                    cwd=repo,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    shell=shell
                )
            except:
                import os
                PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo + ' cwd: ' + os.path.abspath('.'))
                self.output_queue.put(Output(repo, 'Error executing: %s on repo: %s' % (cmd, repo), '', ''))
                return

            self.stdout_thread = self._CreateReaderThread(p, 'stdout')
            self.stderr_thread = self._CreateReaderThread(p, 'stderr')

            p.wait()
            self.stdout_thread.join(2) #finish in at most 2 seconds
            self.stderr_thread.join(2) #finish in at most 2 seconds
            stdout = AsStr(self.stdout_thread.GetFullOutput())
            stderr = AsStr(self.stderr_thread.GetFullOutput())

            self._HandleOutput(msg, stdout, stderr)

    def GetPartialStderrOutput(self):
        stderr_thread = getattr(self, 'stderr_thread', None)
        if stderr_thread is not None:
            return stderr_thread.GetPartialOutput()

    def GetFullStderrOutput(self):
        stderr_thread = getattr(self, 'stderr_thread', None)
        if stderr_thread is not None:
            return stderr_thread.GetFullOutput()

    def GetFullStdoutOutput(self):
        stdout_thread = getattr(self, 'stdout_thread', None)
        if stdout_thread is not None:
            return stdout_thread.GetFullOutput()

    def __str__(self):
        return '${START_COLOR}%s : git %s${RESET_COLOR}' % (self.repo, ' '.join(self.cmd[1:])) #Remove the 'git' from the first part.


    def _HandleOutput(self, msg, stdout, stderr):
        stdout = stdout.strip()
        if not stdout:
            if stderr:
                self.output_queue.put(Output(self.repo, msg + '\n' + Indent(stderr), stdout, stderr))
            else:
                self.output_queue.put(Output(self.repo, msg + ': ' + 'empty', stdout, stderr))
        else:
            self.output_queue.put(Output(self.repo, msg + '\n' + Indent(stdout), stdout, stderr))


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
                    if self.on_output is not None:
                        self.on_output(action)
                    #else:
                    #    Note: in this case, the output will be printed by the
                    #    ExecuteThreadsHandlingOutputQueue method (along with the stderr).
                    #    Print(action)
                else:
                    Print(action) #Progress message.
            except:
                PrintError()

            finally:
                self.output_queue.task_done()


#===================================================================================================
# ExecuteThreadsHandlingOutputQueue
#===================================================================================================
def ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output=None):
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
                        msg = '\n  %s (elapsed %d seconds)\n%s\n' % (
                                t, total_timeout, Indent(partial_output))
                    else:
                        msg = '  %s (elapsed %d seconds)\n' % (t, total_timeout)
                    if total_timeout % 60 == 0:
                        msg += (
                            '  This command seems to be taking a while.\n'
                            '  Note that mu is not able to detect if git got stuck waiting for input.\n'
                            '  Consider executing git directly on the repository to see the output.\n'
                        )

                    output_queue.put(msg)
                else:
                    if on_output is None:
                        # Note: only print when on_output is None (on other situations, nothing
                        # should be printed, as the caller of the method will use the output for
                        # something else, such as getting the name of a branch, etc).
                        stdout = t.GetFullStdoutOutput()

                        stderr = t.GetFullStderrOutput()
                        if stdout:
                            full_output = stdout
                        else:
                            full_output = ''
                        if stderr:
                            if full_output:
                                full_output += '\n'
                            full_output += stderr

                        if full_output:
                            output_queue.put('\n  %s\n%s' % (
                                t, Indent(full_output)))
                        else:
                            output_queue.put('\n  %s' % (t,))

                    break

        except (KeyboardInterrupt, SystemExit):
            Print('Stopping when executing: %s' % (t,))
            raise

    output_queue.put(OnOutputThread.FINISH_PROCESSING_ITEM)
    output_queue.join()
