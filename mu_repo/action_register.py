from __future__ import with_statement
from mu_repo.print_ import Print
from mu_repo import Status
import os

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args
    config_file = params.config_file
    config = params.config

    if len(args) < 2:
        msg = 'Repository (dir name|--all) to track not passed'
        Print(msg)
        return Status(msg, False)
    repos = config.repos
    msgs = []
    args = args[1:]
    join = os.path.join
    isdir = os.path.isdir
    if '--all' in args:
        if len(args) > 1:
            Print('If --all is passed in mu register, no other parameter should be passed.')
            return

        args = [repo for repo in os.listdir('.') if isdir(join(repo, '.git'))]

    elif '--select' in args:
        if len(args) > 1:
            Print('If --select is passed in mu register, no other parameter should be passed.')
            return
        Print('Still not finished!')
        return

    elif '--restore' in args:
        if len(args) > 1:
            Print('If --restore is passed in mu register, no other parameter should be passed.')
            return
        Print('Still not finished!')
        return

    group_repos = config.groups.get(config.current_group, None)
    
    for repo in args:
        if repo in repos:
            msg = 'Repository: %s skipped, already registered' % (repo,)
        else:
            repos.append(repo)
            msg = 'Repository: %s registered' % (repo,)
            
        if group_repos is not None:
            if repo not in group_repos:
                group_repos.append(repo)
                msg += ' (added to group "%s")' % config.current_group
            else:
                msg += ' (already in group "%s")' % config.current_group
                
        Print(msg)
        msgs.append(msg)

    with open(config_file, 'w') as f:
        f.write(str(config))

    return Status('\n'.join(msgs), True, config)



