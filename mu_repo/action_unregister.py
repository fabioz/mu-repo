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
    remove_all = '--all' in args
    if remove_all and args != ['--all']:
        msg = 'If --all is given, no other parameter should be passed.'
        Print(msg)
        return Status(msg, False)
        
    new_args = []
    for arg in args:
        if arg.endswith('\\') or arg.endswith('/'):
            arg = arg[:-1]
        new_args.append(arg)
    args = new_args

    group_repos = config.groups.get(config.current_group, None)

    if remove_all:
        repos[:] = []   
        msg = 'Removed all repositories.' 
        if group_repos:
            group_repos[:] = []
            msg += ' (removed from group "%s")' % config.current_group
        Print(msg)
        msgs.append(msg)
    else:
        for repo in args:
            if repo in repos:
                msg = 'Repository: %s unregistered' % (repo,)
                repos.remove(repo)
            else:
                msg = 'Repository: %s skipped' % (repo,)
                
            if group_repos is not None:
                if repo in group_repos:
                    group_repos.remove(repo)
                    msg += ' (removed from group "%s")' % config.current_group
                    
            Print(msg)
            msgs.append(msg)

    with open(config_file, 'w') as f:
        f.write(str(config))

    return Status('\n'.join(msgs), True, config)



