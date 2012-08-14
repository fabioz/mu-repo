from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel
from mu_repo.print_ import Print



#===================================================================================================
# _GetReposWithChanges
#===================================================================================================
def _GetReposWithChanges(repos_and_curr_branch, params):
    commands = []
    for repo, _branch in repos_and_curr_branch:
        commands.append(ParallelCmd(repo, [params.config.git] + ['status', '-s']))

    repos_with_changes = {}
    def OnOutput(output):
        if not output.stdout:
            repos_with_changes[output.repo] = False
        else:
            repos_with_changes[output.repo] = True

    ExecuteInParallel(commands, on_output=OnOutput)
    return repos_with_changes


#===================================================================================================
# _RebaseRepos
#===================================================================================================
def _RebaseRepos(repos_and_branch, params):
    '''
    :param repos_and_branch: list(tuple(str, str))
    '''
    commands = []

    for repo, branch in repos_and_branch:
        #Simple: Do git rebase origin/current_branch for all repos.
        commands.append(ParallelCmd(
            repo, [params.config.git, 'rebase', 'origin/%s' % (branch,)]))

    ExecuteInParallel(commands)

#===================================================================================================
# _StashRepos
#===================================================================================================
def _StashRepos(repos_and_branch, params, pop=False):
    '''
    :param repos_and_branch: list(tuple(str, str))
    '''
    commands = []

    for repo, _branch in repos_and_branch:
        #Simple: Do git rebase origin/current_branch for all repos.
        if pop:
            cmd = [params.config.git, 'stash', 'pop']
        else:
            cmd = [params.config.git, 'stash']
        commands.append(ParallelCmd(repo, cmd))

    ExecuteInParallel(commands)



#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)

    repos_with_changes = _GetReposWithChanges(repos_and_curr_branch, params)

    #Step 1: do a simple rebase on the ones that don't have any changes.
    rebase_repos = []
    stash_rebase_repos = []
    for repo, branch in repos_and_curr_branch:
        if repos_with_changes[repo]:
            stash_rebase_repos.append((repo, branch))
        else:
            rebase_repos.append((repo, branch))

    if rebase_repos:
        _RebaseRepos(rebase_repos, params)

    if stash_rebase_repos:
        Print('\n  Repos with stash/rebase/unstash: ${START_COLOR}%s${RESET_COLOR}' % (' '.join(x[0] for x in stash_rebase_repos)))
        _StashRepos(stash_rebase_repos, params)
        _RebaseRepos(stash_rebase_repos, params)
        _StashRepos(stash_rebase_repos, params, pop=True)

    return repos_and_curr_branch
