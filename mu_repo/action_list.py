from mu_repo.print_ import Print
from mu_repo import Status

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    stream = params.stream
    config = params.config

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg, file=stream)
        return Status(msg, True, config)
    else:
        repo_str = '\n'.join(sorted(config.repos))
        Print('Tracked Repositories:\n', file=stream)
        Print(repo_str, file=stream)
        return Status(repo_str, True, config)



