'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print
import os.path
import threading
import subprocess
from mu_repo import Status

#===================================================================================================
# Indent
#===================================================================================================
def Indent(txt):
    return '\n'.join('  ' + line for line in  txt.splitlines()) + '\n'


#===================================================================================================
# ExecuteCommandThread
#===================================================================================================
class ExecuteCommandThread(threading.Thread):

    def __init__(self, repo, args):
        self.repo = repo
        self.args = args
        threading.Thread.__init__(self)
        self.stdout = ''
        self.stderr = ''

    def run(self, serial=False):
        args = self.args
        repo = self.repo
        cmd = ['git'] + args
        msg = ' '.join(['\n', repo, ':'] + cmd + ['\n'])

        if serial:
            Print(msg)
            p = subprocess.Popen(cmd, cwd=repo)
            p.wait()

        else:
            self.stdout += msg
            p = subprocess.Popen(cmd, cwd=repo, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
            if stdout:
                if serial:
                    Print(Indent(stdout))
                else:
                    self.stdout += Indent(stdout)
            if stderr:
                if serial:
                    Print(Indent(stderr))
                else:
                    self.stderr += Indent(stderr)


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args
    stream = params.stream
    config = params.config

    if args[0] == 'st':
        args[0] = 'status'

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
            t = ExecuteCommandThread(repo, args)
            threads.append(t)

    if config.serial:
        for t in threads:
            t.run(serial=True) #When serial will print as is executing.
    else:
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        for t in threads:
            if t.stdout:
                Print(t.stdout, file=stream)
            if t.stderr:
                Print(t.stderr, file=stream)


    return Status('Finished', True)
