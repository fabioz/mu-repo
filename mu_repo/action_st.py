'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread, Indent
from mu_repo.on_output_thread import ExecuteThreadsHandlingOutputQueue
from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.print_ import Print, START_COLOR, RESET_COLOR
try:
    import Queue
except ImportError:
    import queue as Queue


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Note: this action always runs in parallel.
    '''
    repos_and_curr_branch = GetReposAndCurrBranch(params, verbose=False)
    as_dict = dict(repos_and_curr_branch)

    threads = []
    output_queue = Queue.Queue()
    for repo, branch in repos_and_curr_branch:
        t = ExecuteGitCommandThread(
            repo, ['status', '-s'], params.config, output_queue)
        threads.append(t)

    def OnOutput(output):
        branch_name = as_dict.get(output.repo, 'UNKNOWN_BRANCH')
        summary = [START_COLOR, output.repo, ' ', branch_name, ':', RESET_COLOR]
        if not output.stdout:
            Print(''.join((summary + [' empty\n'])))
        else:
            Print(''.join((summary + ['\n' , Indent(output.stdout), '\n'])))

    ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output=OnOutput)
    return repos_and_curr_branch
