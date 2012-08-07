from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel



#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)

    commands = []
    for repo, branch in repos_and_curr_branch:
        #Do git rebase origin/current_branch for all repos.
        commands.append(ParallelCmd(
            repo, [params.config.git, 'rebase', 'origin/%s' % (branch,)]))

    ExecuteInParallel(commands)
    return repos_and_curr_branch
