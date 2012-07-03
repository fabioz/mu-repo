import threading
import subprocess
from mu_repo.print_ import Print
from .print_ import START_COLOR, RESET_COLOR
from mu_repo.backwards import AsBytes, AsStr

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

    def __init__(self, repo, args, config, output_queue):
        threading.Thread.__init__(self)
        self.repo = repo
        self.config = config
        self.args = args
        self.output_queue = output_queue


    def run(self, serial=False):
        args = self.args
        repo = self.repo
        git = self.config.git or 'git'
        cmd = [git] + args
        msg = ' '.join([START_COLOR, '\n', repo, ':'] + cmd + [RESET_COLOR])

        if serial:
            #Print directly to stdout/stderr without buffering.
            Print(msg)
            try:
                p = subprocess.Popen(cmd, cwd=repo)
            except:
                from .print_ import PrintError
                PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
            p.wait()

        else:
            try:
                p = subprocess.Popen(
                    cmd,
                    cwd=repo,
                    #stderr=subprocess.STDOUT, # -- let stderr go to sys.stderr!
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
                #Just in case it tries to read something, put empty stuff in there.
                try:
                    p.stdin.write(AsBytes('\n' * 20))
                    p.stdin.close()
                except:
                    pass #Just ignore any error here!
            except:
                from .print_ import PrintError
                PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
                self.output_queue.put(Output(repo, 'Error executing: %s on repo: %s' % (cmd, repo), ''))
                return

            stdout, stderr = p.communicate()
            stdout = AsStr(stdout)
            if stderr:
                stdout += ('\n' + AsStr(stderr))

            self._HandleOutput(msg, stdout)


    def _HandleOutput(self, msg, stdout):
        stdout = stdout.strip()
        if not stdout:
            self.output_queue.put(Output(self.repo, msg + ': ' + 'empty', stdout))
        else:
            self.output_queue.put(Output(self.repo, msg + '\n' + Indent(stdout), stdout))
