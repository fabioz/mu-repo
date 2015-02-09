from fnmatch import fnmatch
from mu_repo.print_ import Print

#===================================================================================================
# GetReposAndLocalBranches
#===================================================================================================
def GetReposAndLocalBranches(params, patterns=(), remote=False):
    '''
    :param params: Params
        The parameters used to get the repos and current branch (mostly using config).

    :return: list(tuple(str, set(str)))
        A list with the repository and local branches for that repository.
    '''
    repos_and_curr_branch = []
    def OnOutput(output):
        stdout = output.stdout.strip()
        if stdout:
            branches = set()
            for line in stdout.splitlines():
                branch = line.strip()
                if branch.startswith('*'):
                    branch = branch[1:].strip()

                if not patterns:
                    branches.add(branch)
                    
                else:
                    for pat in patterns:
                        if fnmatch(branch, pat):
                            branches.add(branch)

            repos_and_curr_branch.append((output.repo, branches))
        else:
            Print('Unable to execute git branch for: %s' % (output.repo,))

    from .action_default import Run  # @Reimport
    from mu_repo import Params
    old_serial = params.config.serial
    params.config.serial = False  # Cannot be serial as we want to get the output
    args = ['branch']
    if remote:
        args.append('-r')
    Run(
        Params(params.config, args, params.config_file),
        on_output=OnOutput
    )

    # Restore serial for next command.
    params.config.serial = old_serial
    return repos_and_curr_branch

