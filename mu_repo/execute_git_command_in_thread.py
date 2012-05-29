import threading
import subprocess
from mu_repo.print_ import Print
from mu_repo import COLOR, RESET

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
        msg = ' '.join([COLOR, '\n', repo, ':'] + cmd + [RESET])

        if serial:
            #Print directly to stdout/stderr without buffering.
            Print(msg)
            p = subprocess.Popen(cmd, cwd=repo)
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
                p.stdin.write('\n' * 20)
                p.stdin.close()
            except:
                self.output_queue.put(Output(repo, 'Error executing: %s' % (cmd,), ''))
                return

            stdout, stderr = p.communicate()
            if stderr:
                stdout += ('\n' + stderr)

            self._HandleOutput(msg, stdout)


    def _HandleOutput(self, msg, stdout):
        stdout = stdout.strip()
        if not stdout:
            self.output_queue.put(Output(self.repo, msg + ': ' + 'empty', stdout))
        else:
            self.output_queue.put(Output(self.repo, msg + '\n' + Indent(stdout), stdout))
