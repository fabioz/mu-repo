'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread
from mu_repo.on_output_thread import ExecuteThreadsHandlingOutputQueue
from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.print_ import Print
try:
    import Queue
except ImportError:
    import queue as Queue



#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)

    threads = []
    output_queue = Queue.Queue()
    for repo, branch in repos_and_curr_branch:
        #We want to update origin/master and not FETCH_HEAD
        #See: http://stackoverflow.com/questions/11051761/why-git-fetch-specifying-branch-does-not-match-fetch-without-specifying-branch/
        t = ExecuteGitCommandThread(
            repo, ['fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch)], params.config, output_queue)
        threads.append(t)

    ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output=Print)
    return repos_and_curr_branch
