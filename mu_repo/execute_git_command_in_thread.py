import threading
import subprocess
from mu_repo.print_ import Print

#===================================================================================================
# Indent
#===================================================================================================
def Indent(txt):
    return '\n'.join(('    ' + line.lstrip()) for line in  txt.splitlines())


#===================================================================================================
# ExecuteGitCommandThread
#===================================================================================================
class ExecuteGitCommandThread(threading.Thread):

    def __init__(self, repo, args, config, output_queue, put_raw_output=False):
        threading.Thread.__init__(self)
        self.repo = repo
        self.config = config
        self.args = args
        self.put_raw_output = put_raw_output
        self.output_queue = output_queue

    def run(self, serial=False):
        args = self.args
        repo = self.repo
        git = self.config.git or 'git'
        cmd = [git] + args
        msg = ' '.join(['\n', repo, ':'] + cmd)

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
                self.output_queue.put('Error executing: %s' % (cmd,))
                return

            stdout, stderr = p.communicate()
            if stderr:
                stdout += ('\n' + stderr)

            self._HandleOutput(msg, stdout)

    def _HandleOutput(self, msg, stdout):
        stdout = stdout.strip()
        if not stdout:
            self.output_queue.put(msg + ': empty')
        else:
            self.output_queue.put(msg + '\n' + Indent(stdout))
