'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel



#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)

    commands = []
    for repo, branch in repos_and_curr_branch:
        #We want to update origin/master and not FETCH_HEAD
        #See: http://stackoverflow.com/questions/11051761/why-git-fetch-specifying-branch-does-not-match-fetch-without-specifying-branch/
        commands.append(ParallelCmd(
            repo, [params.config.git, 'fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch)]))

    ExecuteInParallel(commands)
    return repos_and_curr_branch
