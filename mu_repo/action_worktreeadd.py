import os
from .execute_parallel_command import ParallelCmd, ExecuteInParallel, \
    ExecuteInParallelStackingMessages
from .get_repos_and_curr_branch import GetReposAndCurrBranch
from .print_ import Print, PrintError, CreateJoinedReposMsg
from shutil import copy2
#===================================================================================================
# _WorktreeAdd
#===================================================================================================
def _WorktreeAdd(repos_and_branch, params):
    '''
    :param repos_and_branch: list(tuple(str, str))
    '''
    commands = []

    base_path = "_wt"
    if ( len(params.args) > 2):
        base_path = params.args[1]
        branch = params.args[2]
    else:
        # Use _wt folder in the current repo
        branch = params.args[1]

    # always make sure the branch was added
    if ( not branch in base_path ):
        base_path = os.path.join(base_path, branch)

    base_path = os.path.abspath(base_path)

    repos = []
    for repo, _branch in repos_and_branch:
        repos.append(repo)

    repos.sort(key = len)

    Print(repos)

    for repo in repos:
        #Simple: Do git worktree add <base path> <branch> for all repos
        Print([params.config.git, 'worktree', 'add', os.path.join(base_path,repo) , branch])
        commands.append(ParallelCmd(
            repo, [params.config.git, 'worktree', 'add', os.path.join(base_path,repo) , branch]))

    # True for serial...may be creating nested repos which can break things
    ExecuteInParallel(commands, None, True) 
    # Need to copy .murepo file for the new worktree to work with mu-repo
    copy2(params.config_file, base_path)


#===================================================================================================
# Run
#===================================================================================================
def Run(params):

    repos_and_curr_branch = GetReposAndCurrBranch(params)

    if ( len(params.args) < 2 ):
        PrintError("worktreeadd needs a branch or base path and a branch")
        raise

    _WorktreeAdd(repos_and_curr_branch, params)

    return repos_and_curr_branch
