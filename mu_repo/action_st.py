'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.execute_git_command_in_thread import Indent
from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.print_ import Print, START_COLOR, RESET_COLOR, CreateJoinedReposMsg
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel
from mu_repo.backwards import iteritems


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Note: this action always runs in parallel.
    '''
    repos_and_curr_branch = GetReposAndCurrBranch(params, verbose=False)
    as_dict = dict(repos_and_curr_branch)

    commands = []
    for repo, _branch in repos_and_curr_branch:
        commands.append(ParallelCmd(repo, [params.config.git] + ['status', '-s']))

    empty_repos_and_branches = []
    def OnOutput(output):
        branch_name = as_dict.get(output.repo, 'UNKNOWN_BRANCH')
        if not output.stdout:
            empty_repos_and_branches.append((output.repo, branch_name))
        else:
            status = [
                START_COLOR,
                output.repo,
                ' ',
                branch_name,
                ':',
                RESET_COLOR,
                '\n',
                Indent(output.stdout),
                '\n',
            ]
            Print(''.join(status))

    ExecuteInParallel(commands, on_output=OnOutput)

    if empty_repos_and_branches:
        branch_to_repos = {}
        for repo, branch in empty_repos_and_branches:
            branch_to_repos.setdefault(branch, []).append(repo)

        for branch, repos in iteritems(branch_to_repos):
            Print("${START_COLOR}Unchanged:${RESET_COLOR} %s\nat branch: ${START_COLOR}%s${RESET_COLOR}\n" % (
                CreateJoinedReposMsg('', repos), branch))

    return repos_and_curr_branch
