'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel
from mu_repo.print_ import Print, CreateJoinedReposMsg



#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)
    commands = []
    if len(params.args) > 1 and params.args[1] in ('-a', '--all'):
        for repo, branch in repos_and_curr_branch:
            commands.append(ParallelCmd(repo, [params.config.git, 'fetch']))

    else:
        for repo, branch in repos_and_curr_branch:
            #We want to update origin/master and not FETCH_HEAD
            #See: http://stackoverflow.com/questions/11051761/why-git-fetch-specifying-branch-does-not-match-fetch-without-specifying-branch/
            commands.append(ParallelCmd(
                repo, [params.config.git, 'fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch)]))


    repos = []
    def on_output(output):
        if not output.stdout.strip() and not output.stderr.strip():
            repos.append(output.repo)
        else:
            Print(output)
    ExecuteInParallel(commands, on_output=on_output)
    if repos:
        Print(CreateJoinedReposMsg('Repositories fetched with no changes:', repos))


    return repos_and_curr_branch
