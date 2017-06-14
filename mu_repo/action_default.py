'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from __future__ import with_statement

import os.path

from mu_repo import Status
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel
from mu_repo.print_ import Print


#===================================================================================================
# Run
#===================================================================================================
def Run(params, on_output=None):
    args = params.args
    config = params.config

    if not config.is_sh_command:
        # Only validate git args if actually using git and not running another executable.
        arg0 = args[0]
        if arg0 == 'st':
            args[0] = 'status'
            if len(args) == 1:
                args.insert(1, '-s')

        elif arg0 == 'co':
            args[0] = 'checkout'

        elif len(args) == 1:

            if arg0 == 'mu-branch':
                args[0] = 'rev-parse'
                args.insert(1, '--abbrev-ref')
                args.insert(2, 'HEAD')

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg)
        return Status(msg, True, config)

    commands = []
    for repo in config.repos:
        if not os.path.exists(repo):
            Print('%s does not exist' % (repo,))
        else:
            commands.append(ParallelCmd(repo, [config.git] + args))

    ExecuteInParallel(commands, on_output, serial=config.serial)

    return Status('Finished', True)

