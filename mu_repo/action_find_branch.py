from mu_repo.backwards import iteritems
from mu_repo.get_repos_and_local_branches import GetReposAndLocalBranches
from mu_repo.print_ import Print

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args[1:]
    remote = False
    if len(args) > 0:
        if args[0] == '-r':
            del args[0]
            remote = True

    repos_and_local_branches = GetReposAndLocalBranches(
        params, patterns=['*%s*' % x for x in args], remote=remote)

    # Now, do things the other way, show a connection from the branch to the repos which have it!
    branch_to_repos = ConvertRepoToBranchesToBranchToRepos(repos_and_local_branches)

    # Print it for the user
    PrintBranchToRepos(branch_to_repos, params)

def ConvertRepoToBranchesToBranchToRepos(repos_and_local_branches):
    branch_to_repos = {}
    for repo, branches in repos_and_local_branches:
        for branch in branches:
            repos = branch_to_repos.get(branch)
            if repos is None:
                repos = branch_to_repos[branch] = set()
            repos.add(repo)
    return branch_to_repos

def PrintBranchToRepos(branch_to_repos, params):
    for branch, repos in sorted(iteritems(branch_to_repos)):
        if len(repos) == 1:
            msg = '${START_COLOR}%s${RESET_COLOR}' % (branch,)
        elif len(repos) == len(set(params.config.repos)):
            msg = '${START_COLOR}%s${RESET_COLOR}   (all repos)' % (branch,)
        else:
            msg = '${START_COLOR}%s${RESET_COLOR}   (%s)' % (branch, ', '.join(sorted(repos)))
        Print(msg)
