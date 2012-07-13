'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from __future__ import with_statement
from mu_repo.print_ import Print
import os.path
from mu_repo import Status
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel


#===================================================================================================
# Run
#===================================================================================================
def Run(params, on_output=Print):
    args = params.args
    config = params.config

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

        elif arg0 == 'mu-patch':
            args[0] = 'diff'
            args.insert(1, '--cached')
            args.insert(2, '--full-index')
            config.serial = False #Always exec in parallel mode!
            def OnOutput(output):
                stdout = output.stdout
                if stdout.strip():
                    Print('Writing diff --cached for: ', output.repo)
                    with open('__diff__.' + output.repo + '.patch', 'w') as f:
                        f.write(stdout)
                else:
                    Print('EMPTY diff --cached for: ', output.repo)
            on_output = OnOutput

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

