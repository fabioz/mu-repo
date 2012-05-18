from mu_repo.print_ import Print
from mu_repo import Status

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args
    stream = params.stream
    config_file = params.config_file
    config = params.config

    if len(args) < 2:
        msg = 'Repository (dir name) to track not passed'
        Print(msg, file=stream)
        return Status(msg, False)
    repos = config.repos
    msgs = []
    for repo in args[1:]:
        if repo in repos:
            msg = 'Repository: %s not added (already there)' % (repo,)
            Print(msg, file=stream)
            msgs.append(msg)
        else:
            repos.append(repo)
            msg = 'Repository: %s added' % (repo,)
            Print(msg, file=stream)
            msgs.append(msg)

    with open(config_file, 'w') as f:
        f.write(str(config))

    return Status('\n'.join(msgs), True, config)



