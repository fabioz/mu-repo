'''
Created on 30/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print
from mu_repo.backwards import iteritems, raw_input

#===================================================================================================
# Run
#===================================================================================================
def Run(params):

    #Update them
    from .action_up import Run
    repos_and_curr_branch = Run(params)
    if not repos_and_curr_branch:
        Print('No tracked repos!')
        return

    branch_to_repos = {}

    #Check if all on the same branch
    for repo, branch in repos_and_curr_branch:
        curr = branch_to_repos.setdefault(branch, [])
        curr.append(repo)

    if len(branch_to_repos) > 1:
        msg = '\n${START_COLOR}Warning: found repos in different branches${RESET_COLOR}:\n  %s\nProceed?(y/n)' % ('\n  '.join([str('Branch: ${START_COLOR}%s${RESET_COLOR} (%s)' % (key, ', '.join(val))) for (key, val) in branch_to_repos.items()]))
        ret = ''
        while ret not in ('y', 'n'):
            Print(msg)
            ret = raw_input().strip().lower()

        if ret != 'y':
            return

    #Diff it
    from .action_diff import Run  #@Reimport

    initial_args = params.args[:]
    initial_repos = params.config.repos[:]

    for branch, repos in iteritems(branch_to_repos):
        params.args = initial_args + ['origin/' + branch]
        params.config.repos = repos
        if len(branch_to_repos) > 1:
            Print('\nOutput for branch: ${START_COLOR}%s${RESET_COLOR} (%s)' % (branch, ', '.join(repos)))
        Run(params)

    params.args = initial_args
    params.config.repos = initial_repos


