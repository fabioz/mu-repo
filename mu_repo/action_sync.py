'''
Created on 30/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print

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

    #Check if all on the same branch
    initial_branch = None
    initial_repo = None
    for repo, branch in repos_and_curr_branch:
        if initial_branch is None:
            initial_branch = branch
            initial_repo = repo

        if initial_branch != branch:
            Print('All repos are expected to be in the same branch (%s in %s and %s in %s)' % (
                initial_repo, initial_branch, repo, branch))
            return

    #Diff it
    from .action_diff import Run #@Reimport
    params.args.append('origin/' + initial_branch)
    Run(params)

