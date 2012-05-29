'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread
from mu_repo.on_output_thread import ExecuteThreadsHandlingOutputQueue
from mu_repo.print_ import Print
import Queue


#===================================================================================================
# GetReposAndCurrBranch
#===================================================================================================
def GetReposAndCurrBranch(params):
    repos_and_curr_branch = []
    def OnOutput(output):
        stdout = output.stdout.strip()
        if stdout:
            repos_and_curr_branch.append((output.repo, stdout))
            Print("Will fetch 'origin %s' for %s." % (stdout, output.repo))
        else:
            Print('Unable to update (could not get current branch for: %s)' % (output.repo,))

    on_output = OnOutput

    from .action_default import Run #@Reimport
    from mu_repo import Params
    params.config.serial = False #Cannot be serial as we want to get the output
    Run(
        Params(params.config, ['rev-parse', '--abbrev-ref', 'HEAD'], params.config_file),
        on_output=on_output
    )
    return repos_and_curr_branch


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)

    threads = []
    output_queue = Queue.Queue()
    for repo, branch in repos_and_curr_branch:
        t = ExecuteGitCommandThread(
            repo, ['fetch', 'origin', branch], params.config, output_queue)
        threads.append(t)

    ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output=Print)
