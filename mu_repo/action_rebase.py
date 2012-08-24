from .execute_parallel_command import ParallelCmd, ExecuteInParallel, \
    ExecuteInParallelStackingMessages
from .get_repos_and_curr_branch import GetReposAndCurrBranch
from .print_ import Print, CreateJoinedReposMsg
from .repos_with_changes import ComputeReposWithChanges

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


    ExecuteInParallelStackingMessages(
        commands,
        lambda output: not output.stderr.strip() and \
                       output.stdout.strip().startswith('Current branch') and \
                       output.stdout.strip().endswith('is up to date.'),
        lambda repos: Print(CreateJoinedReposMsg('Up-to-date: ', repos))
    )



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
            cmd = [params.config.git, 'stash', '-u'] #-u means also stash untracked files.
        commands.append(ParallelCmd(repo, cmd))

    ExecuteInParallel(commands)



#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_curr_branch = GetReposAndCurrBranch(params)

    repos_with_changes = ComputeReposWithChanges(repos_and_curr_branch, params)

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
        Print('\n  Repos with stash/rebase/unstash: ${START_COLOR}%s${RESET_COLOR}' % (
            ' '.join(x[0] for x in stash_rebase_repos)))
        _StashRepos(stash_rebase_repos, params)
        _RebaseRepos(stash_rebase_repos, params)
        _StashRepos(stash_rebase_repos, params, pop=True)

    return repos_and_curr_branch
