from mu_repo.print_ import Print
from mu_repo import Status

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    config = params.config

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg)
        return Status(msg, True, config)
    else:
        repo_str = '\n'.join(sorted(config.repos))
        Print('Tracked Repositories:\n')
        Print(repo_str)
        return Status(repo_str, True, config)



