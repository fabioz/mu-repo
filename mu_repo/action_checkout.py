from mu_repo.action_find_branch import ConvertRepoToBranchesToBranchToRepos, PrintBranchToRepos
from mu_repo.backwards import iteritems
from mu_repo.get_repos_and_local_branches import GetReposAndLocalBranches
from mu_repo.print_ import Print

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    base_branch = params.args[1]
    repos_and_local_branches = GetReposAndLocalBranches(
        params, patterns=['*%s*' % base_branch])

    # Now, do things the other way, show a connection from the branch to the repos which have it!
    branch_to_repos = ConvertRepoToBranchesToBranchToRepos(repos_and_local_branches)
            
    if len(params.config.repos) == 1:
        params.config.serial = True

    if base_branch in branch_to_repos or not branch_to_repos:
        # Ok, the default one matches, just go on with it...
        from .action_default import Run
        return Run(params)

    if len(branch_to_repos) == 1:
        # The default one does not match but we have a single match, let's use it!
        branch, _repo = iteritems(branch_to_repos).next()
        params.args[1] = branch
        from .action_default import Run  # @Reimport
        return Run(params)

    # Print it for the user
    Print('Found more than one branch that matches ${START_COLOR}%s${RESET_COLOR}:\n' % params.args[1])
    PrintBranchToRepos(branch_to_repos, params)
    Print('\n${START_COLOR}ERROR${RESET_COLOR}: unable to decide branch to work on.', __color__='RED')

