from mu_repo.action_diff import ParsePorcelain
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel

#===================================================================================================
# ComputeReposWithChanges
#===================================================================================================
def ComputeReposWithChanges(repos_and_curr_branch, params):
    '''
    :param repos_and_curr_branch: list(tuple(str, str))
        A list with the repos and the current branch for each repo.
        
    :param params: Params
        Used to get the git to be used.
        
    :return: dict(str->bool)
        A dictionary where the key is the repo and the value a boolean indicating whether
        there are local changes in that repo.
    '''
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
# ComputeReposWithChangesFromCurrentBranchToOrigin
#===================================================================================================
def ComputeReposWithChangesFromCurrentBranchToOrigin(repos_and_curr_branch, params, target_branch=None):
    '''
    :param repos_and_curr_branch: list(tuple(str, str))
        A list with the repos and the current branch for each repo.
        
    :param params: Params
        Used to get the git to be used.

    :param target_branch: str
        If passed, instead of comparing with the same current branch in the origin, it'll compare
        with origin/target_branch.

    :return: list(str)
        Returns a list with the repositories that have some difference from branch to origin/branch.
    '''
    commands = []
    for repo, curr_branch in repos_and_curr_branch:
        commands.append(
            ParallelCmd(repo, [params.config.git] + ('diff --name-only -z origin/%s' % (
                target_branch or curr_branch,)).split()))

    repos_with_changes = []
    def OnOutput(output):
        for _entry in ParsePorcelain(output.stdout, only_split=True):
            #Iterate: if we have a match, add it as having a change!
            repos_with_changes.append(output.repo)
            break

    ExecuteInParallel(commands, on_output=OnOutput)
    return repos_with_changes

