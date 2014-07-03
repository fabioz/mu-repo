'''
Created on Jun 16, 2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print
from mu_repo.backwards import iteritems

#===================================================================================================
# GetReposAndCurrBranch
#===================================================================================================
def GetReposAndCurrBranch(params, verbose=True):
    '''
    :param params: Params
        The parameters used to get the repos and current branch (mostly using config).

    :return: list(tuple(str, str))
        A list with the repository and current branch for that repository.
    '''
    repos_and_curr_branch = []
    def OnOutput(output):
        stdout = output.stdout.strip()
        if stdout:
            repos_and_curr_branch.append((output.repo, stdout))
        else:
            if verbose:
                Print('Unable to update (could not get current branch for: %s)' % (output.repo,))

    from .action_default import Run #@Reimport
    from mu_repo import Params
    old_serial = params.config.serial
    params.config.serial = False #Cannot be serial as we want to get the output
    Run(
        Params(params.config, ['rev-parse', '--abbrev-ref', 'HEAD'], params.config_file),
        on_output=OnOutput
    )
    if verbose:
        branch_to_repos = {}
        for repo, branch in repos_and_curr_branch:
            branch_to_repos.setdefault(branch, []).append(repo)

        for branch, repos in iteritems(branch_to_repos):
            Print("Will handle ${START_COLOR}origin %s${RESET_COLOR} for: %s\n" % (
                branch, ', '.join(sorted(repos))))

    #Restore serial for next command.
    params.config.serial = old_serial
    return repos_and_curr_branch

