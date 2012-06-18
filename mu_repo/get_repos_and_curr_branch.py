'''
Created on Jun 16, 2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print

#===================================================================================================
# GetReposAndCurrBranch
#===================================================================================================
def GetReposAndCurrBranch(params):
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
            Print("Will handle 'origin %s' for '%s'." % (stdout, output.repo))
        else:
            Print('Unable to update (could not get current branch for: %s)' % (output.repo,))

    on_output = OnOutput

    from .action_default import Run #@Reimport
    from mu_repo import Params
    old_serial = params.config.serial
    params.config.serial = False #Cannot be serial as we want to get the output
    Run(
        Params(params.config, ['rev-parse', '--abbrev-ref', 'HEAD'], params.config_file),
        on_output=on_output
    )

    #Restore serial for next command.
    params.config.serial = old_serial
    return repos_and_curr_branch

