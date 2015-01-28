from mu_repo.backwards import iteritems
from mu_repo.get_repos_and_local_branches import GetReposAndLocalBranches
from mu_repo.print_ import Print

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    repos_and_local_branches = GetReposAndLocalBranches(
        params, patterns=['*%s*' % x for x in params.args[1:]])

    # Now, do things the other way, show a connection from the branch to the repos which have it!
    branch_to_repos = {}
    for repo, branches in repos_and_local_branches:
        for branch in branches:
            repos = branch_to_repos.get(branch)
            if repos is None:
                repos = branch_to_repos[branch] = set()
            repos.add(repo)

    # Print it for the user
    for branch, repo in sorted(iteritems(branch_to_repos)):
        if len(repos) == 1:
            msg = '${START_COLOR}%s${RESET_COLOR}' % (branch,)
        else:
            msg = '${START_COLOR}%s${RESET_COLOR}\n    %s\n' % (branch, ', '.join(sorted(repos)))
        Print(msg)
